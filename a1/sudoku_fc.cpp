#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <random>
#include <list>
#include <vector>

#include <sys/types.h>
#include <unistd.h>


#define IS_VALID(pos, val)	((((1 << pos) >> 1) & val) != 0)
#define SET(pos, val) 		val = val | ((1 << pos) >> 1)
#define CLEAR(pos, val)		val = val & (~((1 << pos) >> 1))

using namespace std;

int easy_puzzle[][9] = {
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

int test_puzzle[][9] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 1, 0, 0, 0, 0, 0, 0, 0},
    {0, 2, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0}
};


int (*puzzle)[9];
list<int> assignment;
unsigned int seed;
unsigned int countNode = 0;

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

void select(
    const vector<int>* const pVariable,
    int* pPos,
    int* pI,
    int* pJ
)
{
    int newPos;

    assert(*pPos != pVariable->size());
    newPos = (*pVariable)[*pPos];
    *pI = newPos / 9;
    *pJ = newPos % 9;
    // Update iterator
    ++(*pPos);
}

void initDomain(vector<int>* pDomain)
{
    pDomain->reserve(9);
    // Init. Domain
    for (int i = 1; i <= 9; ++i)
    {
        pDomain->push_back(i);
    }
    // Randomize Domain
    shuffle(pDomain->begin(), pDomain->end(), std::default_random_engine(seed));
}

void initVariable(const int (*puzzle)[9], vector<int>* pVariable)
{
    pVariable->reserve(81);
    // Init. Variable
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            if (puzzle[i][j] == 0)
            {
                pVariable->push_back(i * 9 + j);
            }
        }
    }
    // Randomize Variable
    shuffle(pVariable->begin(), pVariable->end(), std::default_random_engine(seed));
}

void updateTable
(
    unsigned int (*table)[9],
    const int val,
    const int x,
    const int y
)
{
//cout<<endl;
//print(reinterpret_cast<int (*)[9]>(table));
     
    // Update Row
    for (int j = 0; j < 9; ++j)
    {
        if (j != y)
        {
            CLEAR(val, table[x][j]);
        }
        else
        {
            table[x][j] = 0;
            SET(val, table[x][j]);
        }

    }
//cout<<endl;
//print(reinterpret_cast<int (*)[9]>(table));

    // Update Column
    for (int i = 0; i < 9; ++i)
    {
        if (i != x)
        {
	    CLEAR(val, table[i][y]);
        }
        else
        {
            table[i][y] = 0;
            SET(val, table[i][y]);
        }
    }
//cout<<endl;
//print(reinterpret_cast<int (*)[9]>(table));

    // Locate Subgrid (i, k)
    int l = x / 3;
    int k = y / 3;
    // Update Subgrid
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            int m = 3 * l + i;
            int n = 3 * k + j;
            if (m != x || n != y)
            {
	        CLEAR(val, table[m][n]);
            }
            else
            {
                table[m][n] = 0;
                SET(val, table[m][n]);
            }
        }
    }
//cout<<endl;
//print(reinterpret_cast<int (*)[9]>(table));
}

bool checkTable(const unsigned int (*table)[9])
{
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            if (table[i][j] == 0)
                return false;
        }
    }
    return true;
}

void initTable
(
    unsigned int (*table)[9],
    const int (*puzzle)[9] 
)
{
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            if (puzzle[i][j] != 0)
            {
                updateTable(table, puzzle[i][j], i, j);
            }
        }
    }
}

bool solve(
    const unsigned int (*pTable)[9], // Table in previous state
    const vector<int>* const pDomain,
    const vector<int>* const pVariable,
    int pos,
    int (*puzzle)[9]
)
{
    unsigned int table[9][9]; // Table for forward checking
    int i, j;

    // Base case
    if (isComplete(puzzle))
        return true;


    // Init. table for forward checking
    memcpy(table, pTable, 4 * 9 * 9);
    select(pVariable, &pos, &i, &j);
    // Init. domain
    for (int k = 0; k < 9; ++k)
    {
        if (!IS_VALID((*pDomain)[k], table[i][j]))
        {
            // This value is not in the domain
            continue; // Skip
        }

        puzzle[i][j] = (*pDomain)[k];
        ++countNode;
        if (isLegal(puzzle))
        {
            // Forward checking
            updateTable(table, puzzle[i][j], i, j);
            if (!checkTable(table))
            {
                // Failed - backtrack
                puzzle[i][j] = 0;
                memcpy(table, pTable, 4 * 9 * 9);
                continue;
            }

            assignment.push_back((*pDomain)[k]);
            if (solve(table, pDomain, pVariable, pos, puzzle))
            {
                return true;
            }
            // Failed - backtrack
            assignment.pop_back();
            puzzle[i][j] = 0;
            memcpy(table, pTable, 4 * 9 * 9);
        }
    }
    // Tried all values in domain for this variable
    puzzle[i][j] = 0;
    return false;
}

int main(int argc, char* argv[])
{
    int index = atoi(argv[1]);
    switch(index)
    {
        case 0:
            puzzle = easy_puzzle;
            cout<<"easy"<<endl;
            break;

        case 1:
            puzzle = medium_puzzle;
            cout<<"medium"<<endl; 
            break;

        case 2:
            puzzle = hard_puzzle;
            cout<<"hard"<<endl;
            break;

        case 3:
            puzzle = evil_puzzle;
            cout<<"evil"<<endl;
            break;

        default:
/*
            puzzle = test_puzzle;
            break;
*/
            assert(0);
    }

    // Initialize
    seed = (unsigned int)getpid();
    vector<int> variable, domain;
    initVariable(puzzle, &variable);
    initDomain(&domain);
    vector<int>::iterator endIt = variable.end();
    unsigned int table[9][9];
    for (int i = 0; i < 9; ++i)
    {
        for (int j = 0; j < 9; ++j)
        {
            table[i][j] = 0x1ff;
        }
    }
    initTable(table, puzzle);
/*
    print(reinterpret_cast<int (*)[9]>(table));
    cout<<endl;
    puzzle[0][1] = 3;
    updateTable(table, 3, 0, 1);
    print(reinterpret_cast<int (*)[9]>(table));
    cout<<endl;
    puzzle[8][8] = 3;
    updateTable(table, 3, 8, 8);
    print(reinterpret_cast<int (*)[9]>(table));
*/    


    // Solve + Print result
    assert(solve(table, &domain, &variable, 0, puzzle));
    print(puzzle);
    cout<<"count: "<<countNode<<endl;
    return 0;
}
