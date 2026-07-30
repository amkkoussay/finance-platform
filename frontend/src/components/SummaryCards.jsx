import { formatCurrency } from "../utils/formatCurrency";

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  const cards = [
    { label: "Total Income", value: summary.total_income, tone: "income" },
    { label: "Total Expense", value: summary.total_expense, tone: "expense" },
    { label: "Balance", value: summary.balance, tone: summary.balance >= 0 ? "income" : "expense" },
    {
      label: "Transactions",
      value: summary.transaction_count,
      tone: "neutral",
      raw: true,
    },
  ];

  return (
    <div className="summary-cards">
      {cards.map((card) => (
        <div className="summary-card" key={card.label}>
          <span className="summary-card-label">{card.label}</span>
          <span className={`summary-card-value summary-card-${card.tone}`}>
            {card.raw ? card.value : formatCurrency(card.value)}
          </span>
        </div>
      ))}
    </div>
  );
}
