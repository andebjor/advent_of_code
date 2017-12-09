#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
#include <cassert>


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
T count_repeated(const std::vector<T> &array)
{
    T sum = 0;
    for (size_t i=0; i<array.size(); i++)
    {
        const T &c_val = array[i];
        const T &n_val = get_next_circular(i, array);

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

    int sum = count_repeated(array);

    std::cout << "Answer is: " << sum << '\n';

    return 0;
}

