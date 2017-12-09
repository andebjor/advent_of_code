#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>
// #include <cassert>


const std::string read_file(const std::string &f_name)
{
    std::ifstream f(f_name);
    std::stringstream buffer;
    buffer << f.rdbuf();

    return buffer.str();
}


std::vector<std::string> tokenize(const std::string &input, const char token)
{
    std::vector<std::string> ret;
    std::string tmp = "";
    for (size_t i=0; i<input.length(); i++)
    {
        if (input[i] == token)
        {
            ret.push_back(tmp);
            tmp = "";
        }
        else
        {
            tmp += input[i];
        }
    }

    // add the last part, if not empty
    if (tmp != "")
    {
        ret.push_back(tmp);
    }


    return ret;
}


const std::vector<int> convert_to_int_array(const std::string &str)
{
    auto str_arr = tokenize(str, '\n');

    std::vector<int> ret;
    ret.reserve(str_arr.size());
    for (size_t i=0; i<str_arr.size(); i++)
    {
        ret.push_back(atoi(str_arr[i].c_str()));
    }

    return ret;
}


uint64_t jumps_until_out(const std::vector<int> &array, bool rule1)
{
    auto     jump_vec(array);
    int      pos     = 0;
    uint64_t n_jumps = 0;

    do
    {
        if (rule1)
        {
            pos += jump_vec[pos]++;
        }
        else
        {
            if (jump_vec[pos] >= 3)
            {
                pos += jump_vec[pos]--;
            }
            else
            {
                pos += jump_vec[pos]++;
            }
        }

        n_jumps++;
    } while (pos >= 0 && pos < jump_vec.size());

    return n_jumps;
}


int main(void)
{
    const auto file_string = read_file("../input/jumplist.dat");
    const auto array       = convert_to_int_array(file_string);

    auto n_jumps = jumps_until_out(array, true);
    std::cout << "Answer to part 1 is: " << n_jumps << '\n';

    n_jumps = jumps_until_out(array, false);
    std::cout << "Answer to part 2 is: " << n_jumps << '\n';

    return 0;
}
