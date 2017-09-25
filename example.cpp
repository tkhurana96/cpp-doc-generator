// example.cpp

#include <iostream>
#include <vector>

/**
    * @function someFunc
    * @desc Multiplies every number in the collection of given input numbers by
    * the given multiplier
    *
    * @param {std::vector<int>} _v Collection of integers
    * @param {int} _multiplier Amount to multiply every number by
    * @returns {std::vector<int>} Collection of results
*/
auto times(const std::vector<int>& _v, const int& _multiplier){
    
    std::vector<int> res;

    for(auto &x: _v){
        res.push_back(x * _multiplier);
    }

    return res;
}

int main(){

    std::vector<int> my_vec{4, 6, 8, 2, 1};

    auto twice = times(my_vec, 2);
    std::cout << "Double of my_vec:";
    for (auto &x: twice){
        std::cout << ' ' << x;
    }

    std::cout << '\n';

    auto thrice = times(my_vec, 3);
    std::cout << "Thrice of my_vec:";
    for (auto &x: thrice){
        std::cout << ' ' << x;
    }

    return 0;
}