#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>

#ifdef WIN32

#include <windows.h>
double get_time()
{
    LARGE_INTEGER t, f;
    QueryPerformanceCounter(&t);
    QueryPerformanceFrequency(&f);
    return (double)t.QuadPart/(double)f.QuadPart;
}

#else

#include <sys/time.h>
#include <sys/resource.h>

double get_time()
{
    struct timeval t;
    struct timezone tzp;
    gettimeofday(&t, &tzp);
    return t.tv_sec + t.tv_usec*1e-6;
}

#endif

typedef struct thread{
	pthread_t thread_id;
	char filename[6];
	int blocksize;
	int random_int;
	double diff;	
} ThreadData;

void* loop_time (void *thread);
void* write_seq_file (void *thread);
void* write_ran_file (void *thread);
void* read_seq_file (void *thread);
void* read_ran_file (void *thread);
int detect_mode(char* mode);

int main(int argc, char *argv[]) {
	int nb_threads = atoi(argv[3]);
	int blocksize = atoi(argv[2]);
	int index;
	char filename[6];
	char* mode = argv[1];
	int i = 0;
	double latency, throughput;
	double  avg_latency = 0, avg_throughput = 0, total_throughput = 0;	
	ThreadData thread[nb_threads];
	ThreadData empty_loop;
	pthread_t empty_loop_id;
	int random_int;

	
	srand(time(NULL));	
	random_int = rand();

	/* Detect mode betweem Write/Sequential, Write/Random, Read/Sequential, Read/Random */
	index = detect_mode(mode);
	printf("BLOCKSIZE : %d",blocksize);
	printf("THREADS   : %d",nb_threads);
	printf("\n=======================================\n");

	/* Calculating empty loop_size latency*/
	empty_loop.blocksize = blocksize/nb_threads;
	empty_loop.diff = 0;
	pthread_create(&empty_loop_id,NULL,loop_time,(void *) argv);
	pthread_join(empty_loop_id, NULL);

	/* Creating threads */		
	for(i=0; i < nb_threads; i++){

		snprintf(filename,sizeof(filename),"temp%d",i);

		strncpy(thread[i].filename,filename,sizeof(filename));
		thread[i].blocksize = blocksize/nb_threads;
		thread[i].random_int = random_int;
		thread[i].diff = 0;

		/* Determining thread to be created (Write, Sequential, Sequential, Random) */
		switch(index){	
		case 0:
			re = pthread_create(&(thread[i].thread_id),NULL,write_seq_file,(void *)(&thread[i]));
			break;
		case 1:
			re = pthread_create(&(thread[i].thread_id),NULL,write_ran_file,(void *)(&thread[i]));
			break;
		case 2:
			re = pthread_create(&(thread[i].thread_id),NULL,read_seq_file,(void *)(&thread[i]));
			break;
		case 3:
			re = pthread_create(&(thread[i].thread_id),NULL,read_ran_file,(void *)(&thread[i]));
			break;		
		default:
			return 0;
			break;
		}
		if(re == -1){
			printf("Error creating thread %d",i);
		else{
			printf("Thread %d/%d created.",i,nb_threads);
		}
	}
	
	/* Wait for all the threads to complete */
	for(i=0; i < nb_threads; i++){
		pthread_join(thread[i].thread_id, NULL);	
	}
	sleep(2);

	/* Calculating and printing  throughput and latency for each thread */
	for(i=0; i < nb_threads; i++){
		latency = ((thread[i].diff)-empty_loop.diff); //We substract the empty loop latency
		throughput = (thread[i].blocksize/1000000.0)/latency;
		avg_latency +=latency;	
		total_throughput += throughput;
		printf("\nThread      : %d\n", i+1);
		printf("Blocksize   : %d B\n", thread[i].blocksize);
		printf("Latency     : %.5f ms\n",(latency*1000));
		printf("Throughput  : %.2f MB/s\n",throughput);
	}

	/* Calculating average throughput and latency */
	avg_latency /= nb_threads;
	avg_throughput = total_throughput/nb_threads;	
	printf("\n---------------------------------------\n");
	printf("Average latency     : %.5f ms\n", (avg_latency*1000));
	printf("Average throughput  : %.5f ms\n", avg_throughput);
	printf("Total throughput    : %.2f MB/s", total_throughput);
	printf("\n---------------------------------------\n");

	return 0;
}


void* loop_time(void* thread){
	ThreadData *my_data = (ThreadData*)thread;
	int blocksize = my_data->blocksize;
	double start,end;
	long i;
	start = get_time();
	for (i=0; i<blocksize; i++){
	}
	end = get_time();
	my_data->diff = end - start;
 
	pthread_exit(NULL);
}

void* write_seq_file(void *thread){
	ThreadData *my_data = (ThreadData*)thread;
	char *filename = my_data->filename;
	FILE* fp = fopen(filename,"w+");
	int blocksize = my_data->blocksize;
	double start,end;
	char c = 'a';
	long i;

	start = get_time();
	for (i=0; i<blocksize; i++){
		fputc(c,fp);
	}
	end = get_time();
	fclose(fp);
	my_data->diff = end - start;
	
	pthread_exit(NULL);
}

void* write_ran_file(void *thread){
	ThreadData *my_data = (ThreadData*)thread;
	char *filename = my_data->filename;
	FILE* fp = fopen(filename,"w+");
	int blocksize = my_data->blocksize;
	int random_int = my_data->random_int;
	char c = 'a';
	long i;
	fseek(fp, random_int, SEEK_SET);
	for (i=0; i<blocksize; i++){
		fputc(c,fp);
	}

	pthread_exit(NULL);
}


void* read_seq_file(void *thread){
	ThreadData *my_data = (ThreadData*)thread;
	char *filename = my_data->filename;
	FILE* fp = fopen(filename,"r+");
	int blocksize = my_data->blocksize;
	long i;
	for(i=0; i<blocksize; i++){
		fgetc(fp);
	}
	pthread_exit(NULL);	
}

void* read_ran_file(void *thread){
	ThreadData *my_data = (ThreadData*)thread;
	char *filename = my_data->filename;
	FILE* fp = fopen(filename,"r+");
	int blocksize = my_data->blocksize;
	int random_int = my_data->random_int;
	long i;
	fseek(fp, random_int, SEEK_SET);
	for(i=0; i<blocksize; i++){
		fgetc(fp);
	}
	pthread_exit(NULL);
}

int detect_mode(char *mode){
	int index;
	printf("\n=======================================\n");
	if (strcmp(mode,"ws") == 0){
		index = 0;
		printf("MODE    : Write / Sequential");
	}
	else if (strcmp(mode, "wr") == 0){
		index = 1;
		printf("MODE    : Write / Random");
	}
	else if (strcmp(mode, "rs") == 0){
		index = 2;
		printf("MODE    : Read / Sequential");
	}
	else if (strcmp(mode, "rr") == 0){
		index = 3;
		printf("MODE    : Read / Random");		
	}
	else{
		fprintf(stderr,"Usage is ./test <ws,wr,rs,rr><nb_threads>");
		exit(0);
	}
return index;
}
