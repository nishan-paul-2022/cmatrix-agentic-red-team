"use client";

import { User, Shield, Zap, Globe, BarChart3, Crosshair } from "lucide-react";
import Image from "next/image";

const SuccessStoriesPage = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 selection:bg-emerald-500/30">
      {/* Hero Section */}
      <section className="relative pt-32 pb-24 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_30%_30%,rgba(16,185,129,0.1),transparent)] pointer-events-none" />
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl text-left">
            <h1 className="text-5xl md:text-7xl font-black mb-8 bg-gradient-to-r from-white via-slate-200 to-slate-500 bg-clip-text text-transparent leading-[1.1] animate-in fade-in slide-in-from-bottom-4 duration-1000">
              The Impact of <span className="text-emerald-500">Precision</span> Security
            </h1>
            <p className="text-xl md:text-2xl text-slate-400 mb-12 leading-relaxed max-w-2xl animate-in fade-in slide-in-from-bottom-6 duration-1000 delay-200 text-left">
              See how industry leaders leverage CMatrix to transform complex vulnerabilities into
              strategic advantages.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-10 border-t border-slate-800 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-300">
              <div>
                <p className="text-4xl font-bold text-emerald-500">500+</p>
                <p className="text-xs text-slate-500 uppercase tracking-widest font-bold mt-1">
                  Clients Worldwide
                </p>
              </div>
              <div>
                <p className="text-4xl font-bold text-emerald-500">65%</p>
                <p className="text-xs text-slate-500 uppercase tracking-widest font-bold mt-1">
                  Faster Response
                </p>
              </div>
              <div>
                <p className="text-4xl font-bold text-emerald-500">1M+</p>
                <p className="text-xs text-slate-500 uppercase tracking-widest font-bold mt-1">
                  Patched Threats
                </p>
              </div>
              <div>
                <p className="text-4xl font-bold text-emerald-500">100%</p>
                <p className="text-xs text-slate-500 uppercase tracking-widest font-bold mt-1">
                  Compliance Rate
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Story 1 */}
      <section className="py-24 border-t border-slate-900 bg-slate-900/10">
        <div className="container mx-auto px-6">
          <div className="grid lg:grid-cols-12 gap-16 items-center">
            <div className="lg:col-span-7 space-y-8 text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-bold uppercase tracking-widest">
                <Globe className="w-4 h-4" />
                Enterprise Case Study
              </div>
              <h2 className="text-4xl md:text-5xl font-bold text-white leading-tight">
                Global Tech Solutions <br />
                <span className="text-slate-500">Multinational Defense Strategy</span>
              </h2>
              <div className="text-lg text-slate-400 leading-relaxed space-y-4">
                <p>
                  With 15 global offices and a rapidly expanding cloud footprint, Global Tech
                  Solutions needed a unified orchestration layer to manage their cybersecurity
                  posture across diverse regulatory environments.
                </p>
              </div>

              <div className="grid sm:grid-cols-2 gap-6">
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-emerald-500/30 transition-all group">
                  <div className="text-4xl font-bold text-emerald-500 mb-1">65%</div>
                  <div className="text-sm font-bold text-slate-300 uppercase tracking-tighter">
                    Faster Mitigation
                  </div>
                  <p className="text-xs text-slate-500 mt-2">
                    Reduction in mean-time-to-respond (MTTR) across all critical incidents.
                  </p>
                </div>
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-emerald-500/30 transition-all group">
                  <div className="text-4xl font-bold text-emerald-500 mb-1">42%</div>
                  <div className="text-sm font-bold text-slate-300 uppercase tracking-tighter">
                    Workflow Automation
                  </div>
                  <p className="text-xs text-slate-500 mt-2">
                    Of compliance and monitoring tasks now handled by agentic intelligence.
                  </p>
                </div>
              </div>

              <blockquote className="bg-slate-900/80 border-l-4 border-emerald-500 p-8 rounded-r-2xl shadow-xl">
                <p className="text-xl italic text-slate-200 font-medium mb-6">
                  &quot;CMatrix didn&apos;t just provide a tool; they provided a force multiplier
                  for our global security team. The visibility we have now is unparalleled.&quot;
                </p>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
                    <User className="text-slate-400 w-6 h-6" />
                  </div>
                  <div>
                    <p className="font-bold text-white">Sarah Jenkins</p>
                    <p className="text-xs text-slate-500 uppercase tracking-widest font-bold">
                      Chief Technology Officer
                    </p>
                  </div>
                </div>
              </blockquote>
            </div>

            <div className="lg:col-span-5 relative">
              <div className="absolute -inset-4 bg-emerald-500/20 blur-[100px] rounded-full pointer-events-none" />
              <div className="relative aspect-[3/4] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl group">
                <Image
                  src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop"
                  alt="Security Operations"
                  fill
                  priority
                  className="object-cover transition-transform duration-1000 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-60" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Story 2 */}
      <section className="py-24 bg-slate-950 relative">
        <div className="container mx-auto px-6">
          <div className="grid lg:grid-cols-12 gap-16 items-center">
            <div className="lg:col-span-12 space-y-6 text-center max-w-3xl mx-auto mb-16">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-bold uppercase tracking-widest">
                <Shield className="w-4 h-4" />
                Compliance Mastery
              </div>
              <h2 className="text-4xl md:text-5xl font-bold text-white">
                Swift Financial Services
              </h2>
              <p className="text-lg text-slate-400">
                Facing strict FINRA and SEC regulations, Swift Financial required an airtight,
                verifiable audit trail for every single system interaction.
              </p>
            </div>

            <div className="lg:col-span-6 order-2 lg:order-1">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2 relative rounded-3xl overflow-hidden shadow-2xl h-64 border border-slate-800">
                  <Image
                    src="https://images.unsplash.com/photo-1563986768609-322da13575f3?q=80&w=2070&auto=format&fit=crop"
                    fill
                    className="object-cover opacity-60"
                    alt="Finance security"
                  />
                  <div className="absolute inset-0 flex items-center justify-center bg-slate-950/40">
                    <div className="text-center p-6 bg-slate-900/80 backdrop-blur-md rounded-2xl border border-slate-700">
                      <p className="text-5xl font-black text-white">0</p>
                      <p className="text-xs text-slate-400 uppercase tracking-widest font-black mt-1">
                        Breaches Post-Launch
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-8 rounded-3xl bg-emerald-500 text-slate-950 text-center flex flex-col justify-center shadow-[0_0_30px_rgba(16,185,129,0.2)]">
                  <p className="text-4xl font-black mb-1">100%</p>
                  <p className="text-[10px] font-black uppercase tracking-widest">Audit Accuracy</p>
                </div>
                <div className="p-8 rounded-3xl bg-slate-900 text-white border border-slate-800 text-center flex flex-col justify-center">
                  <p className="text-4xl font-black mb-1">24/7</p>
                  <p className="text-[10px] font-black uppercase tracking-widest">
                    Drift Monitoring
                  </p>
                </div>
              </div>
            </div>

            <div className="lg:col-span-6 order-1 lg:order-2 space-y-8 text-left">
              <ul className="grid gap-6">
                {[
                  {
                    icon: <Zap className="w-5 h-5" />,
                    title: "Instant Access Controls",
                    text: "Granular RBAC implemented across 4,000+ cloud assets in under a week.",
                  },
                  {
                    icon: <BarChart3 className="w-5 h-5" />,
                    title: "Live Auditing",
                    text: "Automated report generation that reduced audit preparation time by 90%.",
                  },
                  {
                    icon: <Crosshair className="w-5 h-5" />,
                    title: "Proactive Hunting",
                    text: "Continuous identification and remediation of shadow IT resources.",
                  },
                ].map((item, idx) => (
                  <li
                    key={idx}
                    className="flex gap-4 p-6 rounded-2xl hover:bg-slate-900/50 transition-colors border border-transparent hover:border-slate-800 group"
                  >
                    <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-emerald-500 border border-slate-800 group-hover:bg-emerald-500 group-hover:text-slate-950 transition-all">
                      {item.icon}
                    </div>
                    <div>
                      <p className="font-bold text-white text-lg mb-1">{item.title}</p>
                      <p className="text-sm text-slate-400 leading-relaxed">{item.text}</p>
                    </div>
                  </li>
                ))}
              </ul>

              <button className="bg-white text-slate-950 hover:bg-slate-200 px-10 py-5 rounded-2xl font-black text-xl transition-all shadow-xl w-full sm:w-auto">
                Read Detailed PDF
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 bg-slate-900/20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-white mb-16">Trusted by the Best</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Marcus Voe",
                role: "DevOps Engineer",
                quote:
                  "The interface is simply the best I&apos;ve encountered in three decades. It makes complex security data approachable.",
                company: "CloudWare",
              },
              {
                name: "Lina Chen",
                role: "Product Manager",
                quote:
                  "It reduced our project turnaround by half. We&apos;re launching twice as fast with 100% confidence.",
                company: "Innovate Labs",
              },
              {
                name: "David Smith",
                role: "Security Consultant",
                quote:
                  "Essential for any serious red-teaming operation. The automation tools are absolute top tier.",
                company: "CyberArmor",
              },
            ].map((user, i) => (
              <div
                key={i}
                className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 text-left hover:-translate-y-2 transition-all duration-300"
              >
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/20">
                    <User className="text-emerald-500 w-5 h-5" />
                  </div>
                  <div>
                    <p className="font-bold text-white text-sm">{user.name}</p>
                    <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest">
                      {user.role} @ {user.company}
                    </p>
                  </div>
                </div>
                <p className="text-slate-400 italic text-sm leading-relaxed">
                  &quot;{user.quote}&quot;
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Bottom */}
      <section className="py-32 relative overflow-hidden bg-emerald-500">
        <div className="container mx-auto px-6 text-center relative z-10">
          <h2 className="text-5xl md:text-6xl font-black text-slate-950 mb-6 drop-shadow-sm">
            Ready to secure <br className="hidden md:block" />
            your next success?
          </h2>
          <p className="text-xl text-slate-900/80 mb-12 max-w-xl mx-auto font-medium">
            Contact our engineering team today for a tailored security assessment and implementation
            plan.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-slate-950 text-white font-black px-12 py-6 rounded-2xl text-xl hover:scale-105 active:scale-95 transition-all shadow-2xl">
              Book a Strategy Call
            </button>
            <button className="bg-transparent border-2 border-slate-950 text-slate-950 font-bold px-12 py-6 rounded-2xl text-xl hover:bg-slate-950 hover:text-white transition-all">
              Live Demo
            </button>
          </div>
        </div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/20 blur-[80px] -mr-32 -mt-32 rounded-full" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-slate-950/10 blur-[100px] -ml-40 -mb-40 rounded-full" />
      </section>
    </div>
  );
};

export default SuccessStoriesPage;
