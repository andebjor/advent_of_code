#include "circular_list.h"
#include <algorithm>


template<typename T>
Circular_list<T>::Circular_list(size_t length, bool fill_linear):
    list(length, static_cast<T>(0))
{
    if (fill_linear)
    {
        for (size_t i=0; i<length; i++)
        {
            list[i] = static_cast<T>(i);
        }
    }
}


template<typename T>
const T &Circular_list<T>::Get(size_t index) const
{
    return list[lin_index(index)];
}


template<typename T>
Circular_list<T> Circular_list<T>::Get(size_t start, size_t length) const
{
    Circular_list<T> new_list(length, false);

    for (size_t i=0; i<length; i++)
    {
        new_list.Set(i, Get(start + i));
    }

    return new_list;
}


template<typename T>
void Circular_list<T>::Set(size_t index, const T &value)
{
    list[lin_index(index)] = value;
}


template<typename T>
void Circular_list<T>::Set(size_t index, const Circular_list<T> &sublist)
{
    for (size_t i=0; i<sublist.size(); i++)
    {
        Set(index + i, sublist.Get(i));
    }
}


template<typename T>
void Circular_list<T>::Reverse()
{
    std::reverse(std::begin(list), std::end(list));
}


// force instantiation of the class for int
template class Circular_list<int>;
