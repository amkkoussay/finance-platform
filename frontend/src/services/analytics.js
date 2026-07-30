import api from "./api";

/** Totals: income, expense, balance, transaction count. */
export async function getSummary(userId) {
  try {
    const response = await api.get("/analytics/summary", { params: { user_id: userId } });
    return { success: true, summary: response.data.summary };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Expense breakdown by category for a given month (YYYY-MM), defaults to current month. */
export async function getByCategory(userId, month) {
  try {
    const response = await api.get("/analytics/by-category", {
      params: { user_id: userId, month },
    });
    return { success: true, data: response.data.data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Monthly expense totals for the last N months, oldest first. */
export async function getMonthly(userId, months = 6) {
  try {
    const response = await api.get("/analytics/monthly", {
      params: { user_id: userId, months },
    });
    return { success: true, data: response.data.data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Average daily spending over the last N days. */
export async function getSpendingRate(userId, days = 30) {
  try {
    const response = await api.get("/analytics/spending-rate", {
      params: { user_id: userId, days },
    });
    return { success: true, rate: response.data.rate };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
