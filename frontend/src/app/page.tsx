import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Terminal, Code2, Zap, Shield, Globe } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white selection:bg-emerald-500/30">
      {/* Navigation */}
      <nav className="border-b border-zinc-800/50 bg-zinc-950/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="text-emerald-400" />
            <span className="font-bold text-xl tracking-tight">CodeForge</span>
          </div>
          <div className="flex gap-4">
            <Button variant="ghost" className="text-zinc-300 hover:text-white">Log in</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">Get Started</Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-900/20 via-zinc-950 to-zinc-950"></div>
        <div className="max-w-5xl mx-auto px-4 text-center relative z-10">
          <div className="inline-flex items-center rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-300 mb-8">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            Execution Engine v2.0 is now live
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-clip-text text-transparent bg-gradient-to-b from-white to-zinc-400">
            The Cloud IDE for <br /> Modern Developers
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Write, run, and scale your code instantly. An enterprise-grade execution platform with isolated Docker sandboxing and sub-second latency.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/ide/demo">
              <Button size="lg" className="h-14 px-8 text-lg bg-emerald-600 hover:bg-emerald-700 w-full sm:w-auto shadow-[0_0_40px_-10px_rgba(16,185,129,0.5)]">
                Start Coding for Free
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="h-14 px-8 text-lg border-zinc-700 hover:bg-zinc-800 w-full sm:w-auto">
              View Documentation
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 border-t border-zinc-800/50 bg-zinc-950">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Everything you need to ship faster</h2>
            <p className="text-zinc-400">Built for scale, designed for speed.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Code2 className="h-6 w-6 text-emerald-400" />,
                title: "Monaco Editor Integration",
                description: "Experience the same power as VS Code right in your browser. Complete with syntax highlighting and intelligent auto-completion."
              },
              {
                icon: <Shield className="h-6 w-6 text-emerald-400" />,
                title: "Secure Docker Sandboxes",
                description: "Every execution runs in a pristine, isolated Docker container ensuring maximum security and zero cross-contamination."
              },
              {
                icon: <Zap className="h-6 w-6 text-emerald-400" />,
                title: "Sub-second Execution",
                description: "Our container pooling technology ensures your code starts executing in milliseconds, not seconds."
              }
            ].map((feature, i) => (
              <div key={i} className="p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800 hover:border-emerald-500/50 transition-colors">
                <div className="h-12 w-12 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-zinc-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
