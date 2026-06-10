import { useState } from "react";

function UploadCSV({ onUploadStateChange }) {
  const [localError, setLocalError] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    setLocalError(null);
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".csv")) {
      const msg = "CSV must be a .csv file";
      setLocalError(msg);
      onUploadStateChange({ uploaded: false, loading: false, error: msg });
      return;
    }

    try {
      onUploadStateChange({ uploaded: false, loading: true, error: null });

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/upload/csv", {
        method: "POST",
        body: formData,
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        const msg = data?.detail || data?.error || "CSV upload failed";
        throw new Error(msg);
      }

      onUploadStateChange({ uploaded: true, loading: false, error: null });
    } catch (err) {
      const msg = err?.message || "CSV upload failed";
      setLocalError(msg);
      onUploadStateChange({ uploaded: false, loading: false, error: msg });
    }
  };

  return (
    <div className="card">
      <h3>Upload CSV File</h3>

      <input
        type="file"
        accept=".csv"
        onChange={handleUpload}
      />

      {localError ? <p className="error">{localError}</p> : null}
    </div>
  );
}

export default UploadCSV;
