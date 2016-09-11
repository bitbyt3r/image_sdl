#include <fstream>
#include <iostream>
#include <vector>
#include <iterator>
#include <stdio.h>
#include <unistd.h>
#include "camera.h"
#include "graphics.h"
#include "input.h"
#include <math.h>

#define MAIN_TEXTURE_WIDTH 128
#define MAIN_TEXTURE_HEIGHT 128

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
        float speed = 0;
        float rot = 0;
        float fps = 24;

        std::ifstream in("settings.txt");
        std::vector<float> lines{ std::istream_iterator<float>(in),
                                  std::istream_iterator<float>() };
        if (lines.size() == 8) {
                std::cout << "Read settings from file\n";
                c_x = lines[0];
                c_y = lines[1];
                t_x = lines[2];
                t_y = lines[3];
                scale = lines[4];
                speed = lines[5];
                rot = lines[6];
                fps = lines[7];
        }

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
                Input(&c_x, &c_y, &scale, &t_x, &t_y, &speed);
		BeginFrame();
		float aspect_ratio = float(MAIN_TEXTURE_WIDTH)/float(MAIN_TEXTURE_HEIGHT);
//		float screen_aspect_ratio = 1920.f/1080.f;
		float screen_aspect_ratio = 1.f;
                if (speed > 1.f) {
                    speed = 1.f;
                }
                if (speed < -1.f) {
                    speed = -1.f;
                }
                rot = fmod((rot + ((6.282 / fps) * speed)), 6.282);
		DrawTextureRect(&textures[0],-aspect_ratio/screen_aspect_ratio+c_x,-1.f+c_y,aspect_ratio/screen_aspect_ratio+c_x,1.f+c_y,t_x,t_y,rot,scale);
//		DrawTextureRect(&textures[0],1.f,1.f,1.f,1.f,rot);
		EndFrame();
		i++;
                std::ofstream settings;
                settings.open("settings.txt");
                settings << c_x << '\n';
                settings << c_y << '\n';
                settings << t_x << '\n';
                settings << t_y << '\n';
                settings << scale << '\n';
                settings << speed << '\n';
                settings << rot << '\n';
                settings << fps << '\n';
                settings.close();
	}

	StopCamera();
}
