import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getSummary } from "../services/analytics";
import { getTransactions } from "../services/transactions";
import SummaryCards from "../components/SummaryCards";
import Loading from "../components/Loading";
import ErrorAlert from "../components/ErrorAlert";
import { formatCurrency } from "../utils/formatCurrency";
import { formatDate } from "../utils/dateFormatter";

export default function DashboardPage() {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard() {
      setIsLoading(true);
      setError("");

      const [summaryResult, transactionsResult] = await Promise.all([
        getSummary(user.user_id),
        getTransactions(user.user_id),
      ]);

      if (!isMounted) return;

      if (summaryResult.success) {
        setSummary(summaryResult.summary);
      } else {
        setError(summaryResult.error);
      }

      if (transactionsResult.success) {
        setRecentTransactions(transactionsResult.transactions.slice(0, 5));
      }

      setIsLoading(false);
    }

    loadDashboard();
    return () => {
      isMounted = false;
    };
  }, [user.user_id]);

  return (
    <div className="page">
      <h1 className="page-title">Welcome back, {user.username}</h1>
      <p className="page-subtitle">Here&apos;s where your money stands today.</p>

      <ErrorAlert message={error} onClose={() => setError("")} />

      {isLoading ? (
        <Loading label="Loading your dashboard..." />
      ) : (
        <>
          <SummaryCards summary={summary} />

          <div className="dashboard-grid">
            <section className="card">
              <div className="card-header">
                <h2>Recent transactions</h2>
                <Link to="/transactions" className="link">
                  View all
                </Link>
              </div>

              {recentTransactions.length === 0 ? (
                <p className="empty-state">No transactions yet.</p>
              ) : (
                <ul className="recent-list">
                  {recentTransactions.map((txn) => (
                    <li key={txn.id} className="recent-list-item">
                      <div>
                        <span className="recent-list-category capitalize">{txn.category}</span>
                        <span className="recent-list-date">{formatDate(txn.date)}</span>
                      </div>
                      <span className={txn.is_income ? "text-income" : "text-expense"}>
                        {formatCurrency(txn.amount)}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section className="card">
              <div className="card-header">
                <h2>Quick actions</h2>
              </div>
              <div className="quick-actions">
                <Link to="/transactions" className="btn btn-primary">
                  Add transaction
                </Link>
                <Link to="/analytics" className="btn btn-secondary">
                  View analytics
                </Link>
              </div>
            </section>
          </div>
        </>
      )}
    </div>
  );
}
