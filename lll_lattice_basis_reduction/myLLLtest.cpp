// build in NTL src/ folder
//g++ -I../include -I.  -g -O2 -std=c++11 -pthread -march=native  -o myLLLtest myLLLtest.cpp ntl.a  -lgmp    -lm #LSTAT


#include <NTL/LLL.h>

NTL_CLIENT

int main()
{
    mat_ZZ B;

    cin >> B;

    ZZ d;

    LLL(d, B, 90, 100);

    cout << "det = " << d << endl;
    cout << "B = " << B << endl;
    cout << "Finished" << endl;
}
