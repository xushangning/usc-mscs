/* CS580 Homework 3 */

#include	<numeric>
#include	<numbers>
#include	"stdio.h"
#include	<cmath>
#include	<algorithm>
#include	<array>
#include	<valarray>
#include	"Gz.h"
#include	"rend.h"

import dda;
import geometry;
import linalg;

#define PI (float) 3.14159265358979323846

constexpr int N_RGB = 3;

constexpr GzPixel BACKGROUND{ 0, 0, 1000, 1, std::numeric_limits<GzDepth>::max() };

constexpr GzIntensity MIN_INTENSITY = 0, MAX_INTENSITY = 4095;

inline constexpr float deg2rad(float d) noexcept { return d * std::numbers::pi_v<float> / 180; }

using std::fill;
using std::cos;
using std::sin;

using std::valarray;

int GzRender::GzRotXMat(float degree, GzMatrix mat)
{
/* HW 3.1
// Create rotate matrix : rotate along x axis
// Pass back the matrix using mat value
*/
	fill(mat[0], mat[4], 0.0f);
	mat[0][0] = mat[3][3] = 1;
	auto rad = deg2rad(degree);
	mat[1][1] = mat[2][2] = cos(rad);
	mat[2][1] = sin(rad);
	mat[1][2] = -mat[2][1];

	return GZ_SUCCESS;
}

int GzRender::GzRotYMat(float degree, GzMatrix mat)
{
/* HW 3.2
// Create rotate matrix : rotate along y axis
// Pass back the matrix using mat value
*/
	fill(mat[0], mat[4], 0.0f);
	mat[1][1] = mat[3][3] = 1;
	auto rad = deg2rad(degree);
	mat[0][0] = mat[2][2] = cos(rad);
	mat[0][2] = sin(rad);
	mat[2][0] = -mat[0][2];

	return GZ_SUCCESS;
}

int GzRender::GzRotZMat(float degree, GzMatrix mat)
{
/* HW 3.3
// Create rotate matrix : rotate along z axis
// Pass back the matrix using mat value
*/
	fill(mat[0], mat[4], 0.0f);
	mat[2][2] = mat[3][3] = 1;
	auto rad = deg2rad(degree);
	mat[0][0] = mat[1][1] = cos(rad);
	mat[1][0] = sin(rad);
	mat[0][1] = -mat[1][0];

	return GZ_SUCCESS;
}

int GzRender::GzTrxMat(GzCoord translate, GzMatrix mat)
{
/* HW 3.4
// Create translation matrix
// Pass back the matrix using mat value
*/
	fill(mat[0], mat[4], 0.0f);
	mat[0][0] = mat[1][1] = mat[2][2] = mat[3][3] = 1;
	mat[0][3] = translate[0];
	mat[1][3] = translate[1];
	mat[2][3] = translate[2];

	return GZ_SUCCESS;
}


int GzRender::GzScaleMat(GzCoord scale, GzMatrix mat)
{
/* HW 3.5
// Create scaling matrix
// Pass back the matrix using mat value
*/
	fill(mat[0], mat[4], 0.0f);
	mat[0][0] = scale[0];
	mat[1][1] = scale[1];
	mat[2][2] = scale[2];
	mat[3][3] = 1;

	return GZ_SUCCESS;
}


using std::min;

GzRender::GzRender(int xRes, int yRes)
	: m_camera({
		.position = {DEFAULT_IM_X, DEFAULT_IM_Y, DEFAULT_IM_Z},
		.worldup = {0, 1, 0},
		.FOV = DEFAULT_FOV
	}),
	matlevel(0), Xsp(), numlights{}
{
/* HW1.1 create a framebuffer for MS Windows display:
 -- set display resolution
 -- allocate memory for framebuffer : 3 bytes(b, g, r) x width x height
 -- allocate memory for pixel buffer
 */
	xres = min(xRes, MAXXRES);
	yres = min(yRes, MAXYRES);

	auto resolution = xres * yres;
	framebuffer = new char[resolution * N_RGB];
	pixelbuffer = new GzPixel[resolution];

/* HW 3.6
- setup Xsp and anything only done once 
- init default camera 
*/
	Xsp[0][0] = Xsp[0][3] = static_cast<float>(xres) / 2;
	Xsp[1][3] = static_cast<float>(yres) / 2;
	Xsp[1][1] = -Xsp[1][3];
	Xsp[2][2] = static_cast<float>(std::numeric_limits<GzDepth>::max());
	Xsp[3][3] = 1;
}

GzRender::~GzRender()
{
/* HW1.2 clean up, free buffer memory */
	delete pixelbuffer;
	delete framebuffer;
}

int GzRender::GzDefault()
{
/* HW1.3 set pixel buffer to some default values - start a new frame */
	for (int i = 0; i < xres * yres; ++i)
		pixelbuffer[i] = BACKGROUND;
	return GZ_SUCCESS;
}

int GzRender::GzBeginRender()
{
/* HW 3.7 
- setup for start of each frame - init frame buffer color,alpha,z
- compute Xiw and projection xform Xpi from camera definition 
- init Ximage - put Xsp at base of stack, push on Xpi and Xiw 
- now stack contains Xsw and app can push model Xforms when needed 
*/
	GzPushMatrix(Xsp);

	// Xpi
	auto& Xpi = m_camera.Xpi;
	fill(Xpi[0], Xpi[4], 0.0f);
	Xpi[0][0] = Xpi[1][1] = Xpi[3][3] = 1;
	Xpi[2][2] = Xpi[3][2] = std::tan(deg2rad(m_camera.FOV / 2));
	GzPushMatrix(Xpi);

	// Xiw
	Vector z(m_camera.lookat);
	z -= m_camera.position;
	z /= abs(z);

	Vector y(m_camera.worldup);
	y -= y.Dot(z) * z;
	y /= abs(y);

	Vector x = y.Cross(z);
	
	auto& Xiw = m_camera.Xiw;
	fill(Xiw[0], Xiw[4], 0.0f);
	Xiw[0][0] = x[0];
	Xiw[0][1] = x[1];
	Xiw[0][2] = x[2];

	Xiw[1][0] = y[0];
	Xiw[1][1] = y[1];
	Xiw[1][2] = y[2];

	Xiw[2][0] = z[0];
	Xiw[2][1] = z[1];
	Xiw[2][2] = z[2];

	Xiw[0][3] = -x.Dot(m_camera.position);
	Xiw[1][3] = -y.Dot(m_camera.position);
	Xiw[2][3] = -z.Dot(m_camera.position);

	Xiw[3][3] = 1.0f;

	GzPushMatrix(Xiw);

	return GZ_SUCCESS;
}

int GzRender::GzPutCamera(GzCamera camera)
{
/* HW 3.8 
/*- overwrite renderer camera structure with new camera definition
*/
	m_camera = camera;
	return GZ_SUCCESS;	
}

int GzRender::GzPushMatrix(GzMatrix	matrix)
{
/* HW 3.9 
- push a matrix onto the Ximage stack
- check for stack overflow
*/
	if (matlevel >= MATLEVELS)
		return GZ_FAILURE;

	// The matrix after scaling and translation components are removed.
	GzMatrix matrix_for_norm = {
		{1.0f, 0.0f, 0.0f, 0.0f},
		{0.0f, 1.0f, 0.0f, 0.0f},
		{0.0f, 0.0f, 1.0f, 0.0f},
		{0.0f, 0.0f, 0.0f, 1.0f}
	};
	if (!Is3x3Diagonal(matrix))
		// If not diagnoal, the upper left 3 * 3 matrix must be a rotation
		// matrix. Copy it over to matrix_for_norm.
		for (int i = 0; i < 3; ++i)
			std::copy_n(matrix[i], 3, matrix_for_norm[i]);

	if (matlevel) {
		MatMul(Ximage[matlevel], Ximage[matlevel - 1], matrix);
		MatMul(Xnorm[matlevel], Xnorm[matlevel - 1], matrix_for_norm);
	}
	else {
		std::copy(matrix[0], matrix[4], Ximage[matlevel][0]);
		std::copy(matrix_for_norm[0], matrix_for_norm[4], Xnorm[matlevel][0]);
	}
	++matlevel;

	return GZ_SUCCESS;
}

int GzRender::GzPopMatrix()
{
/* HW 3.10
- pop a matrix off the Ximage stack
- check for stack underflow
*/
	if (matlevel == 0)
		return GZ_FAILURE;
	--matlevel;
	return GZ_SUCCESS;
}

int GzRender::GzPut(int i, int j, GzIntensity r, GzIntensity g, GzIntensity b, GzIntensity a, GzDepth z)
{
/* HW1.4 write pixel values into the buffer */
	if (!(i >= 0 && j >= 0 && i < xres && j < yres))
		return GZ_FAILURE;

	using std::clamp;
	if (z < pixelbuffer[ARRAY(i, j)].z)
		pixelbuffer[ARRAY(i, j)] = {
			clamp(r, MIN_INTENSITY, MAX_INTENSITY),
			clamp(g, MIN_INTENSITY, MAX_INTENSITY),
			clamp(b, MIN_INTENSITY, MAX_INTENSITY),
			a, z
		};
	return GZ_SUCCESS;
}


int GzRender::GzGet(int i, int j, GzIntensity *r, GzIntensity *g, GzIntensity *b, GzIntensity *a, GzDepth *z)
{
/* HW1.5 retrieve a pixel information from the pixel buffer */
	if (!(i >= 0 && j >= 0 && i < xres && j < yres))
		return GZ_FAILURE;

	auto& pixel = pixelbuffer[ARRAY(i, j)];
	if (r)
		*r = pixel.red;
	if (g)
		*g = pixel.green;
	if (b)
		*b = pixel.blue;
	if (a)
		*a = pixel.alpha;
	if (z)
		*z = pixel.z;
	return GZ_SUCCESS;
}


inline char twelve2EightBitColor(GzIntensity color)
{
	return static_cast<char>(color >> 4);
}

int GzRender::GzFlushDisplay2File(FILE* outfile)
{
/* HW1.6 write image to ppm file -- "P6 %d %d 255\r" */
	fprintf(outfile, "P6 %d %d 255\n", xres, yres);		// Header

	for (int i = 0; i < xres * yres; ++i) {
		fputc(twelve2EightBitColor(pixelbuffer[i].red), outfile);
		fputc(twelve2EightBitColor(pixelbuffer[i].green), outfile);
		fputc(twelve2EightBitColor(pixelbuffer[i].blue), outfile);
	}
	return GZ_SUCCESS;
}

int GzRender::GzFlushDisplay2FrameBuffer()
{
/* HW1.7 write pixels to framebuffer: 
	- put the pixels into the frame buffer
	- CAUTION: when storing the pixels into the frame buffer, the order is blue, green, and red 
	- NOT red, green, and blue !!!
*/
	for (int i = 0, j = 0; i < xres * yres; ++i, j += N_RGB) {
		framebuffer[j] = twelve2EightBitColor(pixelbuffer[i].blue);
		framebuffer[j + 1] = twelve2EightBitColor(pixelbuffer[i].green);
		framebuffer[j + 2] = twelve2EightBitColor(pixelbuffer[i].red);
	}
	return GZ_SUCCESS;
}


/***********************************************/
/* HW2 methods: implement from here */

int GzRender::GzPutAttribute(int numAttributes, GzToken	*nameList, GzPointer *valueList) 
{
/* HW 2.1
-- Set renderer attribute states (e.g.: GZ_RGB_COLOR default color)
-- In later homeworks set shaders, interpolaters, texture maps, and lights
*/

/*
- GzPutAttribute() must accept the following tokens/values:

- GZ_RGB_COLOR					GzColor		default flat-shade color
- GZ_INTERPOLATE				int			shader interpolation mode
- GZ_DIRECTIONAL_LIGHT			GzLight
- GZ_AMBIENT_LIGHT            	GzLight		(ignore direction)
- GZ_AMBIENT_COEFFICIENT		GzColor		Ka reflectance
- GZ_DIFFUSE_COEFFICIENT		GzColor		Kd reflectance
- GZ_SPECULAR_COEFFICIENT       GzColor		Ks coef's
- GZ_DISTRIBUTION_COEFFICIENT   float		spec power
*/
	for (int i = 0; i < numAttributes; ++i)
		switch (nameList[i]) {
		case GZ_RGB_COLOR:
			std::copy_n(*static_cast<GzColor*>(valueList[i]), N_RGB, flatcolor);
			break;
		case GZ_INTERPOLATE:
			interp_mode = *static_cast<int*>(valueList[i]);
			break;
		case GZ_DIRECTIONAL_LIGHT:
			if (numlights < MAX_LIGHTS)
				lights[numlights++] = *static_cast<GzLight*>(valueList[i]);
			else
				return GZ_FAILURE;
			break;
		case GZ_AMBIENT_LIGHT:
			ambientlight = *static_cast<GzLight*>(valueList[i]);
			break;
		case GZ_AMBIENT_COEFFICIENT:
			std::copy_n(*static_cast<GzColor*>(valueList[i]), N_RGB, Ka);
			break;
		case GZ_DIFFUSE_COEFFICIENT:
			std::copy_n(*static_cast<GzColor*>(valueList[i]), N_RGB, Kd);
			break;
		case GZ_SPECULAR_COEFFICIENT:
			std::copy_n(*static_cast<GzColor*>(valueList[i]), N_RGB, Ks);
			break;
		case GZ_DISTRIBUTION_COEFFICIENT:
			spec = *static_cast<float*>(valueList[i]);
			break;
		}
	return GZ_SUCCESS;
}

int tex_fun(float u, float v, GzColor color);

valarray<float> phongLighting(const GzRender& renderer, valarray<float> normal)
{
	// Compute ambient color first.
	valarray<float> result(renderer.Ka, N_RGB), specular_term(N_RGB), diffuse_term(N_RGB);
	result *= valarray<float>(renderer.ambientlight.color, N_RGB);

	// Bring the normal vector to image space.
	MatValarrayMul(renderer.Xnorm[renderer.matlevel - 1], normal);

	const valarray<float> eye = { 0.0f, 0.0f, -1.0f };
	for (int i = 0; i < renderer.numlights; ++i) {
		const auto& light = renderer.lights[i];
		const valarray<float> light_direction(light.direction, 3), light_color(light.color, N_RGB);

		auto n_dot_e = Dot(normal, eye), n_dot_l = Dot(normal, light_direction);
		if (n_dot_e > 0 && n_dot_l < 0 || n_dot_e < 0 && n_dot_l > 0)
			// The eye/camera and the light are on opposite sides of the triangle.
			continue;

		if (n_dot_e <= 0 && n_dot_l <= 0) {
			// The normal's direction is opposite to both the light and
			// eye/camera's directions. Flip the normal's direction.
			normal = -normal;
			n_dot_l = -n_dot_l;
		}

		diffuse_term += light_color * n_dot_l;

		const auto reflection = normal * n_dot_l * 2 - light_direction;
		auto clamped_r_dot_e = std::max(Dot(reflection, eye), 0.0f);
		specular_term += light_color * std::pow(clamped_r_dot_e, renderer.spec);
	}

	result += valarray<float>(renderer.Ks, N_RGB) * specular_term
		+ valarray<float>(renderer.Kd, N_RGB) * diffuse_term;
	for (auto& v : result)
		v = std::min(v, 1.0f);
	return result;
}

/// <summary>
/// Rasterize a trapezoid parallel to the x-axis or its degenerated form, a
/// triangle with one edge parallel to the x-axis.
/// </summary>
/// 
/// <param name="leader">
/// An iterator that provides coordinates along one side that is not parallel
/// to the x-axis. It is the iterator used to determine the end of a loop.
/// </param>
/// <param name="follower">
/// An iterator that provides coordinates along the other side that is not
/// parallel to the x-axis
/// </param>
/// <param name="leader_on_x_begin">
/// Whether the leader iterator corresponds to the side with smaller
/// x-coordinates than the other.
/// </param>
void putTrapezoid(
	GzRender& renderer,	PerspectiveCorrectDDA::iterator& leader,
	PerspectiveCorrectDDA::iterator& follower,
	const PerspectiveCorrectDDA::iterator& end, bool leader_on_x_begin
)
{
	auto& x_begin = leader_on_x_begin ? leader : follower,
		& x_end = leader_on_x_begin ? follower : leader;
	while (leader != end) {
		PerspectiveCorrectDDA x(0, *x_begin, *x_end);		// DDA along the x axis.
		for (const auto& v : x) {
			valarray<float> color;
			switch (renderer.interp_mode) {
			case GZ_FLAT:
				color = { renderer.flatcolor, N_RGB };
				break;
			case GZ_COLOR:
				color = v[2];
				break;
			case GZ_NORMALS: {
				GzColor texture;
				tex_fun(v[1][0], v[1][1], texture);
				std::ranges::copy(texture, renderer.Ka);
				std::ranges::copy(texture, renderer.Kd);
				color = phongLighting(renderer, v[2] / Norm(v[2]));
				break;
			}
			}

			renderer.GzPut(
				static_cast<int>(v[0][0]), static_cast<int>(v[0][1]),
				renderer.ctoi(color[0]), renderer.ctoi(color[1]), renderer.ctoi(color[2]),
				1, static_cast<GzDepth>(v[0][2])
			);
		}

		++leader;
		++follower;
	}

}

/// <summary>
/// Represent a sample point in a 3D model.
/// </summary>
struct ModelPoint { valarray<float> coordinate, normal, texture; };

/// <summary>
/// Construct different DDAs in different interpolation modes. The current
/// structure of DDA's interpolated value is [coordinate, texture, normal].
/// </summary>
PerspectiveCorrectDDA BuildPerspectiveCorrectDDA(
	const GzRender& renderer, std::size_t param_index,
	const ModelPoint& begin, const ModelPoint& end
)
{
	return renderer.interp_mode == GZ_COLOR
			? PerspectiveCorrectDDA(
				param_index,
				{
					begin.coordinate,
					begin.texture,
					phongLighting(renderer, begin.normal)
				},
				{
					end.coordinate,
					end.texture,
					phongLighting(renderer, end.normal)
				}
			)
		: renderer.interp_mode == GZ_NORMALS
			? PerspectiveCorrectDDA(
				param_index,
				{ begin.coordinate, begin.texture, begin.normal },
				{ end.coordinate, end.texture, end.normal }
			)
		: PerspectiveCorrectDDA(param_index, { begin.coordinate }, { end.coordinate });
}

int GzRender::GzPutTriangle(int numParts, GzToken *nameList, GzPointer *valueList)
/* numParts - how many names and values */
{
/* HW 2.2
-- Pass in a triangle description with tokens and values corresponding to
	GZ_NULL_TOKEN:		do nothing - no values
	GZ_POSITION:		3 vert positions in model space
-- Return error code
*/
/*
-- Xform positions of verts using matrix on top of stack
-- Clip - just discard any triangle with any vert(s) behind view plane
		- optional: test for triangles with all three verts off-screen (trivial frustum cull)
-- invoke triangle rasterizer
*/
	GzCoord* vertices{}, * normals{};
	GzTextureIndex* textures{};
	for (int i = 0; i < numParts; ++i)
		switch (nameList[i]) {
		case GZ_POSITION:
			vertices = static_cast<GzCoord*>(valueList[i]);
			break;
		case GZ_NORMAL:
			normals = static_cast<GzCoord*>(valueList[i]);
			break;
		case GZ_TEXTURE_INDEX:
			textures = static_cast<GzTextureIndex*>(valueList[i]);
			break;
		}
	if (!(vertices && normals && textures))
		return GZ_FAILURE;

	typedef std::array<ModelPoint, 3> TriangleModel;
	TriangleModel triangle;
	for (TriangleModel::size_type i = 0; i < triangle.size(); ++i) {
		auto& p = triangle[i];
		p.coordinate = valarray<float>(vertices[i], 3);
		// Cull triangles with a negative-z vertex.
		if (!(MatValarrayMul(Ximage[matlevel - 1], p.coordinate) && p.coordinate[2] >= 0))
			return GZ_SUCCESS;

		p.normal = valarray<float>(normals[i], 3);
		p.texture = valarray<float>(textures[i], 2);
	}

	std::array sorted_by_y = { triangle.cbegin(), triangle.cbegin() + 1, triangle.cbegin() + 2 };
	typedef TriangleModel::const_iterator ModelIter; 
	std::ranges::sort(sorted_by_y, [](ModelIter i, ModelIter j) { return i->coordinate[1] < j->coordinate[1]; });

	const auto& y_begin = *sorted_by_y[0],
		/// <summary>
		/// The vertex with the middling y-coordinate among the three.
		/// The triangle is divided into two parts by the line that is
		/// parallel to the x-ais and goes through this vertex.
		/// </summary>
		& y_mid = *sorted_by_y[1],
		& y_end = *sorted_by_y[2];

	auto cross_product = CrossProduct2D(y_begin.coordinate, y_end.coordinate, y_mid.coordinate);
	if (cross_product == 0)
		// degenerated triangle
		return GZ_SUCCESS;
	// Whether the edges (y_begin, y_mid, y_end) have smaller
	// x-coordinates than the edge (y_begin, y_end) i.e., on the left
	// of (y_begin, y_end).
	bool y_mid_on_x_begin = cross_product > 0;

	// Compute color for flat shading.
	if (interp_mode == GZ_FLAT)
		std::ranges::copy(phongLighting(*this, triangle[0].normal), flatcolor);

	PerspectiveCorrectDDA begin_end = BuildPerspectiveCorrectDDA(*this, 1, y_begin, y_end);
	auto begin_end_iter = begin_end.begin();
	if (y_begin.coordinate[1] != y_mid.coordinate[1]) {
		// Rasterize the part of the triangle with smaller x-coordinates.
		PerspectiveCorrectDDA begin_mid = BuildPerspectiveCorrectDDA(*this, 1, y_begin, y_mid);
		auto begin_mid_iter = begin_mid.begin();

		putTrapezoid(*this, begin_mid_iter, begin_end_iter, begin_mid.end(), y_mid_on_x_begin);
	}

	if (y_mid.coordinate[1] != y_end.coordinate[1]) {
		// Rasterize the other part of the triangle with larger x-coordinates.
		PerspectiveCorrectDDA mid_end = BuildPerspectiveCorrectDDA(*this, 1, y_mid, y_end);
		auto mid_end_iter = mid_end.begin();

		putTrapezoid(*this, mid_end_iter, begin_end_iter, mid_end.end(), y_mid_on_x_begin);
	}

	return GZ_SUCCESS;
}
