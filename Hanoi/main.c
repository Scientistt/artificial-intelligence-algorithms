#include <stdio.h>
#include <stdlib.h>

int interestingDisk, movementCounter = 0, numberOfDisks;

void hanoi(int disk, char stemA, char stemB, char stemC);

int main(void)
{
    fprintf(stdout, "Numero de discos: ");
    scanf("%d", &numberOfDisks);
    setbuf(stdin, NULL);

    fprintf(stdout, "Disco que você quer acompanhar: ");
    scanf("%d", &interestingDisk);
    setbuf(stdin, NULL);

    hanoi(numberOfDisks, 'A', 'B', 'C');
    return 0;
}

void hanoi(int disk, char stemA, char stemB, char stemC)
{
    if (disk == 1)
    {
        movementCounter++;
        if(disk == interestingDisk)
            fprintf(stdout, " %02d ", movementCounter);
    }
    else
    {
        hanoi(disk - 1, stemA, stemC, stemB);

        movementCounter++;
        if(disk == interestingDisk)
            fprintf(stdout, " %02d ", movementCounter);

        hanoi(disk - 1, stemC, stemB, stemA);
    }
}
