#ifndef _GPUOPS_H_
#define _GPUOPS_H_

typedef struct TestResult {
	double int_times[3];
	double float_times[3];
} TestResult;

extern TestResult gpu_test();

#endif
