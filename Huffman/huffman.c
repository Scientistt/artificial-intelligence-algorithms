#include "huffman.h"

void pause()
{
    printf("Press ENTER to continue...");
    getchar();
}


int CmpTrees(const void *a, const void *b)
{
    const huffmanTree **x = (const huffmanTree **) a, **y = (const huffmanTree **) b;
    if((*x)->freq == (*y)->freq) return 0;
    else return ((*x)->freq < (*y)->freq) ? 1 : -1;
}


char *Concat(char *prefix, char letter)
{
    char *result = (char *)malloc(strlen(prefix) + 2);
    sprintf(result, "%s%c", prefix, letter);
    return result;
}

void Error(const char *msg)
{
    fprintf(stderr, "Error: %s\n", msg);
    exit(1);
}

huffmanTree *BuildTree(int frequencies[])
{
    int i, len = 0;
    huffmanTree *queue[RANGE];

    for(i = 0; i < RANGE; i++)
    {
        if(frequencies[i])
        {
            huffmanTree *toadd = (huffmanTree *)calloc(1, sizeof(huffmanTree));
            toadd->letter = i;
            toadd->freq = frequencies[i];

            queue[len++] = toadd;
        }
    }

    while(len > 1)
    {
        huffmanTree *toadd = (huffmanTree *)malloc(sizeof(huffmanTree));

        qsort(queue, len, sizeof(huffmanTree *), CmpTrees);

        toadd->left = queue[--len];
        toadd->right = queue[--len];
        toadd->freq = toadd->left->freq + toadd->right->freq;

        queue[len++] = toadd; /* insert back in the queue */
    }

    return queue[0];
}

void FreeTree(huffmanTree *tree)
{
    if(tree)
    {
        FreeTree(tree->left);
        FreeTree(tree->right);
        free(tree);
    }
}

void TraverseTree(huffmanTree *tree, char **table, char *prefix)
{
    if(!tree->left && !tree->right) table[tree->letter] = prefix;
    else
    {
        if(tree->left) TraverseTree(tree->left, table, Concat(prefix, '0'));
        if(tree-> right) TraverseTree(tree->right, table, Concat(prefix, '1'));
        free(prefix);
    }
}

char **BuildTable(int frequencies[])
{
    static char *table[RANGE];
    char *prefix = (char *)calloc(1, sizeof(char));
    huffmanTree *tree = BuildTree(frequencies);
    TraverseTree(tree, table, prefix);
    FreeTree(tree);

    return table;
}

void FreeTable(char *table[])
{
    int i;
    for(i = 0; i < RANGE; i++) if(table[i]) free(table[i]);
}

void WriteHeader(FILE *out, int frequencies[])
{
    int i, count = 0;

    for(i = 0; i < RANGE; i++) if(frequencies[i]) count++;
    fprintf(out, "%d\n", count);

    for(i = 0; i < RANGE; i++)
        if(frequencies[i]) fprintf(out, "%d %d\n", i, frequencies[i]);
}

int *ReadHeader(FILE *in)
{
    static int frequencies[RANGE];
    int i, count, letter, freq;

    if(fscanf(in, "%d", &count) != 1) Error("\n\tWe couldn't decompress the specified file\n\tThe data File may be corrupted! ;(");

    for(i = 0; i < count; i++)
    {
        if((fscanf(in, "%d %d", &letter, &freq) != 2)
                || letter < 0 || letter >= RANGE) Error("\n\tWe couldn't decompress the specified file\n\tThe data File may be corrupted! ;");

        frequencies[letter] = freq;
    }
    fgetc(in);

    return frequencies;
}


void WriteBits(const char *encoding, FILE *out)
{
    static int bits = 0, bitcount = 0;

    while(*encoding)
    {
        bits = bits * 2 + *encoding - '0';
        bitcount++;

        if(bitcount == BYTE)
        {
            fputc(bits, out);
            bits = 0;
            bitcount = 0;
        }
        encoding++;
    }
}

int ReadBit(FILE *in)
{
    static int bits = 0, bitcount = 0;
    int nextbit;
    if(bitcount == 0)
    {
        bits = fgetc(in);
        bitcount = (1 << (BYTE - 1));
    }
    nextbit = bits / bitcount;
    bits %= bitcount;
    bitcount /= 2;
    return nextbit;
}

int DecodeChar(FILE *in, huffmanTree *tree)
{
    while(tree->left || tree->right)
    {
        if(ReadBit(in)) tree = tree->right;
        else tree = tree->left;

        if(!tree) Error("invalid input file.");
    }
    return tree->letter;
}


void Decode(FILE *in, FILE *data, FILE *out)
{
    int *frequencies, c;
    huffmanTree *tree;
    frequencies = ReadHeader(data);
    tree = BuildTree(frequencies);
    while((c = DecodeChar(in, tree)) != MY_END_OF_FILE)
        fputc(c, out);
    FreeTree(tree);
}

void Encode(FILE *in, FILE *data, FILE *out)
{
    int c, frequencies[RANGE] = { 0 };
    char **table;
    while((c = fgetc(in)) != EOF) frequencies[c]++;
    frequencies[MY_END_OF_FILE] = 1;
    rewind(in);
    table = BuildTable(frequencies);
    WriteHeader(data, frequencies);
    while((c = fgetc(in)) != EOF)
        WriteBits(table[c], out);
    WriteBits(table[MY_END_OF_FILE], out);
    WriteBits("0000000", out);
    FreeTable(table);
}
