#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <regex.h>
#include <dirent.h>
#include <fcntl.h>
#include <linux/input.h>
#include <stdbool.h>

bool Input ( float* c_x, float* c_y, float* scale, float* t_x, float* t_y )
{
    static int first = 1;
    static int keyboardFd = -1;
    struct input_event ev[64];
    int rd;

    bool ret = false;


    // Set up the devices on the first call
    if(first)
    {
	DIR *dirp;
	struct dirent *dp;
	regex_t kbd;

	char fullPath[1024];
	static char *dirName = "/dev/input/by-id";
	int result;

	if(regcomp(&kbd,"event-kbd",0)!=0)
	{
	    printf("regcomp for kbd failed\n");
	    return true;

	}

	if ((dirp = opendir(dirName)) == NULL) {
	    perror("couldn't open '/dev/input/by-id'");
	    return true;
	}

	// Find any files that match the regex for keyboard or mouse

	do {
	    errno = 0;
	    if ((dp = readdir(dirp)) != NULL) 
	    {
		printf("readdir (%s)\n",dp->d_name);
		if(regexec (&kbd, dp->d_name, 0, NULL, 0) == 0)
		{
		    printf("match for the kbd = %s\n",dp->d_name);
		    sprintf(fullPath,"%s/%s",dirName,dp->d_name);
		    keyboardFd = open(fullPath,O_RDONLY | O_NONBLOCK);
		    printf("%s Fd = %d\n",fullPath,keyboardFd);
		    printf("Getting exclusive access: ");
		    result = ioctl(keyboardFd, EVIOCGRAB, 1);
		    printf("%s\n", (result == 0) ? "SUCCESS" : "FAILURE");

		}
	    }
	} while (dp != NULL);

	closedir(dirp);

	regfree(&kbd);
	
	first = 0;
	if(keyboardFd == -1) return true;

    }

    // Read events from keyboard

    rd = read(keyboardFd,ev,sizeof(ev));
    if(rd > 0)
    {
	int count,n;
	struct input_event *evp;

	count = rd / sizeof(struct input_event);
	n = 0;
	while(count--)
	{
	    evp = &ev[n++];
	    if(evp->type == 1)
	    {
		if(evp->value == 1) 
		{
		    if(evp->code == KEY_UP)
		    {
                        *c_y = *c_y + 0.01;
			printf("Up: %f\n", *c_y);
		    }
		    if(evp->code == KEY_DOWN )
		    {
                        *c_y = *c_y - 0.01;
			printf("Down: %f\n", *c_y);
		    }
		    if(evp->code == KEY_LEFT)
		    {
                        *c_x = *c_x - 0.01;
			printf("Left: %f\n", *c_x);
		    }
		    if(evp->code == KEY_RIGHT)
		    {
                        *c_x = *c_x + 0.01;
			printf("Right: %f\n", *c_x);
		    }
		    if(evp->code == KEY_W)
		    {
                        *t_y = *t_y + 0.1;
			printf("W: %f\n", *t_y);
                    }
		    if(evp->code == KEY_S)
		    {
                        *t_y = *t_y - 0.1;
			printf("S: %f\n", *t_y);
		    }
		    if(evp->code == KEY_A)
		    {
                        *t_x = *t_x - 0.1;
			printf("A: %f\n", *t_x);
                    }
		    if(evp->code == KEY_D)
		    {
                        *t_x = *t_x + 0.1;
			printf("D: %f\n", *t_x);
		    }
		    if(evp->code == KEY_Q)
		    {
                        *scale = *scale + 0.1;
			printf("W: %f\n", *scale);
                    }
		    if(evp->code == KEY_E)
		    {
                        *scale = *scale - 0.1;
			printf("S: %f\n", *scale);
		    }
		}


		if((evp->code == KEY_Q) && (evp->value == 1))
		    ret = true;;


	    }
	}

    }

    return(ret);

}
