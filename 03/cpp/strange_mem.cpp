#include "strange_mem.h"
#include "solve.h"

#include <cassert>
#include <iostream>


template<typename T>
Strange_memory<T>::Strange_memory(uint64_t layers): n_layers(layers), side_len(2*layers + 1)
{
    for (uint64_t i=0; i<side_len; i++)
    {
        mem.push_back(std::vector<T>());
        mem.back().reserve(side_len);
        for (uint64_t j=0; j<side_len; j++)
        {
            mem.back().push_back(static_cast<T>(0));
        }
    }

    // iniialize center
    mem[layers][layers] = 1;
}


template<typename T>
T Strange_memory<T>::get_neigh_sum(uint64_t position)
{
    std::pair<uint64_t, uint64_t> pos = get_2D_pos(position);

    auto i = pos.first;
    auto j = pos.second;
    assert(i > 0 && i < side_len-1);
    assert(j > 0 && j < side_len-1);

    T sum = 0;
    for (int ip=-1; ip<=1; ip++)
    {

        for (int jp=-1; jp<=1; jp++)
        {
            sum += mem[i + ip][j + jp];
        }
    }

    return sum;
}


template<typename T>
void Strange_memory<T>::set_value(const T &value, uint64_t position)
{
    std::pair<uint64_t, uint64_t> pos = get_2D_pos(position);

    auto i = pos.first;
    auto j = pos.second;
    assert(i < side_len);
    assert(j < side_len);

    mem[i][j] = value;
}


template<typename T>
T Strange_memory<T>::fill_until_larger(const T &value)
{
    uint64_t pos = 0;
    T val;
    do
    {
        val = get_neigh_sum(pos);
        set_value(val, pos);
        pos++;
    } while (val < value);

    return val;
}


template<typename T>
std::pair<uint64_t, uint64_t> Strange_memory<T>::get_2D_pos(uint64_t position)
{
    uint64_t i;
    uint64_t j;
    uint64_t center = n_layers;

    // special case center...
    if (position == 0)
    {
        i = center;
        j = center;
    }
    else
    {
        auto p1_num = position + 1;

        layer_info li = get_layer(p1_num);
        auto side_start = get_side_start(p1_num, li);

        // figure out how far long the side
        auto rest = p1_num - side_start.second;
        switch (side_start.first)
        {
            case 0:
                i = center + li.layer;
                j = center - (li.layer-1) + rest;
                break;
            case 2:
                i = center - li.layer;
                j = center + (li.layer-1) - rest;
                break;
            case 1:
                i = center + (li.layer-1) - rest;
                j = center + li.layer;
                break;
            case 3:
                i = center - (li.layer-1) + rest;
                j = center - li.layer;
                break;
            default:
                assert(false);
        }
    }

// std::cerr << "pos: " << position << ": [" << i << ", " << j << "]\n";
    return std::pair<uint64_t, uint64_t>(i, j);
}


// force instantiation of the class for uint64_t
template class Strange_memory<uint64_t>;
