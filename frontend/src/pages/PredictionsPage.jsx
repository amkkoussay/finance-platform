import { useEffect, useState } from "react";
import {
  getMonthlyForecast,
  getCategoryForecast,
  getRecommendations,
} from "../services/predictions";
import { CATEGORIES } from "../services/transactions";
import { MonthlyLineChart } from "../components/Charts";
import TrendBadge from "../components/TrendBadge";
import Loading from "../components/Loading";
import ErrorAlert from "../components/ErrorAlert";
import { formatCurrency } from "../utils/formatCurrency";

const FORECASTABLE_CATEGORIES = CATEGORIES.filter((c) => c !== "salary");

export default function PredictionsPage() {
  const [selectedCategory, setSelectedCategory] = useState(FORECASTABLE_CATEGORIES[0]);

  const [monthlyForecast, setMonthlyForecast] = useState(null);
  const [categoryForecast, setCategoryForecast] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const [isLoading, setIsLoading] = useState(true);
  const [isCategoryLoading, setIsCategoryLoading] = useState(true);
  const [error, setError] = useState("");

  // Monthly forecast + recommendations load once.
  useEffect(() => {
    let isMounted = true;

    async function load() {
      setIsLoading(true);
      setError("");

      const [monthlyResult, recsResult] = await Promise.all([
        getMonthlyForecast(),
        getRecommendations(10),
      ]);

      if (!isMounted) return;

      if (monthlyResult.success) setMonthlyForecast(monthlyResult.forecast);
      else setError(monthlyResult.error);

      if (recsResult.success) setRecommendations(recsResult.recommendations);

      setIsLoading(false);
    }

    load();
    return () => {
      isMounted = false;
    };
  }, []);

  // Category forecast reloads whenever the selected category changes.
  useEffect(() => {
    let isMounted = true;

    async function loadCategoryForecast() {
      setIsCategoryLoading(true);
      const result = await getCategoryForecast(selectedCategory);
      if (!isMounted) return;

      if (result.success) setCategoryForecast(result.forecast);
      else setError(result.error);

      setIsCategoryLoading(false);
    }

    loadCategoryForecast();
    return () => {
      isMounted = false;
    };
  }, [selectedCategory]);

  return (
    <div className="page">
      <h1 className="page-title">Predictions</h1>
      <p className="page-subtitle">
        Forecasts from a simple trend line fitted to your last 6 months of spending.
      </p>

      <ErrorAlert message={error} onClose={() => setError("")} />

      {isLoading ? (
        <Loading label="Loading predictions..." />
      ) : (
        <div className="predictions-grid">
          <section className="card">
            <div className="card-header">
              <h2>Monthly forecast</h2>
              {monthlyForecast && <TrendBadge trend={monthlyForecast.trend} />}
            </div>

            {monthlyForecast ? (
              <>
                <div className="forecast-headline">
                  <span className="summary-card-label">Next month's estimated spend</span>
                  <span className="summary-card-value summary-card-expense">
                    {formatCurrency(monthlyForecast.forecast_next_month)}
                  </span>
                </div>
                <MonthlyLineChart data={monthlyForecast.history} />
              </>
            ) : (
              <p className="empty-state">Not enough transaction history yet.</p>
            )}
          </section>

          <section className="card">
            <div className="card-header">
              <h2>Category forecast</h2>
              {categoryForecast && <TrendBadge trend={categoryForecast.trend} />}
            </div>

            <label className="form-field form-field-inline">
              <span>Category</span>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                {FORECASTABLE_CATEGORIES.map((c) => (
                  <option key={c} value={c}>
                    {c[0].toUpperCase() + c.slice(1)}
                  </option>
                ))}
              </select>
            </label>

            {isCategoryLoading ? (
              <Loading label="Loading forecast..." />
            ) : categoryForecast ? (
              <>
                <div className="forecast-headline">
                  <span className="summary-card-label">
                    Next month's estimated {selectedCategory} spend
                  </span>
                  <span className="summary-card-value summary-card-expense">
                    {formatCurrency(categoryForecast.forecast_next_month)}
                  </span>
                </div>
                <MonthlyLineChart data={categoryForecast.history} />
              </>
            ) : (
              <p className="empty-state">No history for this category yet.</p>
            )}
          </section>

          <section className="card predictions-recommendations">
            <div className="card-header">
              <h2>Recommendations</h2>
            </div>

            {recommendations.length === 0 ? (
              <p className="empty-state">
                Add a few months of expenses to unlock savings recommendations.
              </p>
            ) : (
              <ul className="recommendation-list">
                {recommendations.map((rec) => (
                  <li className="recommendation-card" key={rec.category}>
                    <div className="recommendation-card-header">
                      <span className="recommendation-category">
                        {rec.category[0].toUpperCase() + rec.category.slice(1)}
                      </span>
                      <span className="recommendation-savings">
                        Save {formatCurrency(rec.estimated_annual_savings)}/yr
                      </span>
                    </div>
                    <p className="recommendation-detail">
                      Cutting this category by {rec.cut_percent}% (from{" "}
                      {formatCurrency(rec.current_monthly_spend)}/mo) saves about{" "}
                      {formatCurrency(rec.estimated_monthly_savings)} per month.
                    </p>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
