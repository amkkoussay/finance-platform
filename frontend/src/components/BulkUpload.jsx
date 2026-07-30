import { useRef, useState } from "react";

export default function BulkUpload({ onUpload }) {
  const fileInputRef = useRef(null);
  const [result, setResult] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  async function handleFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setResult(null);

    const response = await onUpload(file);

    setIsUploading(false);
    setResult(response);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  return (
    <div className="bulk-upload">
      <h3 className="form-title">Bulk upload (CSV)</h3>
      <p className="bulk-upload-hint">
        Columns: date, category, amount, description, is_income
      </p>

      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        disabled={isUploading}
      />

      {isUploading && <p className="bulk-upload-status">Uploading...</p>}

      {result?.success && (
        <div className="bulk-upload-result">
          <p>Imported {result.imported} transaction(s).</p>
          {result.errors?.length > 0 && (
            <ul className="bulk-upload-errors">
              {result.errors.map((err) => (
                <li key={err.row}>
                  Row {err.row}: {err.error}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {result && !result.success && <p className="form-error">{result.error}</p>}
    </div>
  );
}
