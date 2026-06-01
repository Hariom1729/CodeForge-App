import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem

async def fix():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem).filter(Problem.title == "Reverse the array"))
        problem = result.scalars().first()
        if problem:
            # Update test cases to have real expected output
            problem.test_cases = [
                {"input": "arr = [1, 2, 3], n = 3", "expected_output": "3 2 1"}
            ]
            
            # Update the starter code so that main() prints the array
            starter = problem.starter_code.copy() if problem.starter_code else {}
            
            starter["cpp"] = """#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

class Solution {
public:
    void reverseTheArray(vector<int>& arr, int n) {
        // Write your logic here
        
    }
};

int main() {
    Solution sol;
    vector<int> arr = {1, 2, 3};
    sol.reverseTheArray(arr, 3);
    for(int i=0; i<3; i++) cout << arr[i] << (i == 2 ? "" : " ");
    cout << endl;
    return 0;
}"""
            problem.starter_code = starter
            await session.commit()
            print("Successfully updated Reverse the array!")
        else:
            print("Problem not found.")

if __name__ == "__main__":
    asyncio.run(fix())
