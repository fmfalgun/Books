// Exercise 2.20: What does the following program do?
// 	int i = 42;
// 	int *p1 = &i;
//	*p1 = *p1 * *p1;

#include <iostream>

int main(){

	int i =42;
	int *p1 = &i;
	std::cout << *p1 << " " << p1 << " " << i << std::endl; 
	*p1 = *p1 * *p1;
	std::cout << *p1 << " " << p1 << " " << i << std::endl; 

	return 0;
}	
// My Expected: saves value of 42*42 in i
