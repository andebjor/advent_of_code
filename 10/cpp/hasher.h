#ifndef HASHER_H
#define HASHER_H

#include "circular_list.h"


template<typename T>
class Hasher
{
    public:
        Hasher(size_t length);

        const T &Get(size_t index) const;

        void Apply(size_t length);

    private:
        Circular_list<T> list;
        size_t position;
        size_t skip_size;
};

#endif
