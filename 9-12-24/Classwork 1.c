#include <studio.h>

// write an algorithm to find the maximum element in an array.
// implement the algorithm in C/C++ code 

// upload your solution on Githib and share your link via Discord DM

//PSUEDOCODE

/*
    Finding maximum element in array

    DECLARE an array named arr
    ASSIGN a list of random numbers to array name arr
    DECLARE as integer and INITIALISE  variable i and j to 0
    WHILE i < length of arr DO
        IF j < arr element in position i DO
            ASSIGN value of that arr element to j
        END IF

    END WHILE

    PRINT result in j

*/

// C code


int main() {
    int arr[] = {21,5,7,55,27,93,22,5,90,1};
    int i =0,j = 0; // i is a counter  and j is the variable that hold the maximum
    int arraySize = sizeof(arr) / sizeof(arr[0]);

    while (i < arraySize) {
        if (j< arr[i]) {
            j = arr[i];
        }
          i++;
    }
    
      printf("The maximum element in the array is: %d\n ", j);
    return 0;
}