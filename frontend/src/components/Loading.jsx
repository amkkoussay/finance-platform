export default function Loading({ label = "Loading..." }) {
  return (
    <div className="loading">
      <div className="loading-spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
