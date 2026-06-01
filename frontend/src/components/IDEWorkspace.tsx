"use client";

import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Settings, List, Code2, Beaker, FileText, Star, Share2, ThumbsUp, ThumbsDown, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import api from "@/lib/api";
import ReactMarkdown from 'react-markdown';

const DEFAULT_SNIPPETS: Record<string, string> = {
  'cpp': '#include <iostream>\nusing namespace std;\n\nbool isAnswer(vector<int>& position, int m, int mid) {\n    // Write your logic here\n    return true;\n}\n\nint main() {\n    cout << "Ready to solve!" << endl;\n    return 0;\n}',
  'python': 'class Solution:\n    def solve(self) -> int:\n        pass\n\nprint("Ready to solve!")',
  'go': 'package main\n\nimport "fmt"\n\nfunc solve() int {\n    return 0\n}\n\nfunc main() {\n    fmt.Println("Ready to solve!")\n}',
  'rust': 'impl Solution {\n    pub fn solve() -> i32 {\n        0\n    }\n}\n\nfn main() {\n    println!("Ready to solve!");\n}'
};

export default function IDEWorkspace({ projectId }: { projectId?: string }) {
  const [selectedLanguage, setSelectedLanguage] = useState('cpp');
  const [code, setCode] = useState(DEFAULT_SNIPPETS['cpp']);
  const [output, setOutput] = useState("");
  const [isExecuting, setIsExecuting] = useState(false);
  const [activeTab, setActiveTab] = useState('description');
  const [problem, setProblem] = useState<any>(null);

  useEffect(() => {
    const autoLogin = async () => {
      try {
        localStorage.removeItem("access_token");
        try {
          await api.post("/auth/register", { email: "demo@codeforge.com", password: "password", name: "Demo User" });
        } catch (e) { /* ignore */ }
        
        const form = new URLSearchParams();
        form.append('username', 'demo@codeforge.com');
        form.append('password', 'password');
        const res = await api.post("/auth/login", form, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        localStorage.setItem("access_token", res.data.access_token);
      } catch (err) {
        console.error("Auto login failed", err);
      }
    };
    autoLogin().then(() => {
      if (projectId && projectId !== 'demo') {
        api.get(`/problems/${projectId}`).then(res => {
          setProblem(res.data);
        }).catch(err => console.error("Failed to fetch problem", err));
      } else {
        // Fallback for demo mode
        setProblem({
          title: "1552. Magnetic Force Between Two Balls",
          topic: "Array",
          difficulty: "Medium",
          description: "In the universe Earth C-137, Rick discovered a special form of magnetic force between two balls if they are put in his new invented basket. Rick has `n` empty baskets, the `i-th` basket is at `position[i]`, Morty has `m` balls and needs to distribute the balls into the baskets such that the **minimum magnetic force** between any two balls is **maximum**.\n\nRick stated that magnetic force between two different balls at positions `x` and `y` is `|x - y|`.\n\nGiven the integer array `position` and the integer `m`. Return *the required force*.",
          likes: 1800,
          dislikes: 100
        });
      }
    });
  }, [projectId]);

  const handleLanguageChange = (lang: string) => {
    setSelectedLanguage(lang);
    setCode(DEFAULT_SNIPPETS[lang]);
  };

  const handleExecute = async () => {
    setIsExecuting(true);
    setOutput("Executing...");
    
    try {
      const res = await api.post("/execute/", {
        language: selectedLanguage,
        code: code
      });
      setOutput(res.data.output + `\n\n[Finished in ${res.data.execution_time}s]`);
    } catch (error: any) {
      setOutput(error.response?.data?.detail || "Execution failed.");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="h-screen w-full flex flex-col bg-[#1a1a1a] text-[#bfbfbf] font-sans">
      {/* Top Navbar */}
      <div className="h-12 border-b border-[#333] flex items-center justify-between px-4 bg-[#282828]">
        <div className="flex items-center gap-4">
          <div className="font-bold text-lg text-white flex items-center gap-2">
            <Code2 className="text-orange-500" />
            CodeForge
          </div>
          <Link href="/problems">
            <div className="flex items-center gap-2 text-sm bg-[#333] px-3 py-1.5 rounded-md text-zinc-300 font-semibold cursor-pointer hover:bg-[#444] transition-colors">
              <List size={16}/> Problem List
            </div>
          </Link>
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={handleExecute} 
            disabled={isExecuting}
            variant="ghost"
            className="hover:bg-[#333] text-zinc-300 gap-2 h-8"
          >
            <Play size={14} className="text-green-500 fill-green-500" /> Run
          </Button>
          <Button 
            className="bg-green-600 hover:bg-green-700 text-white gap-2 h-8 font-semibold px-6"
          >
            Submit
          </Button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 p-2 flex overflow-hidden gap-2">
        {/* Left Panel: Problem Description */}
        <div className="w-1/2 bg-[#282828] rounded-lg border border-[#333] flex flex-col min-w-0">
          {/* Tabs */}
          <div className="flex bg-[#282828] border-b border-[#333] px-2 rounded-t-lg shrink-0">
            <button className={`px-4 py-2.5 text-sm font-semibold border-b-2 flex items-center gap-2 ${activeTab === 'description' ? 'border-white text-white' : 'border-transparent hover:text-white'}`} onClick={() => setActiveTab('description')}><FileText size={16} />Description</button>
            <button className={`px-4 py-2.5 text-sm font-semibold border-b-2 flex items-center gap-2 ${activeTab === 'editorial' ? 'border-white text-white' : 'border-transparent hover:text-white'}`} onClick={() => setActiveTab('editorial')}><Beaker size={16} />Editorial</button>
            <button className={`px-4 py-2.5 text-sm font-semibold border-b-2 ${activeTab === 'solutions' ? 'border-white text-white' : 'border-transparent hover:text-white'}`} onClick={() => setActiveTab('solutions')}>Solutions</button>
            <button className={`px-4 py-2.5 text-sm font-semibold border-b-2 ${activeTab === 'submissions' ? 'border-white text-white' : 'border-transparent hover:text-white'}`} onClick={() => setActiveTab('submissions')}>Submissions</button>
          </div>
          
          {/* Content */}
          <div className="p-6 overflow-y-auto flex-1 text-[15px] leading-relaxed custom-scrollbar">
            {!problem ? (
              <div className="text-zinc-500">Loading problem...</div>
            ) : (
              <>
                <h1 className="text-[22px] font-bold text-white mb-4">{problem.title}</h1>
                <div className="flex gap-4 mb-8 items-center text-[13px]">
                  <span className="bg-[#333] text-orange-400 px-3 py-1 rounded-full font-bold">{problem.difficulty}</span>
                  <span className="bg-[#1e1e1e] border border-[#333] text-zinc-400 px-3 py-1 rounded-full font-semibold">{problem.topic}</span>
                  <span className="flex items-center gap-1.5 hover:text-white cursor-pointer transition-colors ml-2"><ThumbsUp size={14} className="text-zinc-400" /> {problem.likes}</span>
                  <span className="flex items-center gap-1.5 hover:text-white cursor-pointer transition-colors"><ThumbsDown size={14} className="text-zinc-400" /> {problem.dislikes}</span>
                  <Star size={16} className="text-zinc-400 hover:text-white cursor-pointer transition-colors"/>
                  <Share2 size={16} className="text-zinc-400 hover:text-white cursor-pointer transition-colors"/>
                </div>
                
                <div className="space-y-5 text-zinc-300 prose prose-invert max-w-none">
                  <ReactMarkdown>{problem.description}</ReactMarkdown>
                </div>
              </>
            )}
          </div>
        </div>
        
        {/* Right Panel: Editor and Console */}
        <div className="w-1/2 flex flex-col gap-2 min-w-0">
          {/* Editor */}
          <div className="h-[70%] bg-[#282828] rounded-lg border border-[#333] flex flex-col min-h-0 min-w-0 overflow-hidden relative">
            {/* Editor Header */}
            <div className="h-10 bg-[#282828] border-b border-[#333] flex items-center px-4 shrink-0 justify-between">
              <div className="flex gap-2">
                <select 
                  className="bg-[#333] text-sm font-semibold text-white outline-none cursor-pointer px-2 py-1 rounded"
                  value={selectedLanguage}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                >
                  <option value="cpp">C++</option>
                  <option value="python">Python</option>
                  <option value="go">Go</option>
                  <option value="rust">Rust</option>
                </select>
              </div>
              <div className="flex items-center gap-4 text-zinc-400">
                <span className="text-xs font-semibold cursor-pointer hover:text-white transition-colors">Format</span>
                <Settings size={14} className="cursor-pointer hover:text-white transition-colors" />
              </div>
            </div>
            <div className="flex-1 w-full h-full relative">
              <div className="absolute inset-0">
                <Editor
                  height="100%"
                  width="100%"
                  language={selectedLanguage}
                  theme="vs-dark"
                  value={code}
                  onChange={(val) => setCode(val || "")}
                  options={{ minimap: { enabled: false }, fontSize: 14, scrollBeyondLastLine: false, padding: { top: 16 } }}
                />
              </div>
            </div>
          </div>

          {/* Console Output */}
          <div className="h-[30%] bg-[#282828] rounded-lg border border-[#333] flex flex-col overflow-hidden">
            <div className="h-10 border-b border-[#333] bg-[#282828] flex items-center px-4 text-sm font-semibold gap-6 text-zinc-400 shrink-0">
              <button className="flex items-center gap-2 hover:text-white text-white border-b-2 border-white h-full px-1">
                <Terminal size={14} /> Testcases
              </button>
              <button className="flex items-center gap-2 hover:text-white h-full px-1">
                Test Result
              </button>
            </div>
            <div className="flex-1 p-4 font-mono text-sm overflow-auto whitespace-pre-wrap text-[#4ade80]">
              {output || "Run code to see output..."}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
