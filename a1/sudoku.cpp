#include <cassert>
#include <iostream>
#include <list>

using namespace std;

int eazy_puzzle[][9] = {
    {0, 6, 1, 0, 0, 0, 0, 5, 2},
    {8, 0, 0, 0, 0, 0, 0, 0, 1},
    {7, 0, 0, 5, 0, 0, 4, 0, 0},
    {9, 0, 3, 6, 0, 2, 0, 4, 7},
    {0, 0, 6, 7, 0, 1, 5, 0, 0},
    {5, 7, 0, 9, 0, 3, 2, 0, 6},
    {0, 0, 4, 0, 0, 9, 0, 0, 5},
    {1, 0, 0, 0, 0, 0, 0, 0, 8},
    {6, 2, 0, 0, 0, 0, 9, 3, 0}
};

int medium_puzzle[][9] = {
    {5, 0, 0, 6, 1, 0, 0, 0, 0},
    {0, 2, 0, 4, 5, 7, 8, 0, 0},
    {1, 0, 0, 0, 0, 0, 5, 0, 3},
    {0, 0, 0, 0, 2, 1, 0, 0, 0},
    {4, 0, 0, 0, 0, 0, 0, 0, 6},
    {0, 0, 0, 3, 6, 0, 0, 0, 0},
    {9, 0, 3, 0, 0, 0, 0, 0, 2},
    {0, 0, 6, 7, 3, 9, 0, 8, 0},
    {0, 0, 0, 0, 8, 6, 0, 0, 5}
};

int hard_puzzle[][9] = {
    {0, 4, 0, 0, 2, 5, 9, 0, 0},
    {0, 0, 0, 0, 3, 9, 0, 4, 0},
    {0, 0, 0, 0, 0, 0, 0, 6, 1},
    {0, 1, 7, 0, 0, 0, 0, 0, 0},
    {6, 0, 0, 7, 5, 4, 0, 0, 9},
    {0, 0, 0, 0, 0, 0, 7, 3, 0},
    {4, 2, 0, 0, 0, 0, 0, 0, 0},
    {0, 9, 0, 5, 4, 0, 0, 0, 0},
    {0, 0, 8, 9, 6, 0, 0, 5, 0}
};

int evil_puzzle[][9] = {
    {0, 6, 0, 8, 2, 0, 0, 0, 0},
    {0, 0, 2, 0, 0, 0, 8, 0, 1},
    {0, 0, 0, 7, 0, 0, 0, 5, 0},
    {4, 0, 0, 5, 0, 0, 0, 0, 6},
    {0, 9, 0, 6, 0, 7, 0, 3, 0},
    {2, 0, 0, 0, 0, 1, 0, 0, 7},
    {0, 2, 0, 0, 0, 9, 0, 0, 0},
    {8, 0, 4, 0, 0, 0, 7, 0, 0},
    {0, 0, 0, 0, 4, 8, 0, 2, 0}
};

int (*puzzle)[9];
list<int> assignment;

void print(int (*puzzle)[9])
{
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            cout<<puzzle[i][j]<<" ";
        }
        cout<<endl;
    }
}

bool isComplete(int (*puzzle)[9])
{
    // NOT check legal
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            if (puzzle[i][j] == 0)
                return false;
        }
    }

    return true;
}

bool isLegal(int (*puzzle)[9])
{
    // NOT check finish
    int sum;

    // Check Row
    for (int i = 0; i < 9; ++i)
    {
        sum = 0;
        for (int j = 0; j < 9; ++j)
        {
            if (sum & ((1 << puzzle[i][j]) >> 1))
            {
                // Repeat
                return false;
            }
            // Record
            sum += (1 << puzzle[i][j]) >> 1;
        }
    }

    // Check Column
    for (int i = 0; i < 9; ++i)
    {
        sum = 0;
        for (int j = 0; j < 9; ++j)
        {
            if (sum & ((1 << puzzle[j][i]) >> 1))
            {
                // Repeat
                return false;
            }
            // Record
            sum += (1 << puzzle[j][i]) >> 1;
        }
    }

    // Check Subgrid
    for (int l = 0; l < 3; ++l)
    {
        for (int k = 0; k < 3; ++k)
        {
            sum = 0;
            for (int i = 0; i < 3; ++i)
            {
                for (int j = 0; j < 3; ++j)
                {
                    if (sum & ((1 << puzzle[3 * l + i][3 * k + j]) >> 1))
                    {
                        // Repeat
                        return false;
                    }
                    // Record
                    sum += (1 << puzzle[3 * l + i][3 * k + j]) >> 1;
                }
            }
        }
    }
    return true;
}

void select(int *pPos, int* pI, int* pJ, int (*puzzle)[9])
{
    int new_pos = *pPos;
    while (puzzle[new_pos / 9][new_pos % 9] != 0)
    {
        new_pos = (new_pos + 1) % 81;
        assert(new_pos != *pPos);
    }

    *pI = new_pos / 9;
    *pJ = new_pos % 9;
    *pPos = new_pos;
}

bool solve(int pos, int (*puzzle)[9])
{
    int i, j;

    // Base case
    if (isComplete(puzzle))
        return true;

    select(&pos, &i, &j, puzzle);
    for (int k = 1; k <= 9; ++k)
    {
        puzzle[i][j] = k;
#ifdef DBG
cout<<"Try ("<<i<<", "<<j<<") = "<<k<<endl;
if (i == 0 && j == 0 && k == 4)
{
    print(puzzle);
    assert(0);
}
#endif
        if (isLegal(puzzle))
        {
            assignment.push_back(k);
            if (solve(pos, puzzle))
            {
                return true;
            }
            // Failed - backtrack
            assignment.pop_back();
            puzzle[i][j] = 0;
        }
    }
    // Tried all values in domain for this variable
    puzzle[i][j] = 0;
    return false;
}

int main(int argc, char* argv[])
{
    puzzle = eazy_puzzle;
    puzzle = medium_puzzle;
    puzzle = hard_puzzle;
    puzzle = evil_puzzle;

    assert(solve(0, puzzle));
    print(puzzle);

    return 0;
}
