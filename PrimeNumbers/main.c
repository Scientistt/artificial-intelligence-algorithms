///
/// @author Fabio Vitor
/// @version 1.0 12/04/2017
///

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/// Function that checks if a number is prime.
/// @param n Is the number that'll be checked;
/// @return 1 if the number is prime or 0 if it isn't;
int is_prime(int n);

/// The main function.
int main()
{
    FILE * file = fopen("dat.txt", "r");        ///> File where are the numbers that'll be tested.
    int i, n, col_num = 5;                      ///> @param col_num Is the number of columns in the printed screen.
    if(file != NULL)                            ///> in case of the file could not be open.
        for(i = 1; i < 10001; i++)              ///> the first 10,000 prime numbers will be tested.
        {
            fscanf(file, "%d", &n);             ///> Reading from the file each number.
            printf("%06d is prime: %s%s", n,
                is_prime(n) ? "TRUE" : "****",  ///> if the number is prime it'll be tagged as TRUE, if it's not, ****.
                i % col_num ? "\t" : " \n");
        }
    return 0;                                   ///> End of Main function.
}

int is_prime(int n)                             ///> Implementation of the is_prime function.
{
    if(!(n % 2))                                ///> if it is a even number.
        return n == 2;                          ///> 2 is the only even number that is prime.
    double i;
    for(i = 3.0; i < n / 2.0; i += 2.0)         ///> starting at 3 to n / 2 and incrementing by 2 each iteration;
        if(!((n / i) - floor(n / i)))           ///> If it is divisible it's not prime.
            return 0;                           ///> Returning FALSE (0);
    return 1;                                   ///> If the loop ends, the number is prime. Returning TRUE (1).
}
