#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int * makeList(int size);
void fillList(int size, int ** vector);

int main()
{
    srand(time(NULL));
    //int randomAmmount = rand() % 5 * 2;
    int randomAmmount = 32;
    int i, j, currentSize = randomAmmount, index = 0;
    int * vector = makeList(randomAmmount), current, past;
    fillList(randomAmmount, &vector);



    current = vector;
    while(currentSize > 1)
    {
        i = 0;
        j = 1;
        index = 0;
        past = current;
        currentSize += currentSize % 2;
        currentSize /= 2;
        current = makeList(currentSize);

        current[index++] = past[i] > past[j] ? past[j] : past[i];
    }


    return 0;
}

int * makeList(int size)
{
    int * vector = (int) malloc(sizeof(int) * size);
    return vector == NULL ? NULL : vector;
}

void fillList(int size, int ** vector)
{
    srand(time(NULL));
    int i;
    for(i = 0; i < size; i++)
        *(*vector + i) = rand();
}
