///
/// Created by Fabio Vitor Noronha at 13-May-2017.
///
/// Simulated Annealing algorithm
/// that minimize the function:
///     f(x) = (1 / 10000) * (x + 10) * (x + 6) * (x + 5) * (x + 1) * (x - 7) * (x - 10)
///

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define FUNCTION_MIN -11
#define FUNCTION_MAX  11
#define JUMP_MIN -1
#define JUMP_MAX  1
#define TEMPERATURE 10.0
#define COOLING_TAX 0.95
#define MAX_ITERATIONS 50
#define TOTAL_COOLING_CICLES 9

double get_x_neighbor(double x);
double evaluate_function(double x);

int main()
{
    int i;
    double start_x, start_energy;
    double current_x, current_energy, current_temperature;
    double potentially_new_x, potentially_new_energy;
    int iteration_counter, cooling_cicles_counter;
    srand(time(NULL));
    printf("Simulates Annealing Algorithm\n\nTemperture: %.2f*C\nCooling tax: %.2f\nIterations per temperature: %d\nCooling cicles: %d\n--- Resuults ---\n", TEMPERATURE,
           COOLING_TAX, MAX_ITERATIONS, TOTAL_COOLING_CICLES);

    current_x = (rand() + 0.0) / RAND_MAX * (FUNCTION_MAX - FUNCTION_MIN) + FUNCTION_MIN;
    current_energy = evaluate_function(current_x);
    start_x = current_x;
    start_energy = current_energy;
    cooling_cicles_counter = 0;
    current_temperature = TEMPERATURE;
    while(cooling_cicles_counter <= TOTAL_COOLING_CICLES)
    {
        while(iteration_counter <= MAX_ITERATIONS)
        {
            iteration_counter++;
            potentially_new_x = get_x_neighbor(current_x);
            potentially_new_energy = evaluate_function(potentially_new_x);
            if(potentially_new_energy < current_energy || (rand() + 0.0 / RAND_MAX) < exp((current_energy - potentially_new_energy) / current_temperature))
            {
                current_x = potentially_new_x;
                current_energy = potentially_new_energy;
            }
        }
        current_temperature *= COOLING_TAX;
        iteration_counter = 0;
        cooling_cicles_counter++;
    }

    printf("Start x value: %.10lf\t\tStart f(x) = %.10lf\n", start_x, start_energy);
    printf("Final x value: %.10lf\t\tFinal f(x) = %.10lf", current_x, current_energy);
    return 0;
}

double evaluate_function(double x)
{
    return 0.0001 * (x + 10) * (x + 6) * (x + 5) * (x + 1) * (x - 7) * (x - 10);
}

double get_x_neighbor(double x)
{
    return x + (rand() + 0.0) / RAND_MAX * (JUMP_MAX - JUMP_MIN) + JUMP_MIN;
}
