import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { validateEmail, validatePassword } from "../utils/validation";
import ErrorAlert from "../components/ErrorAlert";

const EMPTY_FORM = { email: "", username: "", password: "", confirmPassword: "" };

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const emailError = validateEmail(form.email);
    if (emailError) {
      setError(emailError);
      return;
    }
    if (!form.username.trim()) {
      setError("Please choose a username.");
      return;
    }
    const passwordError = validatePassword(form.password, form.confirmPassword);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setIsSubmitting(true);
    const result = await register(form.email, form.username, form.password, form.confirmPassword);
    setIsSubmitting(false);

    if (result.success) {
      navigate("/", { state: { registered: true } });
    } else {
      setError(result.error);
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h1 className="auth-title">Create your account</h1>
        <p className="auth-subtitle">Start tracking income and expenses in minutes.</p>

        <ErrorAlert message={error} onClose={() => setError("")} />

        <label className="form-field">
          <span>Email</span>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
          />
        </label>

        <label className="form-field">
          <span>Username</span>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="yourname"
            required
          />
        </label>

        <div className="form-row">
          <label className="form-field">
            <span>Password</span>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </label>

          <label className="form-field">
            <span>Confirm password</span>
            <input
              type="password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </label>
        </div>

        <button type="submit" className="btn btn-primary btn-block" disabled={isSubmitting}>
          {isSubmitting ? "Creating account..." : "Create account"}
        </button>

        <p className="auth-switch">
          Already have an account? <Link to="/">Log in</Link>
        </p>
      </form>
    </div>
  );
}
