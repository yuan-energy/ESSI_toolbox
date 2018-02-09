#include "h5cxx.hpp"



int main (void)
{

  // User Input:
  std::vector<std::string> files = {"case_in1.feioutput", "case_in2.feioutput"};
  std::vector<float> facs = {1.2,1.5};
  std::string out_file = "case_cpp_combine.h5.feioutput";


  // Real-ESSI groups, which requires scales and combinations.
  std::vector<std::string> groups = {
    "/Model/Elements/Gauss_Outputs",
    "/Model/Elements/Element_Outputs",
    "/Model/Elements/Fibers/Fiber_Outputs",
    "/Model/Nodes/Generalized_Displacements",
    "/Model/Nodes/Generalized_Accelerations"
  };



  h5cxx::combine_files(files, facs, groups, out_file);

  return 0; 
}