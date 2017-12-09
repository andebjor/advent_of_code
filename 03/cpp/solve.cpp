#include <iostream>
#include <cassert>


typedef struct
{
    uint64_t layer;
    uint64_t start;
    uint64_t end;
} layer_info;


layer_info get_layer(uint64_t location)
{
    layer_info li = {0, 0, 1};

    while (li.end < location)
    {
        li.layer++;
        li.start = li.end + 1;

        auto num_in_layer = li.layer*2*4;

        li.end = li.start + num_in_layer - 1;
    }

    return li;
}


uint64_t get_side_start(uint64_t location, const layer_info &li)
{
    auto per_side = 2*li.layer;

    unsigned int side = 0;
    auto side_start = li.start;
    while (side_start + per_side < location)
    {
        side++;
        side_start += per_side;
    }
    assert(side < 4);

    return side_start;
}


uint64_t get_num_steps(uint64_t location)
{
    layer_info li = get_layer(location);
    auto side_start = get_side_start(location, li);

    // distance is two parts: the long and the short
    auto num_steps = li.layer; // the long part

    // calculate the short part
    auto rest = location - side_start;
    auto steps_to_middle = li.layer - 1;
    if (rest < steps_to_middle)
    {
        num_steps += (steps_to_middle - rest);
    }
    else
    {
        num_steps += (rest - steps_to_middle);
    }

    return num_steps;
}


int main(void)
{
    auto num_steps = get_num_steps(277678);
    std::cout << "Answer to part 1 is: " << num_steps << '\n';

    return 0;
}

