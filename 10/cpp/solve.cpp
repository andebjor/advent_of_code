#include "hasher.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <iomanip>


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


std::vector<int> str_to_array(const std::string &input)
{
    std::vector<int> ret;
    ret.reserve(input.length());

    for (size_t i=0; i<input.size(); i++)
    {
        if (input[i] != '\n')
        {
            ret.push_back(input[i]);
        }
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


int solve_part_1(const std::string &fname)
{
    const auto file_string = read_file(fname);
    const auto lengths     = convert_to_array(file_string);

    Hasher<int> hasher(256);
    run_hashing(hasher, lengths);

    return hasher.Get(0)*hasher.Get(1);
}


std::string solve_part_2(const std::string &fname)
{
    const auto file_string = read_file(fname);
    auto lengths           = str_to_array(file_string);
    // append the lengths from the description
    lengths.push_back(17);
    lengths.push_back(31);
    lengths.push_back(73);
    lengths.push_back(47);
    lengths.push_back(23);

    Hasher<int> hasher(256);
    for (size_t i=0; i<64; i++)
    {
        run_hashing(hasher, lengths);
    }

    const auto hash = hasher.get_dense_hash();

    std::stringstream ret;
    for (size_t i=0; i<hash.size(); i++)
    {
        ret << std::setfill('0') << std::setw(2) << std::hex << hash[i];
    }

    return ret.str();
}


int main(void)
{
    long ans = solve_part_1("../input/lengths.dat");
    std::cout << "Answer to part 1 is: " << ans << '\n';

    std::string hash = solve_part_2("../input/lengths.dat");
    std::cout << "Answer to part 2 is: " << hash << '\n';

    return 0;
}
