import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Terminal, Settings, CreditCard, Activity } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight text-emerald-400">Dashboard</h1>
          <Button className="bg-emerald-600 hover:bg-emerald-700">New Project</Button>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="bg-zinc-900 border-zinc-800 text-white">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">Total Executions</CardTitle>
              <Terminal className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,248</div>
              <p className="text-xs text-zinc-500">+12% from last month</p>
            </CardContent>
          </Card>
          
          <Card className="bg-zinc-900 border-zinc-800 text-white">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">Active Projects</CardTitle>
              <Activity className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">7</div>
            </CardContent>
          </Card>
        </div>

        <h2 className="text-xl font-semibold mt-12 mb-4">Recent Projects</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {/* Example static projects for UI visualization */}
          <Card className="bg-zinc-900 border-zinc-800 text-white hover:border-emerald-500 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle>Data Analysis Script</CardTitle>
              <CardDescription className="text-zinc-400">Python • Updated 2h ago</CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800 text-white hover:border-emerald-500 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle>Express.js Server</CardTitle>
              <CardDescription className="text-zinc-400">Node.js • Updated 1d ago</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    </div>
  );
}
