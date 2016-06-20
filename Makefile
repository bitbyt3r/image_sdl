build:
	g++ -std=c++0x -Wall -pedantic test.c -o sdl2_test `sdl2-config --cflags --libs` -lSDL2_image
update:
	/opt/vc/bin/raspistill -o test.jpg --timeout 1 --nopreview -w 1920 -h 1080
