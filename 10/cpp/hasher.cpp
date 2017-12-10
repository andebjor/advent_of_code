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
}


// force instantiation of the class for int
template class Hasher<int>;
