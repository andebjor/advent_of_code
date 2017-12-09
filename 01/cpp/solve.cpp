#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
#include <cassert>


typedef enum
{
    NEXT = 0,
    HALFWAY = 1
} skip_def;


const std::string read_file(const std::string &f_name)
{
    std::ifstream f(f_name);
    std::stringstream buffer;
    buffer << f.rdbuf();

    return buffer.str();
}


const std::vector<int> convert_to_array(const std::string &digits)
{
    std::vector<int> ret;
    ret.reserve(digits.length());

    size_t i=0;
    while (digits[i] >= '0' && digits[i] <= '9')
    {
        ret.push_back(digits[i++] - '0');
    }


    return ret;
}


template<typename T>
T get_next_circular(size_t i, const std::vector<T> &array)
{
    assert(i < array.size());

    return array[(i+1)%array.size()];
}


template<typename T>
T get_mirror_circular(size_t i, const std::vector<T> &array)
{
    assert(i < array.size());

    return array[(i + array.size()/2)%array.size()];
}


template<typename T>
T count_repeated(const std::vector<T> &array, skip_def skip)
{
    T sum = 0;
    for (size_t i=0; i<array.size(); i++)
    {
        const T &c_val = array[i];
              T  n_val;
        if (skip == NEXT)
        {
            n_val = get_next_circular(i, array);
        }
        else if (skip == HALFWAY)
        {
            n_val = get_mirror_circular(i, array);
        }
        else
        {
            assert(false);
        }

        if (c_val == n_val)
        {
            sum += c_val;
        }
    }

    return sum;
}


int main(void)
{
    const std::string digits     = read_file("../input/digits.dat");
    const std::vector<int> array = convert_to_array(digits);

    int sum_1 = count_repeated(array, NEXT);
    std::cout << "Answer to part 1 is: " << sum_1 << '\n';

    int sum_2 = count_repeated(array, HALFWAY);
    std::cout << "Answer to part 2 is: " << sum_2 << '\n';

    return 0;
}

