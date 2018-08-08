#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "huffman.h"

int main(int number, char *things[])
{
    FILE *inputFile, *outputFile, *dataFile;
    char inputFileName[51], dataFileName[51];
    int option;

    while(1)
    {
        system("clear");
        fprintf(stdout, "\n\t\tMain Huffman\n\n\t1 - Compress a specified file\n\t2 - Decompress a specified file\n\t0 - Exit program\n\n\tWhat would you like to do now?\n\t>>> ");
        scanf("%d", &option);
        setbuf(stdin, NULL);

        switch(option)
        {

        case 1:
            printf("\tEnter the file name you want to COMPRESS: ");
            scanf("%[^\n]s", inputFileName);
            setbuf(stdin, NULL);

            inputFile =fopen(inputFileName, "rb");
            strcpy(dataFileName, inputFileName);
            strcat(dataFileName, ".dat");
            dataFile = fopen(dataFileName, "wb");
            strcat(inputFileName, ".zip");
            outputFile = fopen(inputFileName, "wb");

            Encode(inputFile, dataFile, outputFile);

            fclose(inputFile);
            fclose(outputFile);
            fclose(dataFile);

            fprintf(stdout, "\n\n\tGenerated file: \"%s\"\n\n\t", inputFileName);
            break;

        case 2:
            printf("\tEnter the file name you want to DECOMPRESS: ");
            scanf("%[^\n]s", inputFileName);
            setbuf(stdin, NULL);

            printf("\tEnter the DATA FILE name: ");
            scanf("%[^\n]s", dataFileName);
            setbuf(stdin, NULL);

            inputFile =fopen(inputFileName, "rb");
            dataFile = fopen(dataFileName, "rb");
            strcat(inputFileName, ".txt");
            outputFile = fopen(inputFileName, "wb");

            Decode(inputFile, dataFile, outputFile);

            fclose(inputFile);
            fclose(outputFile);
            fclose(dataFile);

            fprintf(stdout, "\n\n\tGenerated file: \"%s\"\n\n\t", inputFileName);
            break;
        case 0:
            exit(1);
            break;

        default:
            printf("\tInvalid Option...\n\t");
        }
        pause();
    }
    return 0;
}
