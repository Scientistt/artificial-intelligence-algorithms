#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define RANGE 257
#define MY_END_OF_FILE 256
#define BYTE 8

typedef struct huffmanTree
{
    struct huffmanTree *left;
    struct huffmanTree *right;
    int letter;
    int freq;
} huffmanTree;


void pause();

void Encode(FILE *in, FILE *data, FILE *out);

void Decode(FILE *in, FILE *data, FILE *out);
