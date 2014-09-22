#include "gpuops.h"
#include <stdio.h>
#include <time.h>

#define N 1000
#define N_TESTS 1 

const float CONST_FLOAT = 1.7;

__global__ void add_int(int *a, int *b, int *c ) {
	int tid = blockIdx.x;
	if(tid < N){
		c[tid] = a[tid] + b[tid];
	}
}

//TODO float operations
__global__ void add_float(float *a, float *b, float *c ) {
        int tid = blockIdx.x;
        if(tid < N){
                c[tid] = a[tid] + b[tid];
        }
}

//TODO read operations
__global__ void read_data() {
}

//TODO write operations
__global__ void write_data() {
}

void speed_test_int(int grids, int blocks){
	int a[N], b[N], c[N];
	int *dev_a, *dev_b, *dev_c;
	cudaMalloc( (void**)&dev_a, N * sizeof(int) );
	cudaMalloc( (void**)&dev_b, N * sizeof(int) );
	cudaMalloc( (void**)&dev_c, N * sizeof(int) );

	for( int i=0; i <N; i++) {
		a[i] = 1;
		b[i] = i;
	}
	cudaMemcpy( dev_a, a, N * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy( dev_b, b, N * sizeof(int), cudaMemcpyHostToDevice);
	
	//TODO clock_t start = clock(), diff;

	add_int<<<N,1>>>(dev_a, dev_b, dev_c);
	//add_int<<grids,blocks,1>>(dev_a, dev_b, dev_c);

	//TODO diff = clock() - start;
        double time = 0.0; //TODO (double) diff / (double) CLOCKS_PER_SEC;

	cudaMemcpy( c, dev_c, N * sizeof(int), cudaMemcpyDeviceToHost);
	
	printf("\nTime spent: %d\n", time);
	for(int i=(N - 3); i<N; i++) {
		printf("%d + %d = %d\n", a[i], b[i], c[i] );
	}

	cudaFree( dev_a );
	cudaFree( dev_b );
	cudaFree( dev_c );

}

void speed_test_float(int grids, int blocks){
        float a[N], b[N], c[N];
        float *dev_a, *dev_b, *dev_c;
        cudaMalloc( (void**)&dev_a, N * sizeof(float) );
        cudaMalloc( (void**)&dev_b, N * sizeof(float) );
        cudaMalloc( (void**)&dev_c, N * sizeof(float) );

        for( int i=0; i <N; i++) {
                a[i] = CONST_FLOAT;
                b[i] = (float) i;
        }
        cudaMemcpy( dev_a, a, N * sizeof(float), cudaMemcpyHostToDevice);
        cudaMemcpy( dev_b, b, N * sizeof(float), cudaMemcpyHostToDevice);

        //TODO clock_t start = clock(), diff;

        add_float<<<N,1>>>(dev_a, dev_b, dev_c);
        //add_float<<grids,blocks,1>>(dev_a, dev_b, dev_c);

        //TODO diff = clock() - start;
        double time = 0.0; //TODO (double) diff / (double) CLOCKS_PER_SEC;

        cudaMemcpy( c, dev_c, N * sizeof(float), cudaMemcpyDeviceToHost);

        printf("\nTime spent: %d\n", time);
        for(int i=(N - 3); i<N; i++) {
                printf("%f + %f = %f\n", a[i], b[i], c[i] );
        }

        cudaFree( dev_a );
        cudaFree( dev_b );
        cudaFree( dev_c );
}


TestResult gpu_test() {
	TestResult result;
	int n_blocks = 1, n_grids = 1; //get actual number of cores here
	
	for(int i = 0; i < N_TESTS; i++) {
		speed_test_int(n_grids, n_blocks);
		result.int_times[i] = 0;
	}
	for(int i = 0; i < N_TESTS; i++) {
		//speed_test_float(n_grids, n_blocks);
                result.float_times[i] = 0;
        }

	//bandwidth test
	return result;
}

