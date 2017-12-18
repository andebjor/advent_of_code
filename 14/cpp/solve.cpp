#include "hasher.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <iomanip>


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


std::vector<int> knot_hash(const std::string &input)
{
    auto lengths = str_to_array(input);
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

    return hasher.get_dense_hash();
}


size_t solve_part_1(const std::string &input)
{
    size_t n_used = 0;

    for (size_t i=0; i<128; i++)
    {
        auto v = knot_hash(input + "-" + std::to_string(i));
        for (size_t j=0; j<v.size(); j++)
        {
            for (size_t k=0; k<v.size(); k++)
            {
                if ((v[j] >> k) & 1)
                {
                    n_used++;
                }
            }
        }
    }

    return n_used;
}


int main(void)
{
    std::string input("ljoxqyyw");
    auto ans = solve_part_1(input);
    std::cout << "Answer to part 1 is: " << ans << '\n';

    return 0;
}
