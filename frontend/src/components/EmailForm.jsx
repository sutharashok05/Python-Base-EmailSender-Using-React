function EmailForm({ value, onChange }) {
  return (
    <div className="card">
      <h3>Email Details</h3>

      <input
        type="text"
        value={value.subject}
        onChange={(e) => onChange((prev) => ({ ...prev, subject: e.target.value }))}
        placeholder="Enter Email Subject"
      />

      <br />
      <br />

      <textarea
        rows="8"
        value={value.body}
        onChange={(e) => onChange((prev) => ({ ...prev, body: e.target.value }))}
        placeholder="Enter Email Body"
      ></textarea>

      <p className="hint">Use <b>{"{name}"}</b> in the body to personalize with the recruiter name.</p>
    </div>
  );
}

export default EmailForm;
