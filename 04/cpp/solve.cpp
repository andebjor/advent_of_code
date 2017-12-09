#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <iostream>


std::string read_file(const std::string &f_name)
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


bool is_valid(const std::vector<std::string> &phrase)
{
    for (size_t i=0; i<phrase.size(); i++)
    {
        for (size_t j=i+1; j<phrase.size(); j++)
        {
            if (phrase[i] == phrase[j])
            {
                return false;
            }
        }
    }

    return true;
}


uint64_t get_num_valid(const std::vector<std::string> &phrases)
{
    uint64_t n_valid = 0;
    for (size_t i=0; i<phrases.size(); i++)
    {
        const auto words = tokenize(phrases[i], ' ');

        if (is_valid(words))
        {
            n_valid++;
        }
    }

    return n_valid;
}


int main(void)
{
    const auto file_string = read_file("../input/passphrases.txt");
    const auto phrases     = tokenize(file_string, '\n');

    const auto num_valid = get_num_valid(phrases);
    std::cout << "Answer to part 1 is: " << num_valid << '\n';

    return 0;
}

