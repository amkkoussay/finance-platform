const LABELS = {
  increasing: "Increasing",
  decreasing: "Decreasing",
  stable: "Stable",
  insufficient_data: "Not enough data yet",
};

/** Small colored pill showing a spending trend (increasing/decreasing/stable). */
export default function TrendBadge({ trend }) {
  if (!trend) return null;

  return (
    <span className={`trend-badge trend-badge-${trend}`}>
      {LABELS[trend] || trend}
    </span>
  );
}
