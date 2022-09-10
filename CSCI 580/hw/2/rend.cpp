#include	"stdio.h"
#include	"math.h"
#include	<numeric>
#include	<algorithm>
#include	<array>
#include	"Gz.h"
#include	"rend.h"

import dda;

/***********************************************/
/* HW1 methods: copy here the methods from HW1 */

constexpr int N_RGB = 3;

constexpr GzPixel BACKGROUND{ 0, 0, 1000, 1, std::numeric_limits<GzDepth>::max() };

constexpr GzIntensity MAX_INTENSITY = 4095;

inline char twelve2EightBitColor(GzIntensity color)
{
	return static_cast<char>(color >> 4);
}

using std::min;

GzRender::GzRender(int xRes, int yRes)
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


int GzRender::GzPut(int i, int j, GzIntensity r, GzIntensity g, GzIntensity b, GzIntensity a, GzDepth z)
{
/* HW1.4 write pixel values into the buffer */
	if (!(i >= 0 && j >= 0 && i < xres && j < yres))
		return GZ_FAILURE;

	if (z < pixelbuffer[ARRAY(i, j)].z)
		pixelbuffer[ARRAY(i, j)] = {
			min(r, MAX_INTENSITY),
			min(g, MAX_INTENSITY),
			min(b, MAX_INTENSITY),
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
	for (int i = 0; i < numAttributes; ++i)
		switch (nameList[i]) {
		case GZ_RGB_COLOR:
			std::copy_n(*static_cast<GzColor*>(valueList[i]), N_RGB, flatcolor);
			break;
		}
	return GZ_SUCCESS;
}

inline float crossProduct(const GzCoord& tail, const GzCoord& head_start, const GzCoord& head_end)
{
	return (head_start[0] - tail[0]) * (head_end[1] - tail[1]) - (head_end[0] - tail[0]) * (head_start[1] - tail[1]);
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
	GzRender& render, const GzIntensity(&color)[3],
	DDA::iterator& leader, DDA::iterator& follower, const DDA::iterator& end,
	bool leader_on_x_begin
)
{
	auto& x_begin = leader_on_x_begin ? leader : follower,
		& x_end = leader_on_x_begin ? follower : leader;
	while (leader != end) {
		DDA x(0, *x_begin, *x_end);		// DDA along the x axis.
		for (auto& coord : x)
			render.GzPut(
				static_cast<int>(coord[0]), static_cast<int>(coord[1]),
				color[0], color[1], color[2],
				1, static_cast<GzDepth>(coord[2])
			);

		++leader;
		++follower;
	}

}

int GzRender::GzPutTriangle(int	numParts, GzToken *nameList, GzPointer *valueList)
/* numParts - how many names and values */
{
/* HW 2.2
-- Pass in a triangle description with tokens and values corresponding to
	GZ_NULL_TOKEN:		do nothing - no values
	GZ_POSITION:		3 vert positions in model space
-- Invoke the rastrizer/scanline framework
-- Return error code
*/
	for (int i = 0; i < numParts; ++i)
		switch (nameList[i]) {
		case GZ_POSITION: {
			auto first_vertex = static_cast<GzCoord*>(valueList[i]);

			std::array vertices = { first_vertex, first_vertex + 1, first_vertex + 2 };
			// Sort by y.
			std::sort(vertices.begin(), vertices.end(), [](GzCoord* a, GzCoord* b) { return (*a)[1] < (*b)[1]; });
			GzCoord& y_begin = *vertices[0],
				/// <summary>
				/// The vertex with the middling y-coordinate among the three.
				/// The triangle is divided into two parts by the line that is
				/// parallel to the x-ais and goes through this vertex.
				/// </summary>
				& y_mid = *vertices[1],
				& y_end = *vertices[2];

			auto cross_product = crossProduct(y_begin, y_end, y_mid);
			if (cross_product == 0)
				// degenerated triangle
				break;
			// Whether the edges (y_begin, y_mid, y_end) have smaller
			// x-coordinates than the edge (y_begin, y_end) i.e., on the left
			// of (y_begin, y_end).
			bool y_mid_on_x_begin = cross_product > 0;
			
			GzIntensity color[]{ ctoi(flatcolor[0]), ctoi(flatcolor[1]), ctoi(flatcolor[2]) };

			DDA begin_end(1, y_begin, y_end);
			auto begin_end_iter = begin_end.begin();
			if (y_begin[1] != y_mid[1]) {
				// Rasterize the part of the triangle with smaller x-coordinates.
				DDA begin_mid(1, y_begin, y_mid);
				auto begin_mid_iter = begin_mid.begin();

				putTrapezoid(*this, color, begin_mid_iter, begin_end_iter, begin_mid.end(), y_mid_on_x_begin);
			}

			if (y_mid[1] != y_end[1]) {
				// Rasterize the other part of the triangle with larger x-coordinates.
				DDA mid_end(1, y_mid, y_end);
				auto mid_end_iter = mid_end.begin();

				putTrapezoid(*this, color, mid_end_iter, begin_end_iter, mid_end.end(), y_mid_on_x_begin);
			}

			break;
		}
		}
	return GZ_SUCCESS;
}

