// system include files
#include <cmath>

// CUDA include files
#include <cuda_runtime.h>

// CMSSW include files
#include "HeterogeneousCore/CUDAUtilities/interface/cudaCheck.h"
#include "cudavectors.h"

namespace cudavectors {



	  // In CUDA function type qualifiers __device__ and __host__ can be used together in which case the function is compiled for both the host and the device.
	  // https://stackoverflow.com/questions/33218522/cuda-host-device-variables
	  // https://www.geeksforgeeks.org/understanding-constexper-specifier-in-c/ 

  __host__ __device__ inline void convert(CylindricalVector const& cylindrical, CartesianVector & cartesian) {
    // fill here ...
    cartesian.x = cylindrical.rho * std::cos(cylindrical.phi);
    cartesian.y = cylindrical.rho * std::sin(cylindrical.phi);
    cartesian.z = cylindrical.rho * std::sinh(cylindrical.eta);
  }


  __global__ void convertKernel(CylindricalVector const* cylindrical, CartesianVector* cartesian, size_t size) {
    // fill here ...
    auto firstElement = threadIdx.x + blockIdx.x * blockDim.x;
    auto gridSize = blockDim.x * gridDim.x;

    for (size_t i = firstElement; i < size; i += gridSize) {
      convert(cylindrical[i], cartesian[i]);
    }// for loop
  }// funct



  void convertWrapper(CylindricalVector const* cylindrical, CartesianVector* cartesian, size_t size) {
    // fill here ...
    // grid contains blocks, each of which holds threads
    // blocks share the fast elements of memory
    // number of blocks of "grid" is basically the same thing
    auto blockSize = 512;                                // somewhat arbitrary
    auto gridSize = (size + blockSize - 1) / blockSize;  // round up to cover the sample size; this is how MANY BLOCKS we want

    convertKernel<<<gridSize, blockSize>>>(cylindrical, cartesian, size);
    cudaCheck(cudaGetLastError());

  }

}  // namespace cudavectors
