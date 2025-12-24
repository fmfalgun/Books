// Exercise 2.21: Explain each of the following definitions. Indicate whether any are illegal and, if so, why.
// int i = 0;
// (a) double* dp = &i; (b) int *ip = i; (c) int *p = &i;

#include <iostream>

int main (){

	int i=0;
	//double* dp = &i;
	//int *ip = i;
	int *p = &i;

	//expected b to be illegal coz it is not forwarding the address of i, but value of i

	return 0;
}

//result: 


/*
┌──(fm㉿kali)-[~/Solo_leveling/Books/CPP_Primer/chapter2]
└─$ g++ ex2_21.cpp -o ex2_21
ex2_21.cpp: In function ‘int main()’:
ex2_21.cpp:10:22: error: cannot convert ‘int*’ to ‘double*’ in initialization
   10 |         double* dp = &i;
      |                      ^~
      |                      |
      |                      int*
ex2_21.cpp:11:19: error: invalid conversion from ‘int’ to ‘int*’ [-fpermissive]
   11 |         int *ip = i;
      |                   ^
      |                   |
      |                   int
ex2_21.cpp:11:19: note: possible fix: take the address with ‘&’
   11 |         int *ip = i;
      |                   ^
      |                   &

 */
