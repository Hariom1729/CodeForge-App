import asyncio
import httpx

SEED_DATA = {
    "problems": [
        {
            "title": "Two Sum",
            "topic": "Arrays",
            "difficulty": "Easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
            "time_limit_ms": 2000,
            "memory_limit_mb": 256,
            "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}],
            "starter_code": {
                "cpp": """#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        return {};
    }
};

int main() {
    // Boilerplate will be handled by Execution Engine using stdin later
    return 0;
}"""
            },
            "visible_test_cases": [
                {"input": "4\\n2 7 11 15\\n9", "expected_output": "0 1", "is_hidden": False},
                {"input": "3\\n3 2 4\\n6", "expected_output": "1 2", "is_hidden": False}
            ],
            "hidden_test_cases": [
                {"input": "2\\n3 3\\n6", "expected_output": "0 1", "is_hidden": True},
                {"input": "4\\n-1 -2 -3 -4\\n-7", "expected_output": "2 3", "is_hidden": True},
                {"input": "5\\n10 20 30 40 50\\n90", "expected_output": "3 4", "is_hidden": True}
            ]
        },
        {
            "title": "Reverse the array",
            "topic": "Arrays",
            "difficulty": "Easy",
            "description": "Reverse an array of integers in place.",
            "constraints": ["1 <= n <= 10^4"],
            "time_limit_ms": 1000,
            "memory_limit_mb": 256,
            "examples": [{"input": "arr = [1, 2, 3], n = 3", "output": "3 2 1"}],
            "starter_code": {
                "cpp": """#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void reverseTheArray(vector<int>& arr, int n) {
        
    }
};

int main() {
    int n;
    if (cin >> n) {
        vector<int> arr(n);
        for(int i=0; i<n; i++) cin >> arr[i];
        Solution sol;
        sol.reverseTheArray(arr, n);
        for(int i=0; i<n; i++) cout << arr[i] << (i == n-1 ? "" : " ");
        cout << endl;
    }
    return 0;
}"""
            },
            "visible_test_cases": [
                {"input": "3\\n1 2 3", "expected_output": "3 2 1", "is_hidden": False},
                {"input": "5\\n10 20 30 40 50", "expected_output": "50 40 30 20 10", "is_hidden": False}
            ],
            "hidden_test_cases": [
                {"input": "1\\n100", "expected_output": "100", "is_hidden": True},
                {"input": "2\\n-5 5", "expected_output": "5 -5", "is_hidden": True},
                {"input": "4\\n0 0 0 0", "expected_output": "0 0 0 0", "is_hidden": True}
            ]
        }
    ]
}

async def seed():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/admin/bulk-import", json=SEED_DATA)
        print("Status:", response.status_code)
        print("Response:", response.json())

if __name__ == "__main__":
    asyncio.run(seed())
