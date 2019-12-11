#ifndef cudavectors_h
#define cudavectors_h

namespace cudavectors {

  // HINT
  // the two strucs following are done
  // to be bit-wise compatible with how the root objects are stored
  // => assume the input is in this format, even though the actual
  // input are objects of a different type/class
  struct CylindricalVector {
    float rho;
    float eta;
    float phi;
  };

  struct CartesianVector {
    float x;
    float y;
    float z;
  };

  void convertWrapper(CylindricalVector const* cylindrical, CartesianVector* cartesian, size_t size);

  //  const unsigned int gridSize  =1;
  //  const unsigned int blockSize =8;

}  // namespace cudavectors

#endif  // cudavectors_h
