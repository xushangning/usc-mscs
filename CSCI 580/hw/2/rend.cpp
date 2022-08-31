#include	"stdafx.h"
#include	"stdio.h"
#include	"math.h"
#include	<algorithm>
#include	"Gz.h"
#include	"rend.h"

/***********************************************/
/* HW1 methods: copy here the methods from HW1 */

constexpr int N_RGB = 3;

constexpr GzPixel BACKGROUND{ 0, 0, 1000, 1, 0 };

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

	return GZ_SUCCESS;
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

	return GZ_SUCCESS;
}

