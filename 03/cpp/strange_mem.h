#ifndef STRANGE_MEM_H
#define STRANGE_MEM_H

#include <cstdint>
#include <utility>
#include <vector>


template<typename T>
class Strange_memory
{
    public:
        Strange_memory(uint64_t layers);
        T fill_until_larger(const T &value);
        void set_value(const T &value, uint64_t position);

    private:
        T get_neigh_sum(uint64_t position);
        std::pair<uint64_t, uint64_t> get_2D_pos(uint64_t position);

        std::vector<std::vector<T>> mem;
        T n_layers;
        T side_len;
};

#endif
