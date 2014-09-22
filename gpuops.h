#ifndef _GPUOPS_H_
#define _GPUOPS_H_

struct test_result {
	double int_times[];
	double float_times[];
};

extern void gpu_test();

#endif
