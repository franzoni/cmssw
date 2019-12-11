// system include files
#include <cmath>
#include <memory>
#include <vector>

// CMSSW include files
#include "DataFormats/Math/interface/Vector3D.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "HeterogeneousCore/CUDAUtilities/interface/cudaCheck.h"

#include "cudavectors.h"

class ConvertToCartesianVectorsCUDA : public edm::stream::EDProducer<> {
public:
  explicit ConvertToCartesianVectorsCUDA(const edm::ParameterSet&);
  ~ConvertToCartesianVectorsCUDA() = default;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  using CartesianVectors = std::vector<math::XYZVectorF>;
  using CylindricalVectors = std::vector<math::RhoEtaPhiVectorF>;

  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<CylindricalVectors> input_;
  edm::EDPutTokenT<CartesianVectors> output_;
};

ConvertToCartesianVectorsCUDA::ConvertToCartesianVectorsCUDA(const edm::ParameterSet& config)
    : input_(consumes<CylindricalVectors>(config.getParameter<edm::InputTag>("input"))) {
  output_ = produces<CartesianVectors>();
}

void ConvertToCartesianVectorsCUDA::produce(edm::Event& event, const edm::EventSetup& setup) {
  auto const& input = event.get(input_);
  auto elements = input.size();

  // https://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique
  // https://en.cppreference.com/w/cpp/memory/unique_ptr
  auto product = std::make_unique<CartesianVectors>(elements);

  // allocate memory on the GPU for the cylindrical and cartesian vectors
  // fill here ...
  cudavectors::CylindricalVector* gpu_input;
  cudavectors::CartesianVector* gpu_product;
  cudaCheck(cudaMalloc(&gpu_input,   sizeof(cudavectors::CylindricalVector) * elements));
  cudaCheck(cudaMalloc(&gpu_product, sizeof(cudavectors::CartesianVector) * elements));
  
  // copy the input data to the GPU
  // fill here ...
  cudaCheck(cudaMemcpy(gpu_input, input.data(), sizeof(cudavectors::CylindricalVector) * elements, cudaMemcpyHostToDevice));

  // convert the vectors from cylindrical to cartesian coordinates, on the GPU
  // fill here ...
  cudavectors::convertWrapper(gpu_input, gpu_product, elements);

  // copy the result from the GPU
  // fill here ...
  cudaCheck(cudaMemcpy(product->data(), gpu_product, sizeof(cudavectors::CartesianVector) * elements, cudaMemcpyDeviceToHost));


  // free the GPU memory
  // fill here ...
  cudaCheck(cudaFree(gpu_input));
  cudaCheck(cudaFree(gpu_product));

  event.put(output_, std::move(product));
}

void ConvertToCartesianVectorsCUDA::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("input", edm::InputTag("cylindricalVectors"));
  descriptions.addWithDefaultLabel(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(ConvertToCartesianVectorsCUDA);
