import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../lib/api";

export default function Register() {
  const location = useLocation();

  const [form, setForm] = useState({
    username: "",
    password: "",
    full_name: "",
    role: "PIN",
    date_of_birth: "",
    home_address: "",
    company_name: "",
    company_id: "",
    company_email: "",
    email: "",
  });
  const [msg, setMsg] = useState("");

  // Read ?role=... from the URL and preselect it
  useEffect(() => {
    const role = new URLSearchParams(location.search).get("role");
    if (role) setForm((f) => ({ ...f, role }));
  }, [location.search]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/register/", form);
      setMsg("Registered! You can login now.");
    } catch (e) {
      setMsg("Register failed");
    }
  };

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 420, margin: "40px auto" }}>
      <h3>Create Account</h3>
      <select
        value={form.role}
        onChange={(e) => setForm({ ...form, role: e.target.value })}
      >
        <option value="PIN">Person-in-Need</option>
        <option value="CV">Corporate Volunteer</option>
        <option value="CSR">CSR Representative</option>
        <option value="ADMIN">Platform Admin</option>
      </select>

      <input
        placeholder="Username"
        value={form.username}
        onChange={(e) => setForm({ ...form, username: e.target.value })}
      />
      <input
        placeholder="Password"
        type="password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <input
        placeholder="Full name"
        value={form.full_name}
        onChange={(e) => setForm({ ...form, full_name: e.target.value })}
      />
      <input
        placeholder="Email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />
      <input
        placeholder="DOB (YYYY-MM-DD)"
        value={form.date_of_birth}
        onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })}
      />
      <input
        placeholder="Home Address"
        value={form.home_address}
        onChange={(e) => setForm({ ...form, home_address: e.target.value })}
      />

      {/* Company fields show for CV/CSR */}
      {(form.role === "CV" || form.role === "CSR") && (
        <>
          <input
            placeholder="Company Name"
            value={form.company_name}
            onChange={(e) => setForm({ ...form, company_name: e.target.value })}
          />
          <input
            placeholder="Company ID"
            value={form.company_id}
            onChange={(e) => setForm({ ...form, company_id: e.target.value })}
          />
          <input
            placeholder="Company Email"
            value={form.company_email}
            onChange={(e) =>
              setForm({ ...form, company_email: e.target.value })
            }
          />
        </>
      )}

      <button type="submit">Create Account</button>
      <div>{msg}</div>
    </form>
  );
}
