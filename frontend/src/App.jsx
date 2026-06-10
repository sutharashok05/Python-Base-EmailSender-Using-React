import { useState } from "react";

import UploadResume from "./components/UploadResume";
import UploadCSV from "./components/UploadCSV";
import EmailForm from "./components/EmailForm";
import SendButton from "./components/SendButton";

function App() {
  const [resumeStatus, setResumeStatus] = useState({
    uploaded: false,
    loading: false,
    error: null,
  });

  const [csvStatus, setCsvStatus] = useState({
    uploaded: false,
    loading: false,
    error: null,
  });

  const [email, setEmail] = useState({
    subject: "Application for Software Developer",
    body: `Hello {name},

I hope you're doing well.

Please find my resume attached.

Regards,
Kirti Jain`,
  });

  const [sendStatus, setSendStatus] = useState({
    loading: false,
    result: null,
    error: null,
  });

  const canSend =
    resumeStatus.uploaded &&
    csvStatus.uploaded &&
    !resumeStatus.loading &&
    !csvStatus.loading;

  return (
    <div className="container">
      <h1>📧 Job Application Sender</h1>

      <UploadResume onUploadStateChange={setResumeStatus} />

      <UploadCSV onUploadStateChange={setCsvStatus} />

      <EmailForm value={email} onChange={setEmail} />

      <SendButton
        disabled={!canSend || sendStatus.loading}
        email={email}
        sendStatus={sendStatus}
        onSendStatusChange={setSendStatus}
      />
    </div>
  );
}

export default App;