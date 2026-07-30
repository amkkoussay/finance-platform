import api from "./api";

/** Forecast of next month's total expense, with recent history + trend. */
export async function getMonthlyForecast() {
  try {
    const response = await api.get("/predictions/monthly-forecast");
    return { success: true, forecast: response.data.forecast };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Forecast of next month's spend for a single category. */
export async function getCategoryForecast(category) {
  try {
    const response = await api.get(`/predictions/category-forecast/${category}`);
    return { success: true, forecast: response.data.forecast };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Top categories to cut back on, ranked by projected annual savings. */
export async function getRecommendations(cutPercent = 10) {
  try {
    const response = await api.get("/predictions/recommendations", {
      params: { cut_percent: cutPercent },
    });
    return { success: true, recommendations: response.data.recommendations };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
