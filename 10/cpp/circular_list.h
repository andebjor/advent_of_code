#ifndef CIRCULAR_LIST_H
#define CIRCULAR_LIST_H

#include <cstddef>
#include <vector>


template<typename T>
class Circular_list
{
    public:
        Circular_list(size_t length, bool fill_linear=false);

        const T &Get(size_t index) const;
        Circular_list<T> Get(size_t start, size_t length) const;

        void Set(size_t index, const T &value);
        void Set(size_t index, const Circular_list<T> &sublist);

        void Reverse();

        size_t size() const {return list.size();}

    private:
        size_t lin_index(size_t circ_index) const {return circ_index%size();};

        std::vector<T> list;
};

#endif
