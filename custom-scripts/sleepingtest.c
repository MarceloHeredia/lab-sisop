#include <stdio.h>
#include <linux/kernel.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdlib.h>

#define SYSCALL_SLEEPINGLIST 442 // código da syscall

int main(int argc, char** argv){  
	long buf[256];
	int ret;

	
	printf("Invoking 'sleepingList' system call.\n");
         
	ret = syscall(SYSCALL_SLEEPINGLIST, buf, sizeof(buf)); 

	printf("used syscall");

	if( ret < 0 ){
		printf("sleepingList Error: %d", ret);
		return -1;
	}
         
	if(ret > 0) {
		/* Success, show the process info. */
		for(int i=0; i<ret; i++){
			printf("%s\n", buf[i]);
		}
	}
	else {
		printf("System call 'sleepingList' did not find any sleeping process %d\n", ret);
		return 1;
	}
          
	return 0;
}