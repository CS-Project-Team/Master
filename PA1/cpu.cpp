#include <time.h>
#include <stdio.h>
#include <math.h>
#include <pthread.h>
#include <iostream>

const int N = 1000;
const int N_TESTS = 1;
const float CONST_FLOAT = 0.7;
int time_int[] = {0, 0, 0};
int time_float[] = {0, 0, 0};

//Performs N^3 operations
void *integer_op(void *threadid){
	int A[N][N];

        //initialize matrix A
        for(int i=0;i<N;i++)
        {
                for(int j=0;j<N;j++)
                {
                        A[i][j] = 0;
                }
        }

	for(int i=0;i<N;i++)
        {
        	for(int j=0;j<N;j++)
                {
			for(int k = 0; k < N; k++)
			{
                        	A[i][j]++;
			}
                }
        }
	printf("\n  - End of a thread.\n");
	
}

//Performs N^3 operations
void *float_op(void *threadid){
	float A[N][N];

        //initialize matrix A
        for(int i=0;i<N;i++)
        {
                for(int j=0;j<N;j++)
                {
                        A[i][j] = 0.0;
                }
        }

	for(int i=0;i<N;i++)
        {
        	for(int j=0;j<N;j++)
                {
			for(int k = 0; k < N; k++)
			{
                        	A[i][j]+=CONST_FLOAT;
			}
                }
        }
	printf("\n  - End of a thread.\n");
	
}

void cpu_test(int n_threads, int test_number){
	pthread_t threads[n_threads];
	
	int rc;
	int i;
	long int total_time = 0;

	//INTEGER OPERATIONS
	clock_t start = clock(), diff;
    	for (i=0; i<n_threads; i++){
		rc = pthread_create(&threads[i], NULL, integer_op, (void *)i);
		printf("\nCREATED THREAD INTEGER%d\n", i);
    	}
	for (int i=0; i<n_threads; i++){
       		(void) pthread_join(threads[i], NULL);
    	}
	diff = clock() - start;
	time_int[test_number] = diff;

	//FLOAT OPERATIONS
	start = clock();
    	for (i=0; i<n_threads; i++){
		rc = pthread_create(&threads[i], NULL, float_op, (void *)i);
		printf("\nCREATED THREAD FLOAT%d\n", i);
    	}
	for (int i=0; i<n_threads; i++){
       		(void) pthread_join(threads[i], NULL);
    	}
	diff = clock() - start;
	time_float[test_number] = diff;
}


int main(int argc, char *argv[]) {
	if(argc != 2)
	{
		printf("\nUsage: <#thread>\n");
		return 1;
	}

	int n_threads = atoi(argv[1]);
	for(int i=0; i<N_TESTS; i++) {
		cpu_test(n_threads, i);
	}
	
	long int n_operations = pow(N,3) * n_threads;
	long int diff = time_int[0];
	double time = (double) diff / (double) CLOCKS_PER_SEC;
	printf("\nTime integer operations = %f seconds", time);
	printf("\nGIOPS = %f\n", n_operations/(time * pow(10,9)));

	diff = time_float[0];
	time = (double) diff / (double) CLOCKS_PER_SEC;
	printf("\nTime float operations = %f seconds", time);
	printf("\nFLOPS = %f\n", n_operations/(time * pow(10,9)));
}
