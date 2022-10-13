/* Texture functions for cs580 GzLib	*/
#include    "stdafx.h" 
#include	"stdio.h"
#include    <cmath>
#include	"Gz.h"

GzColor	*image=NULL;
int xs, ys;
int reset = 1;

/* Image texture function */
int tex_fun(float u, float v, GzColor color)
{
  unsigned char		pixel[3];
  unsigned char     dummy;
  char  		foo[8];
  int   		i, j;
  FILE			*fd;

  if (reset) {          /* open and load texture file */
    fd = fopen ("texture", "rb");
    if (fd == NULL) {
      fprintf (stderr, "texture file not found\n");
      exit(-1);
    }
    fscanf (fd, "%s %d %d %c", foo, &xs, &ys, &dummy);
    image = (GzColor*)malloc(sizeof(GzColor)*(xs+1)*(ys+1));
    if (image == NULL) {
      fprintf (stderr, "malloc for texture image failed\n");
      exit(-1);
    }

    for (i = 0; i < xs*ys; i++) {	/* create array of GzColor values */
      fread(pixel, sizeof(pixel), 1, fd);
      image[i][RED] = (float)((int)pixel[RED]) * (1.0 / 255.0);
      image[i][GREEN] = (float)((int)pixel[GREEN]) * (1.0 / 255.0);
      image[i][BLUE] = (float)((int)pixel[BLUE]) * (1.0 / 255.0);
      }

    reset = 0;          /* init is done */
	fclose(fd);
  }

/* bounds-test u,v to make sure nothing will overflow image array bounds */
/* determine texture cell corner values and perform bilinear interpolation */
/* set color to interpolated GzColor value and return */
    if (!(u >= 0.0f && u <= 1.0f && v >= 0.0f && v <= 1.0f))
        return GZ_FAILURE;

    using std::ceil;
    using std::floor;
    auto scaled_u = u * (xs - 1), scaled_v = v * (ys - 1),
        floored_float_u = floor(scaled_u), floored_float_v = floor(scaled_v),
        delta_u = scaled_u - floored_float_u, delta_v = scaled_v - floored_float_v;
    auto floored_u = static_cast<int>(floored_float_u),
        floored_v = static_cast<int>(floored_float_v),
        ceiled_u = static_cast<int>(ceil(scaled_u)),
        ceiled_v = static_cast<int>(ceil(scaled_v));
    // Bilinear Coefficients: fc == coefficient for floored v, ceiled u
    auto cc = delta_u * delta_v, fc = delta_u * (1.0f - delta_v),
        cf = (1.0f - delta_u) * delta_v, ff = (1.0f - delta_u) * (1.0f - delta_v);

    for (int i = 0; i < 3; ++i)
        color[i] = image[ceiled_v * xs + ceiled_u][i] * cc
            + image[ceiled_v * xs + floored_u][i] * cf
            + image[floored_v * xs + ceiled_u][i] * fc
            + image[floored_v * xs + floored_u][i] * ff;
	return GZ_SUCCESS;
}

/* Procedural texture function */
int ptex_fun(float u, float v, GzColor color)
{

	return GZ_SUCCESS;
}

/* Free texture memory */
int GzFreeTexture()
{
	if(image!=NULL)
		free(image);
	return GZ_SUCCESS;
}

