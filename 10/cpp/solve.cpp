#include "hasher.h"

#include <fstream>
#include <sstream>
#include <iostream>


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


std::vector<int> convert_to_array(const std::string &input)
{
    std::vector<int> ret;

    std::vector<std::string> numbers = tokenize(input, ',');
    ret.reserve(numbers.size());
    for (size_t i=0; i<numbers.size(); i++)
    {
        ret.push_back(atoi(numbers[i].c_str()));
    }

    return ret;
}


template<typename T>
void run_hashing(Hasher<T> &hasher, const std::vector<int> &lengths)
{
    for (size_t i=0; i<lengths.size(); i++)
    {
        hasher.Apply(lengths[i]);
    }
}


int main(void)
{
    const auto file_string = read_file("../input/lengths.dat");
    const auto lengths     = convert_to_array(file_string);

    Hasher<int> hasher(256);
    run_hashing(hasher, lengths);

    const long ans = hasher.Get(0)*hasher.Get(1);
    std::cout << "Answer to part 1 is: " << ans << '\n';

    return 0;
}
