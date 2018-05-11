/*
*/

#include "defs.h"
#include "fplll.h"
#include "nr/matrix.h"


template <class ZT> int lll(fplll::ZZ_mat<ZT> &b)
{
  // Stupid initialization of u and u_inv to be not empty.
  fplll::ZZ_mat<ZT> u(1, 1), u_inv(1, 1);
  int status, flags = 0;

  double delta = 0.99;
  double eta = 0.51;
  fplll::LLLMethod method = 0;
  fplll::FloatType float_type = 0;
  int precision = 0;

  status = lll_reduction(b, delta, eta, method, float_type, precision, flags);

  std::cout << b << std::endl;

  if (status != 0)
  {
    std::cerr << "Failure: " << get_red_status_str(status) << std::endl;
  }
  return status;
}


int main(int argc, char **argv)
{
  std::istream *is;
  fplll::ZZ_mat<ZT> m;
  is = new std::ifstream("test");
  *is >> m;
  if (!*is)
      ABORT_MSG("invalid input");
  delete is;


  int result = 0;
  result = lll(m);


  return result;
}
