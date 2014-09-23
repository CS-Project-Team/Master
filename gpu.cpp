#include <time.h>
#include <stdio.h>
#include <math.h>
#include <pthread.h>
#include "gpuops.h"

const long unsigned int N = 1000;
const int N_TESTS = 1;
const float CONST_FLOAT = 0.7;

//Stores the results for each of the tests
double time_int[] = {0.0, 0.0, 0.0};
double time_float[] = {0.0, 0.0, 0.0};

float average(double values[3]){
        double sum = 0;
        for(int i = 0; i < N_TESTS; i++){
                sum += values[i];
        }
        return sum/N_TESTS;
}

float stand_deviation(double values[3], float average ){
        float variance = 0.00;
        for(int i =0; i < N_TESTS; i++){
                variance += (pow((average - values[i]), 2));
        }
        variance = variance / N_TESTS;
        return sqrt( variance );
}

double get_gops(int n_threads, double time) {
        return (pow(N,3)/pow(10,9))*(n_threads/time);
}


int main(int argc, char *argv[]) {
        TestResult result;
	for(int i=0; i<N_TESTS; i++) {
                printf("\n---- Running test #%d ----\n", i+1);
                result = gpu_test();
		printf("RESULT: time = %f", result.int_times[0]);
                //print_results(n_threads, i);
        }

        float avg_int = average(time_int);
        float avg_float = average(time_float);
        float sd_int = stand_deviation(time_int, avg_int);
        float sd_float = stand_deviation(time_float, avg_float);

        printf("\n========== SUMMARY OF GPU PERFORMANCE ============");
        printf("\nTests                                    : %d", N_TESTS);
        //printf("\nNumber of threads                        : %d", n_threads);
        printf("\nAverage time for integer operations      : %fs", avg_int);
        printf("\nStandard deviation for integer operations: %fs", sd_int);
        //printf("\nAverage integer operations per second    : %f GIOPS", get_gops(n_threads, avg_int));
        printf("\nAverage time for float operations        : %fs", avg_float);
        printf("\nStandard deviation for float operations  : %fs", sd_float);
        //printf("\nAverage float operations per second      : %f GFLOPS", get_gops(n_threads, avg_float));
        printf("\n====================================================\n\n");
}

