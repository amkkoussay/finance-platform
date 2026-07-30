import { useState } from "react";
import { CATEGORIES } from "../services/transactions";
import { formatDateForInput } from "../utils/dateFormatter";
import { validateAmount } from "../utils/validation";

const EMPTY_FORM = {
  date: formatDateForInput(),
  category: CATEGORIES[0],
  amount: "",
  description: "",
  is_income: false,
};

export default function TransactionForm({ onSubmit, isSubmitting }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const amountError = validateAmount(form.amount);
    if (amountError) {
      setError(amountError);
      return;
    }

    const result = await onSubmit({ ...form, amount: Number(form.amount) });
    if (result?.success) {
      setForm(EMPTY_FORM);
    } else if (result?.error) {
      setError(result.error);
    }
  }

  return (
    <form className="transaction-form" onSubmit={handleSubmit}>
      <h3 className="form-title">Add transaction</h3>

      {error && <p className="form-error">{error}</p>}

      <div className="form-row">
        <label className="form-field">
          <span>Date</span>
          <input
            type="date"
            name="date"
            value={form.date}
            onChange={handleChange}
            required
          />
        </label>

        <label className="form-field">
          <span>Category</span>
          <select name="category" value={form.category} onChange={handleChange}>
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="form-row">
        <label className="form-field">
          <span>Amount</span>
          <input
            type="number"
            name="amount"
            step="0.01"
            min="0"
            value={form.amount}
            onChange={handleChange}
            placeholder="0.00"
            required
          />
        </label>

        <label className="form-field form-field-checkbox">
          <input
            type="checkbox"
            name="is_income"
            checked={form.is_income}
            onChange={handleChange}
          />
          <span>This is income</span>
        </label>
      </div>

      <label className="form-field">
        <span>Description</span>
        <input
          type="text"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="e.g. Groceries"
        />
      </label>

      <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
        {isSubmitting ? "Adding..." : "Add transaction"}
      </button>
    </form>
  );
}
