import asyncio
import pandas as pd
from database import AsyncSessionLocal, engine, Base
from models import Problem
import re

def to_camel_case(s):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', s)
    parts = s.split()
    if not parts:
        return "solve"
    return parts[0].lower() + ''.join(x.capitalize() for x in parts[1:])

def get_topic_context(topic):
    topic = topic.lower()
    if "array" in topic or "matrix" in topic or "sort" in topic:
        return {
            "cpp_args": "vector<int>& arr, int n",
            "py_args": "arr: List[int], n: int",
            "go_args": "arr []int, n int",
            "rs_args": "arr: Vec<i32>, n: i32",
            "cpp_main_call": "vector<int> arr = {1, 2, 3};\n    sol.func_name(arr, 3);",
            "py_main_call": "sol = Solution()\nprint(sol.func_name([1, 2, 3], 3))",
            "go_main_call": "func_name([]int{1, 2, 3}, 3)",
            "rs_main_call": "Solution::func_name(vec![1, 2, 3], 3);",
            "desc_text": "Given an array `arr` of size `n`, write an efficient algorithm to solve this problem."
        }
    elif "string" in topic:
        return {
            "cpp_args": "string s",
            "py_args": "s: str",
            "go_args": "s string",
            "rs_args": "s: String",
            "cpp_main_call": "sol.func_name(\"example\");",
            "py_main_call": "sol = Solution()\nprint(sol.func_name(\"example\"))",
            "go_main_call": "func_name(\"example\")",
            "rs_main_call": "Solution::func_name(String::from(\"example\"));",
            "desc_text": "Given a string `s`, write an efficient algorithm to solve this problem."
        }
    elif "linked list" in topic:
        return {
            "cpp_args": "ListNode* head",
            "py_args": "head: Optional[ListNode]",
            "go_args": "head *ListNode",
            "rs_args": "head: Option<Box<ListNode>>",
            "cpp_main_call": "// sol.func_name(head);",
            "py_main_call": "# sol.func_name(head)",
            "go_main_call": "// func_name(head)",
            "rs_main_call": "// Solution::func_name(head);",
            "desc_text": "Given a linked list with head pointer `head`, write an efficient algorithm to solve this problem."
        }
    else:
        return {
            "cpp_args": "int n",
            "py_args": "n: int",
            "go_args": "n int",
            "rs_args": "n: i32",
            "cpp_main_call": "sol.func_name(5);",
            "py_main_call": "sol = Solution()\nprint(sol.func_name(5))",
            "go_main_call": "func_name(5)",
            "rs_main_call": "Solution::func_name(5);",
            "desc_text": "Given an integer `n`, write an efficient algorithm to solve this problem."
        }

async def import_problems():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    print("Reading Excel file...")
    df = pd.read_excel('/Users/mac2/Downloads/FINAL450.xlsx', skiprows=4)
    if len(df.columns) < 2: return
    df.columns = ['Topic', 'ProblemName'] + list(df.columns[2:])
    df = df.dropna(subset=['ProblemName'])
    df['Topic'] = df['Topic'].ffill()
    
    async with AsyncSessionLocal() as session:
        problems_to_add = []
        for index, row in df.iterrows():
            topic = str(row['Topic']).strip()
            title = str(row['ProblemName']).strip()
            func_name = to_camel_case(title)[:30]
            
            ctx = get_topic_context(topic)
            
            cpp_main = ctx['cpp_main_call'].replace('func_name', func_name)
            py_main = ctx['py_main_call'].replace('func_name', func_name)
            go_main = ctx['go_main_call'].replace('func_name', func_name)
            rs_main = ctx['rs_main_call'].replace('func_name', func_name)
            
            starter_code = {
                'cpp': f'#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <string>\nusing namespace std;\n\nclass Solution {{\npublic:\n    void {func_name}({ctx["cpp_args"]}) {{\n        // Write your logic here\n        \n    }}\n}};\n\nint main() {{\n    Solution sol;\n    {cpp_main}\n    cout << "Executed successfully!" << endl;\n    return 0;\n}}',
                'python': f'from typing import List, Optional\n\nclass Solution:\n    def {func_name}(self, {ctx["py_args"]}):\n        pass\n\nif __name__ == "__main__":\n    {py_main}\n    print("Executed successfully!")',
                'go': f'package main\n\nimport "fmt"\n\nfunc {func_name}({ctx["go_args"]}) {{\n    // Write your logic here\n}}\n\nfunc main() {{\n    {go_main}\n    fmt.Println("Executed successfully!")\n}}',
                'rust': f'struct Solution;\n\nimpl Solution {{\n    pub fn {func_name}({ctx["rs_args"]}) {{\n        // Write your logic here\n    }}\n}}\n\nfn main() {{\n    {rs_main}\n    println!("Executed successfully!");\n}}'
            }
            
            description = f"### {title}\n\nThis is a classic problem from the **{topic}** topic.\n\n{ctx['desc_text']}"
            
            examples = [
                {"input": "Generic test case input", "output": "Generic test case output"}
            ]
            
            constraints = ["Standard competitive programming constraints apply.", "Optimize for Time and Space Complexity."]
            
            p = Problem(
                topic=topic,
                title=title,
                description=description,
                starter_code=starter_code,
                examples=examples,
                constraints=constraints,
                time_limit_ms=2000
            )
            problems_to_add.append(p)
            
        session.add_all(problems_to_add)
        await session.commit()
        
    print(f"Successfully generated and imported {len(problems_to_add)} problems.")

if __name__ == "__main__":
    asyncio.run(import_problems())
