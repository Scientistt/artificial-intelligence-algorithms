#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i;
    double value;

    for(i = 0 - 11; i <= 11; i++)
    {
        value = (1.0 / 10000) * (i + 10) * (i + 6) * (i * 5) * (i + 1) * (i - 7) * (i - 10);
        printf("%d = %lf\n", i, value);
    }

    return 0;
}
