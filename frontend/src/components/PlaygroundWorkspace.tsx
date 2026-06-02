"use client";

import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Settings, List, Code2, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import api from "@/lib/api";

const DEFAULT_SNIPPETS: Record<string, string> = {
  'cpp': '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, CodeForge Playground!" << endl;\n    return 0;\n}',
  'python': 'def main():\n    print("Hello, CodeForge Playground!")\n\nif __name__ == "__main__":\n    main()',
  'go': 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, CodeForge Playground!")\n}',
  'rust': 'fn main() {\n    println!("Hello, CodeForge Playground!");\n}',
  'javascript': 'function main() {\n    console.log("Hello, CodeForge Playground!");\n}\n\nmain();'
};

export default function PlaygroundWorkspace() {
  const [selectedLanguage, setSelectedLanguage] = useState('cpp');
  const [code, setCode] = useState(DEFAULT_SNIPPETS['cpp']);
  const [output, setOutput] = useState("");
  const [executionStatus, setExecutionStatus] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [consoleTab, setConsoleTab] = useState('console');
  const [executionTime, setExecutionTime] = useState<number | null>(null);

  useEffect(() => {
    const autoLogin = async () => {
      try {
        if (!localStorage.getItem("access_token")) {
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
        }
      } catch (err) {
        console.error("Auto login failed", err);
      }
    };
    autoLogin();
  }, []);

  const handleLanguageChange = (lang: string) => {
    setSelectedLanguage(lang);
    setCode(DEFAULT_SNIPPETS[lang]);
  };

  const handleRun = async () => {
    setIsExecuting(true);
    setOutput("Compiling and running...");
    setConsoleTab('console');
    setExecutionStatus(null);
    setExecutionTime(null);
    
    try {
      const res = await api.post("/execute", {
        language: selectedLanguage,
        code,
        action: 'run'
      });
      setOutput(res.data.output);
      setExecutionStatus(res.data.status);
      setExecutionTime(res.data.execution_time);
    } catch (err: any) {
      setOutput(err.response?.data?.detail || "Execution failed");
      setExecutionStatus("error");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="h-screen w-full flex flex-col bg-[#1a1a1a] text-[#bfbfbf] font-sans">
      {/* Top Navbar */}
      <div className="h-12 border-b border-[#333] flex items-center justify-between px-4 bg-[#282828]">
        <div className="flex items-center gap-4">
          <Link href="/">
            <div className="font-bold text-lg text-white flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
              <Code2 className="text-orange-500" />
              CodeForge Playground
            </div>
          </Link>
          <Link href="/problems">
            <div className="flex items-center gap-2 text-sm bg-[#333] px-3 py-1.5 rounded-md text-zinc-300 font-semibold cursor-pointer hover:bg-[#444] transition-colors">
              <List size={16}/> Problem List
            </div>
          </Link>
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={handleRun} 
            disabled={isExecuting}
            className="bg-green-600 hover:bg-green-700 text-white gap-2 h-8 font-semibold px-6"
          >
            <Play size={14} className="text-white fill-white" /> Run Code
          </Button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 p-4 flex flex-col min-w-0 max-w-7xl mx-auto w-full gap-4">
        
        {/* Editor */}
        <div className="flex-[2] bg-[#282828] rounded-lg border border-[#333] flex flex-col min-h-0 min-w-0 overflow-hidden relative shadow-lg shadow-black/20">
          {/* Editor Header */}
          <div className="h-12 bg-[#282828] border-b border-[#333] flex items-center px-4 shrink-0 justify-between">
            <div className="flex gap-3 items-center">
              <Terminal size={16} className="text-orange-400" />
              <span className="font-bold text-white text-sm">Editor</span>
              <div className="h-4 w-[1px] bg-[#444] mx-2"></div>
              <select 
                className="bg-[#333] text-sm font-semibold text-white outline-none cursor-pointer px-3 py-1.5 rounded-md hover:bg-[#444] transition-colors"
                value={selectedLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
              >
                <option value="cpp">C++</option>
                <option value="python">Python</option>
                <option value="go">Go</option>
                <option value="rust">Rust</option>
                <option value="javascript">JavaScript</option>
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
                options={{ minimap: { enabled: false }, fontSize: 15, scrollBeyondLastLine: false, padding: { top: 16 } }}
              />
            </div>
          </div>
        </div>

        {/* Console Output */}
        <div className="flex-1 bg-[#282828] rounded-lg border border-[#333] flex flex-col overflow-hidden shadow-lg shadow-black/20">
          <div className="bg-[#2d2d2d] border-b border-[#333] p-3 flex items-center justify-between">
            <div className="flex items-center gap-2 font-bold text-white text-sm">
              <Terminal size={16} /> Console Output
            </div>
            {executionTime !== null && (
              <div className="text-xs font-mono text-zinc-400">
                Execution Time: {(executionTime * 1000).toFixed(0)} ms
              </div>
            )}
          </div>
          <div className="p-4 flex-1 overflow-auto font-mono text-sm bg-[#1e1e1e] text-zinc-300 whitespace-pre-wrap">
            {executionStatus && executionStatus !== 'Accepted' && (
              <div className="mb-4 text-red-400 font-bold">
                Status: {executionStatus}
              </div>
            )}
            {output || (
              <div className="text-zinc-500 italic flex h-full items-center justify-center">
                Click "Run Code" to see the output here...
              </div>
            )}
          </div>
        </div>
        
      </div>
    </div>
  );
}
