/** Format a number as USD currency, e.g. 1234.5 -> "$1,234.50". */
export function formatCurrency(amount) {
  const value = Number(amount) || 0;
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

/** Returns a semantic color for a monetary value: green for positive/income, red for negative/expense. */
export function getCurrencyColor(amount) {
  const value = Number(amount) || 0;
  if (value > 0) return "var(--color-income)";
  if (value < 0) return "var(--color-expense)";
  return "var(--color-text-secondary)";
}
