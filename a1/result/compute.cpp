#include <fstream>
#include <iostream>
#include <cmath>
#include <sstream>
#include <cassert>

using namespace std;

typedef unsigned long long uint64;
typedef unsigned int uint32;

uint64 Avg(uint64 values[], uint32 count)
{
    uint64 sum = 0;
    for (uint32 i = 0; i < count; ++i)
    {
       sum += values[i];
    }

    sum = sum / count;
    return sum;
}

double Std(uint64 values[], uint32 count)
{
    uint64 avg = Avg(values, count);
    double var = 0;
    double std;

    for (uint32 i = 0; i < count; ++i)
    {
       uint64 diff;
       if (values[i] > avg)
       {
           diff = values[i] - avg;
       }
       else
       {
           diff = avg - values[i];
       }
       var += pow(static_cast<double>(diff), 2.00);
//       cout<<"diff: "<<diff<<"\tvar: "<<var<<endl;
    }

    var /= static_cast<double>(count);
    std = sqrt(var);
    return std;
}

double AvgD(double values[], uint32 count)
{
    double sum = 0;
    for (uint32 i = 0; i < count; ++i)
    {
       sum += values[i];
    }

    sum = sum / static_cast<double>(count);
    return sum;
}

double StdD(double values[], uint32 count)
{
    double avg = AvgD(values, count);
    double var = 0;
    double std;

    for (uint32 i = 0; i < count; ++i)
    {
       double diff;
       if (values[i] > avg)
       {
           diff = values[i] - avg;
       }
       else
       {
           diff = avg - values[i];
       }
       var += pow(diff, 2.00);
//       cout<<"diff: "<<diff<<"\tvar: "<<var<<endl;
    }

    var /= static_cast<double>(count);
    std = sqrt(var);
    return std;
}

bool ReadNodeFile(string fileName, uint64 values[], uint32 count)
{
    ifstream iff;
    iff.open(fileName);

    if (iff.fail())
        return false;

    for (uint32 i = 0; i < count; ++i)
    {
        stringstream ss;
        string line;
        string token;
        getline(iff, line);
        
        ss<<line;
        ss>>token;
        ss>>values[i];
//        cout<<values[i]<<endl;
    }
    iff.close();
    return true;
}

double ParseTimeString(const string& str)
{
    static double mM = 60.00;
    stringstream mStr;
    stringstream sStr;
    uint32 i, j;

    for (i = 0; i < str.size(); ++i)
    {
        if (str[i] == 'm')
        {
            break;
        }
        mStr<<str[i];
    }
    for (j = i + 1; j < str.size(); ++j)
    {
        if (str[j] == 's')
        {
            break;
        }
        sStr<<str[j];
    }

    double sec, min, total;
    sStr>>sec;
    mStr>>min;
    total = sec + min * mM;
    return total; 
}

bool ReadTimeFile(string fileName, double values[], uint32 count)
{
    ifstream iff;
    iff.open(fileName);

    if (iff.fail())
        return false;

    for (uint32 i = 0; i < count; ++i)
    {
        stringstream ss;
        string line;
        string token;
        getline(iff, line);
        
        ss<<line;
        ss>>token;
	ss>>values[i];
//        ss>>token;
//        values[i] = ParseTimeString(token);
//        cout<<values[i]<<endl;
    }
    iff.close();
    return true;
}

int main(int argc, char* argv[])
{
/*
    uint64 values[50];

    ReadNodeFile("fc_h/easy_fc_h_node.txt", values, 50);
    cout<<"average: "<<static_cast<double>(Avg(values, 50))<<endl;
    cout<<"standard deviation: "<<Std(values, 50)<<endl;

    ReadNodeFile("fc_h/medium_fc_h_node.txt", values, 50);
    cout<<"average: "<<static_cast<double>(Avg(values, 50))<<endl;
    cout<<"standard deviation: "<<Std(values, 50)<<endl;

    ReadNodeFile("fc_h/hard_fc_h_node.txt", values, 50);
    cout<<"average: "<<static_cast<double>(Avg(values, 50))<<endl;
    cout<<"standard deviation: "<<Std(values, 50)<<endl;

    ReadNodeFile("fc_h/evil_fc_h_node.txt", values, 50);
    cout<<"average: "<<static_cast<double>(Avg(values, 50))<<endl;
    cout<<"standard deviation: "<<Std(values, 50)<<endl;
*/
    double values[50];

    ReadTimeFile("fc_h/easy_fc_h.txt", values, 50);
    cout<<"average: "<<AvgD(values, 50)<<endl;
    cout<<"standard deviation: "<<StdD(values, 50)<<endl;

    ReadTimeFile("fc_h/medium_fc_h.txt", values, 50);
    cout<<"average: "<<AvgD(values, 50)<<endl;
    cout<<"standard deviation: "<<StdD(values, 50)<<endl;

    ReadTimeFile("fc_h/hard_fc_h.txt", values, 50);
    cout<<"average: "<<AvgD(values, 50)<<endl;
    cout<<"standard deviation: "<<StdD(values, 50)<<endl;

    ReadTimeFile("fc_h/evil_fc_h.txt", values, 50);
    cout<<"average: "<<AvgD(values, 50)<<endl;
    cout<<"standard deviation: "<<StdD(values, 50)<<endl;
    
    return 0;
}
