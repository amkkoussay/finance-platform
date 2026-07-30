export default function ErrorAlert({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="error-alert" role="alert">
      <span>{message}</span>
      {onClose && (
        <button
          type="button"
          className="error-alert-close"
          onClick={onClose}
          aria-label="Dismiss error"
        >
          &times;
        </button>
      )}
    </div>
  );
}
