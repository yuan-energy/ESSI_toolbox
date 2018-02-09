#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include "H5Cpp.h"
using namespace H5;

namespace h5cxx{



  int copy_file( std::string const& h5source,  std::string const& h5dest)
  {
    {      
      remove( h5dest.c_str() ) ; 

      std::ifstream  src(h5source, std::ios::binary);
      std::ofstream  dst(h5dest,   std::ios::binary);

      dst << src.rdbuf();
    }
    return 1; 
  }





  bool dataset_exist( std::string const& h5dest,  std::string const& h5dataset_path)
  {
      H5File file( h5dest, H5F_ACC_RDONLY );
      try {
        Exception::dontPrint();
        auto dataset = new DataSet( file.openDataSet( h5dataset_path));
        delete dataset ; 
      }
      catch( FileIException not_found_error ) {
          file.close();
          return false;
      }
      file.close();
      return true;
  }






  std::vector<std::vector<float>> extract_data( std::string const& h5source,  std::string const& h5dataset_path )
  {
    {
      H5File file( h5source, H5F_ACC_RDONLY );
      DataSet dataset = file.openDataSet( h5dataset_path );
      DataSpace dataspace = dataset.getSpace();
      hsize_t dims_out[2];
      dataspace.getSimpleExtentDims( dims_out, NULL);

      /*************************** BEGIN  *******************************/
      size_t rows = dims_out[0];
      size_t cols = dims_out[1];
    /* Allocate memory for new integer array[row][col]. First
       allocate the memory for the top-level array (rows).  Make
       sure you use the sizeof a *pointer* to your data type. */

      // data_out = (float**) malloc(rows*sizeof(float*));
      float**  data_out = (float**) malloc(rows*sizeof(float*));

    /* Allocate a contiguous chunk of memory for the array data values.  
       Use the sizeof the data type. */

        data_out[0] = (float*)malloc( cols*rows*sizeof(float) );

    /* Set the pointers in the top-level (row) array to the
       correct memory locations in the data value chunk. */

        for (size_t i=1; i < rows; i++) data_out[i] = data_out[0]+i*cols;

        /* Initialize data_out array to 0 */
        for (size_t j = 0; j < dims_out[0]; j++) {
            for (size_t i = 0; i < dims_out[1]; i++) {
                    data_out[j][i] = 0;
            }
        }
    /************************* END *************************************/

      dataset.read( &data_out[0][0] , PredType::NATIVE_FLOAT) ; 

      std::vector<std::vector<float>> ans(rows, std::vector<float>(cols, 0));
      for (size_t i = 0; i < rows; ++i){
        for (size_t j = 0; j < cols; ++j){
          ans[i][j] = data_out[i][j] ; 
        }
      }

      free(data_out[0]);
      free(data_out);
      return ans;
    }
  }






  int assign_data( 
        std::string const& h5dest,  
        std::string const& h5dataset_path, 
        std::vector<std::vector<float>> const& vals 
        )
  {
    {
        H5File file( h5dest, H5F_ACC_RDWR );
        DataSet dataset = file.openDataSet( h5dataset_path );

        /*************************** BEGIN  *******************************/
        int rows = vals.size() ;
        int cols = vals[0].size() ;
      /* Allocate memory for new integer array[row][col]. First
         allocate the memory for the top-level array (rows).  Make
         sure you use the sizeof a *pointer* to your data type. */

        // data_out = (float**) malloc(rows*sizeof(float*));
        float**  data_in = (float**) malloc(rows*sizeof(float*));

      /* Allocate a contiguous chunk of memory for the array data values.  
         Use the sizeof the data type. */

          data_in[0] = (float*)malloc( cols*rows*sizeof(float) );

      /* Set the pointers in the top-level (row) array to the
         correct memory locations in the data value chunk. */

          for (int i=1; i < rows; i++) data_in[i] = data_in[0]+i*cols;

          /* Initialize data_in array to 0 */
          for (int j = 0; j < rows; j++) {
              for (int i = 0; i < cols; i++) {
                      data_in[j][i] = vals[j][i] ;
              }
          }
      /************************* END *************************************/

        dataset.write( &data_in[0][0] , PredType::NATIVE_FLOAT) ; 

        free(data_in[0]);
        free(data_in);
      }
      return 0;

  }






  std::vector<std::vector<float>> mat_mul_scalar(
                    std::vector<std::vector<float>>  mat, 
                    float factor
                    )
  {
    if(mat.empty()){
      std::cerr << " ERROR in h5cxx::mul_mat(), -- argument mat is empty() " << std::endl ; 
    }
    for(size_t i = 0 ; i< mat.size() ; i++ ){
      for( size_t j = 0; j < mat[0].size() ; j++ ){
        mat[i][j] *= factor;
      }
    }
    return mat; 
  }




  std::vector<std::vector<float>> mat_add_mat(
                  std::vector<std::vector<float>>  matA, 
                  std::vector<std::vector<float>> const& matB
                  )
  {
    if(matA.empty() || matB.empty()){
      std::cerr << " ERROR in h5cxx::mul_mat(), -- argument mat is empty() " << std::endl ; 
    }
    for(size_t i = 0 ; i< matA.size() ; i++ ){
      for( size_t j = 0; j < matA[0].size() ; j++ ){
        matA[i][j] += matB[i][j] ;
      }
    }
    return matA ; 
  }





  int combine_files(std::vector<std::string> const& filenames, 
                   std::vector<float> const& factors, 
                   std::vector<std::string> const& groups, 
                   std::string const& out_file
                   )
  {
    if (filenames.empty()){
      std::cerr<<" ERROR in h5cxx::combine_files() -- argument filenames is empty!" <<std::endl;
      return -1;
    }
    h5cxx::copy_file(filenames[0] , out_file);

    for(auto group: groups){
      if( dataset_exist( out_file, group ) ){
        auto raw_data = h5cxx::extract_data( filenames[0], group );
        auto new_data = mat_mul_scalar(raw_data, factors[0] );
        for(size_t i = 1; i < factors.size(); i++ ){
          raw_data = h5cxx::extract_data( filenames[i], group );
          new_data = mat_add_mat(new_data, mat_mul_scalar(raw_data, factors[i]));
        }
        assign_data(out_file, group, new_data);
      }
    }
    return 1;
  }




} // end h5cxx namespace