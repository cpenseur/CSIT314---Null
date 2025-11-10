import { Link } from "react-router-dom";

// Simple, dependency-light home page that works with your current routes
// - Uses Tailwind classes for styling (safe to keep even if you haven't set up Tailwind yet)
// - Shows role cards linking to Register with a preset role query param
// - Detects if user is logged in (JWT in localStorage) and swaps CTA
// - Keep it minimal so it runs out-of-the-box

// Main function for Home page
export default function Home() {
  const isAuthed = Boolean(localStorage.getItem("access"));

  const roles = [
    { key: "PIN", title: "Person-in-Need (PIN)", desc: "Request assistance and manage appointments.", color: "bg-rose-50", ring: "ring-rose-200" },
    { key: "CV", title: "Corporate Volunteer (CV)", desc: "Accept tasks, chat with PINs, submit claims.", color: "bg-emerald-50", ring: "ring-emerald-200" },
    { key: "CSR", title: "CSR Representative", desc: "Shortlist, match volunteers, monitor requests.", color: "bg-indigo-50", ring: "ring-indigo-200" },
    { key: "ADMIN", title: "Platform Admin", desc: "See analytics, flags, and platform health.", color: "bg-amber-50", ring: "ring-amber-200" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50">
      {/* Nav */}
      <header className="sticky top-0 z-10 bg-white/70 backdrop-blur border-b border-slate-100">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-bold text-xl tracking-tight">SEA‑Wellness / CSR Platform</Link>
          <nav className="flex items-center gap-3">
            <Link to="/login" className="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">Login</Link>
            <Link to="/register" className="px-3 py-1.5 rounded-lg bg-slate-900 text-white hover:bg-slate-800">Create account</Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-4 pt-12 pb-10">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="text-3xl md:text-5xl font-extrabold leading-tight text-slate-900">
              Connect people in need with trusted corporate volunteers
            </h1>
            <p className="mt-4 text-slate-600 md:text-lg">
              Create requests, match the right volunteer, chat safely, and track reimbursements — all in one place.
            </p>
            <div className="mt-6 flex gap-3">
              {isAuthed ? (
                <Link to="/" className="px-5 py-3 rounded-xl bg-emerald-600 text-white hover:bg-emerald-500">
                  Go to Dashboard
                </Link>
              ) : (
                <>
                  <Link to="/register" className="px-5 py-3 rounded-xl bg-emerald-600 text-white hover:bg-emerald-500">Get Started</Link>
                  <Link to="/login" className="px-5 py-3 rounded-xl border border-slate-300 hover:bg-white">I already have an account</Link>
                </>
              )}
            </div>
            <ul className="mt-6 text-slate-600 grid sm:grid-cols-2 gap-y-2 gap-x-6 text-sm">
              <li>• PIN: create & manage service requests</li>
              <li>• CV: accept jobs, check in/out, submit claims</li>
              <li>• CSR: shortlist & match, monitor statuses</li>
              <li>• Admin: analytics, flags, and reports</li>
            </ul>
          </div>
          <div className="md:pl-10">
            <div className="rounded-3xl border border-slate-200 shadow-sm p-6 bg-white">
              <ol className="space-y-4">
                <li className="flex gap-3">
                  <span className="h-7 w-7 rounded-full bg-slate-900 text-white flex items-center justify-center text-sm">1</span>
                  <div>
                    <p className="font-semibold">Sign up and choose your role</p>
                    <p className="text-slate-600 text-sm">PIN, CV, CSR, or Admin.</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="h-7 w-7 rounded-full bg-slate-900 text-white flex items-center justify-center text-sm">2</span>
                  <div>
                    <p className="font-semibold">Do your first action</p>
                    <p className="text-slate-600 text-sm">PIN creates a request, CSR shortlists, CV accepts.</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="h-7 w-7 rounded-full bg-slate-900 text-white flex items-center justify-center text-sm">3</span>
                  <div>
                    <p className="font-semibold">Coordinate and complete</p>
                    <p className="text-slate-600 text-sm">Message, check-in/out, and submit claims if needed.</p>
                  </div>
                </li>
              </ol>
            </div>
          </div>
        </div>
      </section>

      {/* Role cards */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="text-xl md:text-2xl font-bold mb-5">Choose your role</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {roles.map((r) => (
            <Link
              key={r.key}
              to={`/register?role=${r.key}`}
              className={`group rounded-2xl p-5 border ${r.color} ${r.ring} ring-1 hover:shadow transition`}
            >
              <div className="text-2xl">{r.key === "PIN" ? "🫶" : r.key === "CV" ? "🤝" : r.key === "CSR" ? "🧭" : "🛡️"}</div>
              <h3 className="mt-3 font-semibold text-slate-900 group-hover:underline">{r.title}</h3>
              <p className="mt-1 text-sm text-slate-600">{r.desc}</p>
              <span className="inline-block mt-4 text-sm font-medium text-emerald-700 group-hover:translate-x-0.5 transition">Register as {r.key} →</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Feature strip */}
      <section className="bg-white border-t border-slate-200">
        <div className="mx-auto max-w-6xl px-4 py-10 grid md:grid-cols-3 gap-6">
          <div className="rounded-2xl p-5 border border-slate-200">
            <p className="font-semibold">Secure & role-based</p>
            <p className="text-sm text-slate-600 mt-1">JWT auth, role permissions, and OTP for sensitive edits.</p>
          </div>
          <div className="rounded-2xl p-5 border border-slate-200">
            <p className="font-semibold">End-to-end workflow</p>
            <p className="text-sm text-slate-600 mt-1">Requests → matching → messaging → claims → disputes.</p>
          </div>
          <div className="rounded-2xl p-5 border border-slate-200">
            <p className="font-semibold">Built for growth</p>
            <p className="text-sm text-slate-600 mt-1">Plug in email, OCR, analytics, and auto-reassignment later.</p>
          </div>
        </div>
      </section>

      <footer className="text-center text-slate-500 text-sm py-8">
        © {new Date().getFullYear()} SEA‑Wellness / CSR Platform MVP
      </footer>
    </div>
  );
}
