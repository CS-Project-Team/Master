#include "gpuops.h"
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <sys/resource.h>
//#include <windows.h>

#define N 1000
#define INT_M 2
#define N_TESTS 1 
double get_time()
{
	struct timeval t;
	struct timezone tzp;
	gettimeofday(&t, &tzp);
	return t.tv_sec + t.tv_usec*1e-6;
}

const float CONST_FLOAT = 1.7;

__global__
void saxpy(int n, float a, float *x, float *y, float *z)
{
  int i = blockIdx.x*blockDim.x + threadIdx.x;
  if (i < n) {
	y[i] = a*x[i] + y[i];//y=4
	z[i] = a*x[i] + z[i];//z=5
	z[i] = a*y[i] + z[i];//z=13
	y[i] = a*x[i] + z[i];//y=15
        y[i] = a*x[i] + y[i];//y=17
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

void speed_test_int(int n_blocks, int n_threads){
	int a[N], b[N], c[N];
	int *dev_a, *dev_b, *dev_c;
	cudaMalloc( (void**)&dev_a, N * sizeof(int) );
	cudaMalloc( (void**)&dev_b, N * sizeof(int) );
	cudaMalloc( (void**)&dev_c, N * sizeof(int) );

	for( int i=0; i <N; i++) {
		a[i] = 2;
		b[i] = 1;
	}
	cudaMemcpy( dev_a, a, N * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy( dev_b, b, N * sizeof(int), cudaMemcpyHostToDevice);
	
	//TODO clock_t start = clock(), diff;

	//add_int<<<n_blocks,n_threads>>>(dev_a, dev_b, dev_c, n_blocks, INT_M);
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

int ConvertSMVer2Cores(int major, int minor)
{
        // Defines for GPU Architecture types (using the SM version to determine the # of cores per SM
        typedef struct {
                int SM; // 0xMm (hexidecimal notation), M = SM Major version, and m = SM minor version
                int Cores;
        } sSMtoCores;

        sSMtoCores nGpuArchCoresPerSM[] =
        { { 0x10,  8 }, // Tesla Generation (SM 1.0) G80 class
          { 0x11,  8 }, // Tesla Generation (SM 1.1) G8x class
          { 0x12,  8 }, // Tesla Generation (SM 1.2) G9x class
          { 0x13,  8 }, // Tesla Generation (SM 1.3) GT200 class
          { 0x20, 32 }, // Fermi Generation (SM 2.0) GF100 class
          { 0x21, 48 }, // Fermi Generation (SM 2.1) GF10x class
          { 0x30, 192}, // Fermi Generation (SM 3.0) GK10x class
          {   -1, -1 }
        };

        int index = 0;
        while (nGpuArchCoresPerSM[index].SM != -1) {
                if (nGpuArchCoresPerSM[index].SM == ((major << 4) + minor) ) {
                        return nGpuArchCoresPerSM[index].Cores;
                }
                index++;
        }
        printf("MapSMtoCores SM %d.%d is undefined (please update to the latest SDK)!\n", major, minor);
        return -1;
}

TestResult gpu_test(){
  int Nz = 20 * (1 << 20);
  float *x, *y, *z, *d_x, *d_y, *d_z;
  x = (float*)malloc(Nz*sizeof(float));
  y = (float*)malloc(Nz*sizeof(float));
  z = (float*)malloc(Nz*sizeof(float));

  cudaMalloc(&d_x, Nz*sizeof(float)); 
  cudaMalloc(&d_y, Nz*sizeof(float));
  cudaMalloc(&d_z, Nz*sizeof(float));

  for (int i = 0; i < Nz; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
    z[i] = 3.0f;
  }

  cudaEvent_t start, stop;
  cudaEventCreate(&start);
  cudaEventCreate(&stop);

  cudaMemcpy(d_x, x, Nz*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(d_y, y, Nz*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(d_z, z, Nz*sizeof(float), cudaMemcpyHostToDevice);

  cudaEventRecord(start);

  printf("\nPerform SAXPY on %d elements\n", Nz);
  //saxpy<<<(Nz+511)/512, 512>>>(Nz, 2.0f, d_x, d_y);
  saxpy<<<(Nz+383)/384, 384>>>(Nz, 2.0f, d_x, d_y, d_z);

  cudaEventRecord(stop);

  cudaMemcpy(y, d_y, Nz*sizeof(float), cudaMemcpyDeviceToHost);
  cudaMemcpy(z, d_z, Nz*sizeof(float), cudaMemcpyDeviceToHost);

  cudaEventSynchronize(stop);
  float milliseconds = 0;
  cudaEventElapsedTime(&milliseconds, start, stop);

  float maxError_y = 0.0f;
  float maxError_z = 0.0f;
  for (int i = 0; i < Nz; i++) {
    maxError_y = max(maxError_y, abs(y[i]-17.0f));
    maxError_z = max(maxError_z, abs(z[i]-13.0f));
  }

  printf("\nMax error y: %fn", maxError_y);
  printf("\nMax error z: %fn", maxError_z);
  printf("\nTime elapsed: %f", milliseconds/1e6);
  printf("\nEffective Bandwidth (GB/s): %f\n", Nz*4*3/milliseconds/1e6);

	TestResult result;
        for(int i = 0; i < N_TESTS; i++) {
                //speed_test_float(n_grids, n_blocks);
                result.float_times[i] = 0;
		result.int_times[i] = 0;
        }

        //bandwidth test
        return result;
}

TestResult gpu_test_old() {
	TestResult result;
	double start, end;
	//number of blocks in a grid; number of threads in a block
	int n_blocks = 2, n_threads = 384; //384 get actual number of cores here
	
	int dev = 0;	
	cudaSetDevice(0);
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, dev);

	printf("\n  (%2d) Multiprocessors, (%3d) CUDA Cores/MP:     %d CUDA Cores\n",
               deviceProp.multiProcessorCount,
               ConvertSMVer2Cores(deviceProp.major, deviceProp.minor),
               ConvertSMVer2Cores(deviceProp.major, deviceProp.minor) * deviceProp.multiProcessorCount);	
	for(int i = 0; i < N_TESTS; i++) {
		start = get_time();
		speed_test_int(n_blocks, n_threads);
		end = get_time();
		result.int_times[i] = end - start;
	}
	for(int i = 0; i < N_TESTS; i++) {
		//speed_test_float(n_grids, n_blocks);
                result.float_times[i] = 0;
        }

	//bandwidth test
	return result;
}

