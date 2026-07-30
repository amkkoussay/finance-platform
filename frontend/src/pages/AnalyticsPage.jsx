import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { getByCategory, getMonthly, getSpendingRate } from "../services/analytics";
import { CategoryPieChart, MonthlyLineChart, CategoryBarChart } from "../components/Charts";
import Loading from "../components/Loading";
import ErrorAlert from "../components/ErrorAlert";
import { formatCurrency } from "../utils/formatCurrency";
import { getMonthsRange } from "../utils/dateFormatter";

export default function AnalyticsPage() {
  const { user } = useAuth();
  const months = getMonthsRange(6);

  const [selectedMonth, setSelectedMonth] = useState(months[months.length - 1].value);
  const [categoryData, setCategoryData] = useState({});
  const [monthlyData, setMonthlyData] = useState([]);
  const [spendingRate, setSpendingRate] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadAnalytics() {
      setIsLoading(true);
      setError("");

      const [categoryResult, monthlyResult, rateResult] = await Promise.all([
        getByCategory(user.user_id, selectedMonth),
        getMonthly(user.user_id, 6),
        getSpendingRate(user.user_id, 30),
      ]);

      if (!isMounted) return;

      if (categoryResult.success) setCategoryData(categoryResult.data);
      if (monthlyResult.success) setMonthlyData(monthlyResult.data);
      if (rateResult.success) setSpendingRate(rateResult.rate);

      if (!categoryResult.success) setError(categoryResult.error);

      setIsLoading(false);
    }

    loadAnalytics();
    return () => {
      isMounted = false;
    };
  }, [user.user_id, selectedMonth]);

  return (
    <div className="page">
      <h1 className="page-title">Analytics</h1>
      <p className="page-subtitle">See where your money goes, month over month.</p>

      <ErrorAlert message={error} onClose={() => setError("")} />

      {isLoading ? (
        <Loading label="Loading analytics..." />
      ) : (
        <>
          <div className="analytics-controls">
            <label className="form-field form-field-inline">
              <span>Month</span>
              <select value={selectedMonth} onChange={(e) => setSelectedMonth(e.target.value)}>
                {months.map((m) => (
                  <option key={m.value} value={m.value}>
                    {m.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="analytics-grid">
            <section className="card">
              <div className="card-header">
                <h2>Category breakdown</h2>
              </div>
              <CategoryPieChart data={categoryData} />
            </section>

            <section className="card">
              <div className="card-header">
                <h2>Monthly trend</h2>
              </div>
              <MonthlyLineChart data={monthlyData} />
            </section>

            <section className="card">
              <div className="card-header">
                <h2>Category comparison</h2>
              </div>
              <CategoryBarChart data={categoryData} />
            </section>

            <section className="card">
              <div className="card-header">
                <h2>Spending rate (last 30 days)</h2>
              </div>
              {spendingRate ? (
                <div className="spending-rate">
                  <div>
                    <span className="summary-card-label">Daily average</span>
                    <span className="summary-card-value summary-card-expense">
                      {formatCurrency(spendingRate.daily_average)}
                    </span>
                  </div>
                  <div>
                    <span className="summary-card-label">Total spent</span>
                    <span className="summary-card-value summary-card-expense">
                      {formatCurrency(spendingRate.total_period)}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="empty-state">No spending data available.</p>
              )}
            </section>
          </div>
        </>
      )}
    </div>
  );
}
