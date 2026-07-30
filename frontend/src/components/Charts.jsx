import {
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { formatCurrency } from "../utils/formatCurrency";

const PALETTE = ["#2F80ED", "#1B998B", "#E0503A", "#F2C94C", "#9B51E0", "#556270"];

export function CategoryPieChart({ data }) {
  const entries = Object.entries(data || {}).map(([name, value]) => ({ name, value }));

  if (entries.length === 0) {
    return <p className="empty-state">No expenses recorded for this month yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={entries}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={95}
          label={({ name }) => name}
        >
          {entries.map((entry, index) => (
            <Cell key={entry.name} fill={PALETTE[index % PALETTE.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => formatCurrency(value)} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function MonthlyLineChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="empty-state">No monthly data yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
        <XAxis dataKey="month" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip formatter={(value) => formatCurrency(value)} />
        <Line type="monotone" dataKey="total" stroke="#2F80ED" strokeWidth={2.5} dot={{ r: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function CategoryBarChart({ data }) {
  const entries = Object.entries(data || {}).map(([name, value]) => ({ name, value }));

  if (entries.length === 0) {
    return <p className="empty-state">No expenses recorded for this month yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={entries}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip formatter={(value) => formatCurrency(value)} />
        <Bar dataKey="value" fill="#1B998B" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
