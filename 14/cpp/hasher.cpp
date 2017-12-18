#include "hasher.h"
#include <algorithm>


template<typename T>
Hasher<T>::Hasher(size_t length):
    list(length, true), position(0), skip_size(0)
{
}


template<typename T>
const T &Hasher<T>::Get(size_t index) const
{
    return list.Get(index);
}


template<typename T>
void Hasher<T>::Apply(size_t length)
{
    Circular_list<T> sublist = list.Get(position, length);
    sublist.Reverse();
    list.Set(position, sublist);

    position += length + skip_size++;

    position  %= list.size();
    skip_size %= list.size();
}


template<typename T>
std::vector<T> Hasher<T>::get_dense_hash() const
{
    std::vector<T> ret;
    ret.reserve(16);

    for (size_t i=0; i<16; i++)
    {
        T hsh = list.Get(i*16);
        for (size_t j=1; j<16; j++)
        {
            hsh ^= list.Get(i*16 + j);
        }

        ret.push_back(hsh);
    }

    return ret;
}


// force instantiation of the class for int
template class Hasher<int>;
