/** Format an ISO date string (YYYY-MM-DD) as a readable date, e.g. "Jul 30, 2026". */
export function formatDate(dateStr) {
  if (!dateStr) return "";
  const date = new Date(`${dateStr}T00:00:00`);
  if (Number.isNaN(date.getTime())) return dateStr;
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/** Format a Date (or ISO string) as YYYY-MM-DD, ready to drop into a <input type="date">. */
export function formatDateForInput(date = new Date()) {
  const d = typeof date === "string" ? new Date(date) : date;
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/** Build an array of the last `count` months as {value: "YYYY-MM", label: "Jul 2026"}, oldest first. */
export function getMonthsRange(count = 6) {
  const months = [];
  const cursor = new Date();
  cursor.setDate(1);

  for (let i = 0; i < count; i += 1) {
    const value = `${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, "0")}`;
    const label = cursor.toLocaleDateString("en-US", { year: "numeric", month: "short" });
    months.unshift({ value, label });
    cursor.setMonth(cursor.getMonth() - 1);
  }

  return months;
}
