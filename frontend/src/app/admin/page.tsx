"use client";

import { useState } from "react";
import { Upload, Plus, Edit, Trash, Server, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import api from "@/lib/api";

export default function AdminDashboard() {
  const [jsonInput, setJsonInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const handleBulkImport = async () => {
    setLoading(true);
    setStatus(null);
    try {
      const data = JSON.parse(jsonInput);
      const res = await api.post("/admin/bulk-import", data);
      setStatus(res.data.message);
      setJsonInput("");
    } catch (err: any) {
      setStatus(`Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#121212] text-[#bfbfbf] p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Server className="text-orange-500" />
            CodeForge Admin Dashboard
          </h1>
          <Link href="/">
            <Button variant="ghost" className="text-zinc-400 hover:text-white">Back to App</Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-[#1e1e1e] p-6 rounded-xl border border-[#333]">
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-blue-500/20 text-blue-500 rounded-lg"><Activity size={24} /></div>
              <h3 className="text-lg font-bold text-white">System Status</h3>
            </div>
            <p className="text-sm text-zinc-400 ml-16">Online Judging Engine: <span className="text-green-500 font-bold">Active</span></p>
            <p className="text-sm text-zinc-400 ml-16 mt-1">Docker Containers: <span className="text-green-500 font-bold">Healthy</span></p>
          </div>
          <div className="bg-[#1e1e1e] p-6 rounded-xl border border-[#333]">
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-orange-500/20 text-orange-500 rounded-lg"><Edit size={24} /></div>
              <h3 className="text-lg font-bold text-white">Manage Problems</h3>
            </div>
            <div className="ml-16 space-x-2 mt-2">
              <Button size="sm" className="bg-[#333] hover:bg-[#444] text-white">View All</Button>
              <Button size="sm" className="bg-orange-600 hover:bg-orange-700 text-white"><Plus size={14} className="mr-1"/> Create</Button>
            </div>
          </div>
          <div className="bg-[#1e1e1e] p-6 rounded-xl border border-[#333]">
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-purple-500/20 text-purple-500 rounded-lg"><Trash size={24} /></div>
              <h3 className="text-lg font-bold text-white">Maintenance</h3>
            </div>
            <p className="text-sm text-zinc-400 ml-16">Clear isolated containers and zombie processes.</p>
          </div>
        </div>

        <div className="bg-[#1e1e1e] p-8 rounded-xl border border-[#333]">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2 mb-6">
            <Upload className="text-zinc-400" />
            Bulk Import Tool (JSON)
          </h2>
          
          <div className="mb-4">
            <p className="text-sm text-zinc-400 mb-2">
              Paste your standard JSON array of Problem objects here. It must include `visible_test_cases` and `hidden_test_cases`.
            </p>
            <textarea 
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
              className="w-full h-64 bg-[#121212] border border-[#333] rounded-lg p-4 font-mono text-sm text-zinc-300 focus:outline-none focus:border-orange-500 transition-colors"
              placeholder='{ "problems": [ { "title": "...", "visible_test_cases": [...], "hidden_test_cases": [...] } ] }'
            ></textarea>
          </div>
          
          <div className="flex items-center gap-4">
            <Button 
              onClick={handleBulkImport} 
              disabled={loading || !jsonInput.trim()}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              {loading ? "Importing..." : "Run Bulk Import"}
            </Button>
            {status && (
              <span className={`text-sm font-semibold ${status.startsWith('Error') ? 'text-red-500' : 'text-green-500'}`}>
                {status}
              </span>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
