#ifndef SOLVE_H
#define SOLVE_H

#include <cstdint>
#include <utility>
#include <cassert>


typedef struct
{
    uint64_t layer;
    uint64_t start;
    uint64_t end;
} layer_info;


layer_info get_layer(uint64_t location);
std::pair<int,uint64_t> get_side_start(uint64_t location, const layer_info &li);
uint64_t get_num_steps(uint64_t location);
uint64_t get_first_larger(uint64_t value);

#endif
