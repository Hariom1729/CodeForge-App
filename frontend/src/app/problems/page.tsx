"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import Link from "next/link";
import { Code2, Search, CheckCircle2, Terminal } from "lucide-react";

export default function ProblemList() {
  const [problems, setProblems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("All");

  // Extract unique topics for the filter dropdown
  const topics = ["All", ...Array.from(new Set(problems.map(p => p.topic))).sort()];

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const res = await api.get("/problems");
        setProblems(res.data);
      } catch (err) {
        console.error("Failed to fetch problems", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProblems();
  }, []);

  const filteredProblems = problems.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(search.toLowerCase()) || p.topic.toLowerCase().includes(search.toLowerCase());
    const matchesTopic = selectedTopic === "All" || p.topic === selectedTopic;
    return matchesSearch && matchesTopic;
  });

  return (
    <div className="min-h-screen bg-[#1a1a1a] text-zinc-300 font-sans">
      {/* Top Navbar */}
      <div className="h-14 border-b border-[#333] flex items-center justify-between px-8 bg-[#282828]">
        <Link href="/">
          <div className="font-bold text-xl text-white flex items-center gap-2 cursor-pointer">
            <Code2 className="text-orange-500" />
            CodeForge
          </div>
        </Link>
        <Link href="/playground">
          <div className="flex items-center gap-2 text-sm bg-[#333] px-4 py-2 rounded-md text-zinc-300 font-semibold cursor-pointer hover:bg-[#444] transition-colors">
            <Terminal size={16}/> Playground
          </div>
        </Link>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-white">Problem List</h1>
          <div className="flex gap-4">
            <select
              className="bg-[#282828] border border-[#333] rounded-md px-4 py-2 text-sm text-white focus:outline-none focus:border-zinc-500 transition-colors cursor-pointer"
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
            >
              {topics.map(topic => (
                <option key={topic} value={topic}>{topic}</option>
              ))}
            </select>
            <div className="relative">
              <Search className="absolute left-3 top-2.5 text-zinc-500" size={18} />
              <input 
                type="text" 
                placeholder="Search problems..." 
                className="bg-[#282828] border border-[#333] rounded-md pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-zinc-500 w-64 transition-colors"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-20 text-zinc-500">Loading 450 problems...</div>
        ) : (
          <div className="bg-[#282828] rounded-xl border border-[#333] overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#333] text-zinc-400 text-sm">
                  <th className="py-4 px-6 font-semibold w-16">Status</th>
                  <th className="py-4 px-6 font-semibold">Title</th>
                  <th className="py-4 px-6 font-semibold">Topic</th>
                  <th className="py-4 px-6 font-semibold w-24">Difficulty</th>
                </tr>
              </thead>
              <tbody>
                {filteredProblems.map((problem, index) => (
                  <tr key={problem.id} className="border-b border-[#333]/50 hover:bg-[#333]/50 transition-colors group">
                    <td className="py-4 px-6">
                      {/* Fake status icon for UI flair */}
                      <CheckCircle2 size={18} className="text-zinc-600 group-hover:text-zinc-500" />
                    </td>
                    <td className="py-4 px-6">
                      <Link href={`/ide/${problem.id}`} className="text-zinc-200 hover:text-white hover:underline font-medium">
                        {index + 1}. {problem.title}
                      </Link>
                    </td>
                    <td className="py-4 px-6">
                      <span className="bg-[#1e1e1e] border border-[#333] text-xs px-2.5 py-1 rounded-full text-zinc-400">
                        {problem.topic}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <span className="text-orange-400 font-medium text-sm">{problem.difficulty}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filteredProblems.length === 0 && (
              <div className="text-center py-20 text-zinc-500">No problems found matching your search.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
