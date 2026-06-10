function SendButton({ disabled, email, sendStatus, onSendStatusChange }) {
  const handleClick = async () => {
    try {
      onSendStatusChange({
        loading: true,
        result: null,
        error: null,
      });

      const res = await fetch("http://127.0.0.1:8000/send-emails", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject: email.subject,
          body: email.body,
        }),
      });

      const contentType = res.headers.get("content-type");

      const data =
        contentType && contentType.includes("application/json")
          ? await res.json()
          : { detail: await res.text() };

      if (!res.ok) {
        const msg = data?.detail || data?.error || `Server Error: ${res.status}`;
        throw new Error(msg);
      }

      onSendStatusChange({
        loading: false,
        result: data,
        error: null,
      });
    } catch (err) {
      onSendStatusChange({
        loading: false,
        result: null,
        error: err.message || "Something went wrong",
      });
    }
  };

  return (
    <div className="card">
      <button onClick={handleClick} disabled={disabled || sendStatus.loading}>
        {sendStatus.loading ? "Sending..." : "Send Emails"}
      </button>

      {sendStatus.error ? (
        <p className="error">{sendStatus.error}</p>
      ) : null}

      {sendStatus.result ? (
        <div className="result">
          <p className="success">
            Sent: {sendStatus.result.sent} / {sendStatus.result.total}
          </p>

          {sendStatus.result.failed > 0 ? (
            <div className="errorBox">
              <p className="error">Failed: {sendStatus.result.failed}</p>

              {Array.isArray(sendStatus.result.failures) &&
              sendStatus.result.failures.length > 0 ? (
                <ul>
                  {sendStatus.result.failures.slice(0, 10).map((f, idx) => (
                    <li key={idx}>
                      {f.email || `row ${f.row}`}: {f.error}
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

export default SendButton;