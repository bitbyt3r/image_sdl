#include <stdio.h>
#include <unistd.h>
#include "camera.h"
#include "graphics.h"
#include "input.h"

#define MAIN_TEXTURE_WIDTH 512
#define MAIN_TEXTURE_HEIGHT 512

char tmpbuff[MAIN_TEXTURE_WIDTH*MAIN_TEXTURE_HEIGHT*4];

//entry point
int main(int argc, const char **argv)
{
	//should the camera convert frame data from yuv to argb automatically?
	bool do_argb_conversion = true;

	//init graphics and the camera
	InitGraphics();
	CCamera* cam = StartCamera(MAIN_TEXTURE_WIDTH, MAIN_TEXTURE_HEIGHT,30,1,do_argb_conversion);

	GfxTexture textures[1];
	textures[0].Create(MAIN_TEXTURE_WIDTH, MAIN_TEXTURE_HEIGHT);

	printf("Running frame loop\n");
	long i = 0;

	float c_x = 0;
	float c_y = 0;
	float t_x = 0;
	float t_y = 0;
	float scale = 1.f;

	while(1 == 1)
	{
		//lock the chosen frame buffer, and copy it directly into the corresponding open gl texture
		const void* frame_data; int frame_sz;
		if(cam->BeginReadFrame(0,frame_data,frame_sz))
		{
			if(do_argb_conversion)
			{
				//if doing argb conversion the frame data will be exactly the right size so just set directly
				textures[0].SetPixels(frame_data);
			}
			else
			{
				//if not converting argb the data will be the wrong size and look weird, put copy it in
				//via a temporary buffer just so we can observe something happening!
				memcpy(tmpbuff,frame_data,frame_sz);
				textures[0].SetPixels(tmpbuff);
			}
			cam->EndReadFrame(0);
		}

		//begin frame, draw the texture then end frame (the bit of maths just fits the image to the screen while maintaining aspect ratio)
                Input(&c_x, &c_y, &scale, &t_x, &t_y);
		BeginFrame();
		float aspect_ratio = float(MAIN_TEXTURE_WIDTH)/float(MAIN_TEXTURE_HEIGHT);
//		float screen_aspect_ratio = 1080.f/1920.f;
		float screen_aspect_ratio = 1.f;
                int div; 
                int fps;
                sscanf(argv[1], "%d", &div);
                sscanf(argv[2], "%d", &fps);
                float rot = (6.282 / fps) * (i / div);
		DrawTextureRect(&textures[0],-aspect_ratio/screen_aspect_ratio+c_x,-1.f+c_y,(aspect_ratio/screen_aspect_ratio+c_x)*scale,(1.f+c_y)*scale,t_x,t_y,rot);
//		DrawTextureRect(&textures[0],1.f,1.f,1.f,1.f,rot);
		EndFrame();
		i++;
	}

	StopCamera();
}
