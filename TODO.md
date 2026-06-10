# TODO - Job Application Sender

- [ ] Backend: Update `backend/main.py` to add CORS and implement endpoints:
  - [ ] `POST /upload/resume` (multipart/form-data; save to `backend/uploads/resume.pdf`)
  - [ ] `POST /upload/csv` (multipart/form-data; save to `backend/uploads/recipients.csv`)
  - [ ] `POST /send` (JSON `{subject, body}`; validate uploads + CSV headers)
  - [ ] Return structured success/failure counts and error details
- [ ] Backend: Refactor `backend/email_sender.py` to:
  - [ ] Load Gmail SMTP config from `.env` (SENDER_EMAIL, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT)
  - [ ] Send to every recruiter from `backend/uploads/recipients.csv`
  - [ ] Personalize email body using `{name}` with recruiter name from CSV
  - [ ] Attach `backend/uploads/resume.pdf`
  - [ ] Robust per-row error handling (continue sending; return sent/failed)
- [ ] Frontend: Wire UI to backend in these components:
  - [ ] `UploadResume.jsx` upload handler + validation + loading + errors
  - [ ] `UploadCSV.jsx` upload handler + validation + loading + errors
  - [ ] `EmailForm.jsx` controlled inputs for subject/body
  - [ ] `SendButton.jsx` call `POST /send`, show loading state, and render success/failure summary
  - [ ] `frontend/src/App.jsx` lifted/shared state wiring
- [ ] Frontend: Improve responsive modern styling in `frontend/src/App.css` (loading/disabled/error/success)
- [ ] (Manual) Run and verify:
  - [ ] Backend: `uvicorn backend.main:app --reload --port 8000`
  - [ ] Frontend: `npm run dev` in `frontend/`
  - [ ] Upload resume.pdf + recipients.csv, then send emails; verify counts

