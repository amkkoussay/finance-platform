import { formatCurrency } from "../utils/formatCurrency";
import { formatDate } from "../utils/dateFormatter";

export default function TransactionTable({ transactions, onDelete }) {
  if (!transactions || transactions.length === 0) {
    return <p className="empty-state">No transactions yet. Add your first one above.</p>;
  }

  return (
    <div className="table-wrapper">
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Type</th>
            <th aria-label="Actions" />
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.id}>
              <td>{formatDate(txn.date)}</td>
              <td className="capitalize">{txn.category}</td>
              <td className={txn.is_income ? "text-income" : "text-expense"}>
                {formatCurrency(txn.amount)}
              </td>
              <td>{txn.description || "—"}</td>
              <td>
                <span className={`badge ${txn.is_income ? "badge-income" : "badge-expense"}`}>
                  {txn.is_income ? "Income" : "Expense"}
                </span>
              </td>
              <td>
                <button
                  type="button"
                  className="btn btn-danger-ghost"
                  onClick={() => onDelete(txn.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
