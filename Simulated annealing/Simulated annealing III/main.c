///
/// Created by Fabio Vitor Noronha at 13-May-2017.
///
/// Simulated Annealing algorithm
/// that minimize the function:
///     f(x) = 500 - 20x1 - 26x2 - 4x1x2 + 4x1^2 + 3x2^2
///

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define RANDOM_PARAM 4
#define FUNCTION_MIN  0.0
#define FUNCTION_MAX 10.0
#define COOLING_TAX 0.5
#define MAX_ITERATIONS 2
#define TEMPERATURE_CONST 1
#define CONVERGENCE_TEMPERATURE 1.0
#define TOTAL_COOLING_CICLES

double evaluate_function(double x1, double x2);
double new_random(double min, double max);

int main()
{
    srand(time(NULL));
    int iteration;
    double TEMPERATURE;
    double pre_total = 0;
    double *x, *new_x;
    double x_value, new_x_value, delta;
    x = (double *) malloc(sizeof(double) * 2);
    new_x = (double *) malloc(sizeof(double) * 2);
    for(iteration = 0; iteration < RANDOM_PARAM; iteration++)
        pre_total += evaluate_function(new_random(FUNCTION_MIN, FUNCTION_MAX), new_random(FUNCTION_MIN, FUNCTION_MAX));
    TEMPERATURE = pre_total / RANDOM_PARAM;
    x[0] = new_random(FUNCTION_MIN, FUNCTION_MAX);
    x[1] = new_random(FUNCTION_MIN, FUNCTION_MAX);
    x_value = evaluate_function(x[0], x[1]);
    while(TEMPERATURE > CONVERGENCE_TEMPERATURE)
    {
        for(iteration = 1; iteration < MAX_ITERATIONS; iteration++)
        {
            new_x[0] = x[0] + new_random(FUNCTION_MIN, FUNCTION_MAX) * (x[1] - x[0]);
            new_x[1] = x[0] + new_random(FUNCTION_MIN, FUNCTION_MAX) * (x[1] - x[0]);
            new_x_value = evaluate_function(new_x[0], new_x[1]);
            delta = new_x_value - x_value;
            if(delta < 0 || new_random(0.0, 1.0) < exp((0 - delta) / (TEMPERATURE_CONST * TEMPERATURE)))
            {
                x[0] = new_x[0];
                x[1] = new_x[1];
            }
        }
        TEMPERATURE *= COOLING_TAX;
    }
    printf("\n\nX = {%.3lf, %.3lf}\nF(X) = %.3lf\n\n", x[0], x[1], evaluate_function(x[0], x[1]));
    return 0;
}

double evaluate_function(double x1, double x2)
{
    return 500 - (20 * x1) - (26 * x2) - (4 * x1 * x2) + (4 * pow(x1, 2)) + (3 * pow(x2, 2));
}

double new_random(double min, double max)
{
    return ((rand() + 0.0) / (RAND_MAX + 0.0)) * (max - min) + min;
}
