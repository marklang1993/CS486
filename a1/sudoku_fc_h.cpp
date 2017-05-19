#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <random>
#include <list>
#include <vector>
#include <map>

#include <time.h>
#include <sys/types.h>
#include <unistd.h>

#define FIX_BIT			31
#define MOST_CONSTRAINING_MAX   0x1b // 9 + 9 + 9 is overestimated, but it is ok

#define IS_VALID(pos, val)	((((1 << pos) >> 1) & val) != 0)
#define SET(pos, val) 		val = val | ((1 << pos) >> 1)
#define CLEAR(pos, val)		val = val & (~((1 << pos) >> 1))
#define GET_POS(x, y)           (x * 9 + y)

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
/*
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
*/

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
//            cout<<setw(9)<<hex<<puzzle[i][j]<<" ";
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
            SET(FIX_BIT, table[x][j]);
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
            SET(FIX_BIT, table[i][y]);
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
                SET(FIX_BIT, table[m][n]);
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

int countConstrainingVar
(
    const unsigned int (*table)[9],
    int pos
)
{
    int cntVar = 0;
    int x = pos / 9;
    int y = pos % 9;

    // Update Row
    for (int j = 0; j < 9; ++j)
    {
        if (!IS_VALID(FIX_BIT, table[x][j]))
        {
            // Only check with remaining variables
            if (j == y)
            {
                // Will not count itself
                continue;
            }
            ++cntVar;
        }
    }

    // Update Column
    for (int i = 0; i < 9; ++i)
    {
        if (!IS_VALID(FIX_BIT, table[i][y]))
        {
            // Only check with remaining variables
            if (i == x)
            {
                // Will not count itself
                continue;
            }
            ++cntVar;
        }
    }

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
            
            if (!IS_VALID(FIX_BIT, table[m][n]))
            {
                // Only check with remaining variables
                if (m == x || n == y)
                {
                    // Will not count itself & current row & current column
                    continue;
                }
                ++cntVar;
            }
        }
    }

    return cntVar;
}

void sortVarByH
(
    const unsigned int (*table)[9],
    const vector<int>* const pVariable,
    multimap<int, int>* pSortedVar
)
{
    for (int i = 0; i < pVariable->size(); ++i)
    {
        int pos = (*pVariable)[i];
        int allBits = table[pos / 9][pos % 9];
        int cntBit = 0;
        int cntConstraining = 0;
        // If this variable is fix (set), skip
        if (IS_VALID(FIX_BIT, allBits))
            continue;

        for (int j = 0; j < 10; ++j)
        {
            int r = allBits & 0x1;
            allBits = allBits >> 1;
            if (r != 0)
                ++cntBit;
        }
        cntConstraining = countConstrainingVar(table, pos);
        pSortedVar->insert(make_pair(
                                  //cntConstraining,
                                  (MOST_CONSTRAINING_MAX - cntConstraining) | (cntBit << 16),
                                  pos)
                                 );
    }
/*
    for (map<int, int>::iterator it = pSortedVar->begin();
         it != pSortedVar->end(); ++it)
    {
        cout<<"Pos: "<<it->second / 9<<", "<<it->second % 9;
        cout<<"\tCnt: "<<it->first<<endl;
    }
    cout<<endl;
*/
}

int calRuleOut
(
    const unsigned int (*table)[9],
    int val,
    int pos
)
{
    int cntRuleOut = 0;
    int x = pos / 9;
    int y = pos % 9;

    // Update Row
    for (int j = 0; j < 9; ++j)
    {
        if (!IS_VALID(FIX_BIT, table[x][j]))
        {
            // Only check with remaining variables
            if (j == y)
            {
                // Will not count itself
                continue;
            }
            if (IS_VALID(val, table[x][j]))
                ++cntRuleOut;
        }
    }

    // Update Column
    for (int i = 0; i < 9; ++i)
    {
        if (!IS_VALID(FIX_BIT, table[i][y]))
        {
            // Only check with remaining variables
            if (i == x)
            {
                // Will not count itself
                continue;
            }
            if (IS_VALID(val, table[i][y]))
                ++cntRuleOut;
        }
    }

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
            
            if (!IS_VALID(FIX_BIT, table[m][n]))
            {
                // Only check with remaining variables
                if (m == x || n == y)
                {
                    // Will not count itself & current row & current column
                    continue;
                }
            if (IS_VALID(val, table[m][n]))
                ++cntRuleOut;
            }
        }
    }

    return cntRuleOut;
}

void sortDomainByH
(
    const unsigned int (*table)[9],
    const vector<int>* const pDomain,
    int pos,
    multimap<int, int>* pSortedDomain
)
{
    int i = pos / 9;
    int j = pos % 9;

    for (int k = 0; k < 9; ++k)
    {
        int cntRuleOutVal;
        int val = (*pDomain)[k];
        if (!IS_VALID(val, table[i][j]))
        {
            // This value is not in the domain
            continue; // Skip
        }
        cntRuleOutVal = calRuleOut(table, val, pos);
        pSortedDomain->insert(make_pair(cntRuleOutVal, val));
    }
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

bool solve(
    const unsigned int (*pTable)[9], // Table in previous state
    const vector<int>* const pDomain,
    const vector<int>* const pVariable,
    int (*puzzle)[9]
)
{
    unsigned int table[9][9]; // Table for forward checking
    int pos, i, j;

    // Base case
    if (isComplete(puzzle))
        return true;

    // Init. table for forward checking
    memcpy(table, pTable, 4 * 9 * 9);
    // Init. multimap for most constrained / constraining variables 
    multimap<int, int> sortedVar;
    sortVarByH(pTable, pVariable, &sortedVar); 
    // Select Variable
    pos = sortedVar.begin()->second;
    i = pos / 9;
    j = pos % 9;
    // Init. domain
    multimap<int, int> sortedDomain;
    sortDomainByH(table, pDomain, pos, &sortedDomain);
/*
    cout<<"Pos: "<<i<<", "<<j<<endl;
    for (multimap<int, int>::iterator it = sortedDomain.begin();
         it != sortedDomain.end();
         ++it)
    {
         cout<<"CntRuleOut: "<<it->first;
         cout<<"\tVal: "<<it->second<<endl;
    }
*/
    for (multimap<int, int>::iterator it = sortedDomain.begin();
         it != sortedDomain.end();
         ++it)
    {
        puzzle[i][j] = it->second;
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

            assignment.push_back(it->second);
            if (solve(table, pDomain, pVariable, puzzle))
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
*/
    // Solve + Print result
    clock_t startTime = clock();
    assert(solve(table, &domain, &variable, puzzle));
    clock_t endTime = clock();
    double interval = endTime - startTime;
    interval = interval / (double)CLOCKS_PER_SEC;
    print(puzzle);
    cout<<"count: "<<countNode<<endl;
    cout<<"time: "<<interval<<" s"<<endl;
    return 0;
}
