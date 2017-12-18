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


bool has_neighbour(const std::vector<std::vector<int>> &grid,
                   size_t i,
                   size_t j,
                   int value)
{
    if (i >= 1)
    {
        if (grid[i-1][j] == value)
        {
            return true;
        }
    }

    if (i < grid.size()-1)
    {
        if (grid[i+1][j] == value)
        {
            return true;
        }
    }

    if (j >= 1)
    {
        if (grid[i][j-1] == value)
        {
            return true;
        }
    }

    if (j < grid[i].size()-1)
    {
        if (grid[i][j+1] == value)
        {
            return true;
        }
    }

    return false;
}


size_t solve_2(std::vector<std::vector<int>> &grid)
{
    int cur_region = 1;
    bool found_new_region = true;
    while (found_new_region)
    {
        // search for a new region
        found_new_region = false;
        for (size_t i=0; i<grid.size(); i++)
        {
            for (size_t j=0; j<grid[i].size(); j++)
            {
                if (found_new_region == false)
                {
                    if (grid[i][j] == -1)
                    {
                        found_new_region = true;
                        grid[i][j] = cur_region;
                    }
                }
            }
        }

        bool found_new_member = true;
        while (found_new_member)
        {
            // grow the region
            found_new_member = false;
            for (size_t i=0; i<grid.size(); i++)
            {
                for (size_t j=0; j<grid[i].size(); j++)
                {
                    if (grid[i][j] == -1)
                    {
                        if (has_neighbour(grid, i, j, cur_region))
                        {
                            grid[i][j] = cur_region;
                            found_new_member = true;
                        }
                    }
                }
            }
        }

        cur_region++;
    }

    return cur_region-2;
}


void solve(const std::string &input)
{
    size_t n_used = 0;
    std::vector<std::vector<int>> grid;

    for (size_t i=0; i<128; i++)
    {
        auto v = knot_hash(input + "-" + std::to_string(i));
        grid.push_back(std::vector<int>(128, 0));
        for (size_t j=0; j<v.size(); j++)
        {
            for (size_t k=0; k<8; k++)
            {
                if ((v[j] << k) & 128)
                {
                    n_used++;
                    grid[i][j*8 + k] = -1;
                }
            }
        }
    }

    std::cout << "Answer to part 1 is: " << n_used << '\n';

    auto n_regions = solve_2(grid);
    std::cout << "Answer to part 2 is: " << n_regions << '\n';
}


int main(void)
{
    std::string input("ljoxqyyw");
    solve(input);

    return 0;
}
