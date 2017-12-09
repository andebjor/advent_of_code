#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
#include <limits>
#include <cassert>


std::string read_file(const std::string &f_name)
{
    std::ifstream f(f_name);
    std::stringstream buffer;
    buffer << f.rdbuf();

    return buffer.str();
}


std::vector<std::string> tokenize(const std::string &input, const char token)
{
    std::vector<std::string> ret;
    std::string tmp = "";
    for (size_t i=0; i<input.length(); i++)
    {
        if (input[i] == token)
        {
            ret.push_back(tmp);
            tmp = "";
        }
        else
        {
            tmp += input[i];
        }
    }

    // add the last part, if not empty
    if (tmp != "")
    {
        ret.push_back(tmp);
    }


    return ret;
}


std::vector<std::vector<int>> convert_to_arrays(const std::string &spreadsheet)
{
    std::vector<std::vector<int>> ret;

    std::vector<std::string> lines = tokenize(spreadsheet, '\n');
    ret.reserve(lines.size());
    for (size_t i_row=0; i_row<lines.size(); i_row++)
    {
        std::vector<std::string> line = tokenize(lines[i_row], '\t');

        ret.push_back(std::vector<int>());
        ret.back().reserve(line.size());
        for (size_t i_item=0; i_item<line.size(); i_item++)
        {
            ret.back().push_back(atoi(line[i_item].c_str()));
        }
    }

    return ret;
}


template<typename T>
std::pair<T,T> get_min_max(const std::vector<T> array)
{
    T min = std::numeric_limits<T>::max();
    T max = std::numeric_limits<T>::min();
    for (size_t i=0; i<array.size(); i++)
    {
        if (array[i] < min)
        {
            min = array[i];
        }
        if (array[i] > max)
        {
            max = array[i];
        }
    }

    return std::pair<T,T>(min, max);
}


template<typename T>
T get_checksum(const std::vector<std::vector<T>> &spreadsheet)
{
    T checksum = 0;
    for (size_t i_row=0; i_row<spreadsheet.size(); i_row++)
    {
        std::pair<T,T> min_max = get_min_max(spreadsheet[i_row]);
        checksum += min_max.second - min_max.first;
    }

    return checksum;
}


template<typename T>
std::pair<T,T> get_divisors(const std::vector<T> array)
{
    // loop over array, in inner and outer loop
    // outer is for numerator
    // inner is for denominator

    for (size_t i_n=0; i_n<array.size(); i_n++)
    {
        for (size_t i_d=0; i_d<array.size(); i_d++)
        {
            // we cant divide with our self...
            if (i_n == i_d)
            {
                continue;
            }

            if (array[i_n]%array[i_d] == 0)
            {
                return std::pair<T,T>(array[i_n], array[i_d]);
            }
        }
    }

    assert(false);
}


template<typename T>
T get_div_sum(const std::vector<std::vector<T>> &spreadsheet)
{
    T sum = 0;
    for (size_t i_row=0; i_row<spreadsheet.size(); i_row++)
    {
        std::pair<T,T> divisors = get_divisors(spreadsheet[i_row]);
        sum += divisors.first/divisors.second;
    }

    return sum;
}


int main(void)
{
    const std::string file_string                   = read_file("../input/spreadsheet.dat");
    const std::vector<std::vector<int>> spreadsheet = convert_to_arrays(file_string);

    int checksum = get_checksum(spreadsheet);
    std::cout << "Answer to part 1 is: " << checksum << '\n';

    int div_sum = get_div_sum(spreadsheet);
    std::cout << "Answer to part 2 is: " << div_sum << '\n';

    return 0;
}

