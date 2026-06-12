# Python Base EmailSender

A full-stack email sender app built with **FastAPI** on the backend and **React + Vite** on the frontend. It lets users upload a resume PDF, upload a CSV of recipients, compose an email template, and send personalized emails with the resume attached.[1][2]

## Features

- Upload a resume as a PDF file and store it on the backend for email attachment use.[1][3]
- Upload a recipients CSV file with required `name` and `email` columns for bulk sending.[2][3]
- Compose a reusable subject and body template, including personalization like `{name}` replacement.
- Send emails through SMTP using environment variables stored in a `.env` file.[4][5]
- View API docs automatically through FastAPI’s built-in `/docs` endpoint.[6][7][8]

## Tech Stack

### Backend

- FastAPI
- Uvicorn
- python-dotenv
- python-multipart
- pandas
- pydantic
- email-validator

FastAPI automatically generates an OpenAPI schema and interactive API documentation, typically available at `/docs`.[6][7][9]

### Frontend

- React
- Vite
- Fetch API

## Project Structure

```text
Python-Base-EmailSender/
├── backend/
│   ├── main.py
│   ├── email_sender.py
│   ├── .env
│   ├── uploads/
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── UploadResume.jsx
│   │       ├── UploadCSV.jsx
│   │       ├── EmailForm.jsx
│   │       └── SendButton.jsx
│   └── package.json
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sutharashok05/Python-Base-EmailSender.git
cd Python-Base-EmailSender
```

### 2. Backend setup

Create and activate a virtual environment, then install the required Python packages.

```bash
cd backend
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn python-dotenv python-multipart pandas pydantic email-validator
```

`python-multipart` is needed for `multipart/form-data` handling in file upload endpoints.[1][2][3]

### 3. Create the `.env` file

Create `backend/.env` and add your SMTP settings.

```env
SENDER_EMAIL=yourgmail@gmail.com
APP_PASSWORD=your_16_character_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

`python-dotenv` can load these variables from the `.env` file so the app can read them with `os.getenv()`.[4][10][5]

### 4. Frontend setup

Open a new terminal and install frontend dependencies.

```bash
cd frontend
npm install
npm run dev
```

Vite commonly runs the frontend development server on `http://localhost:5173`.[9]

## Running the app

### Start the backend

From the `backend` folder:

```bash
uvicorn main:app --reload
```

FastAPI will usually be available at `http://127.0.0.1:8000`, and the interactive docs will be at `http://127.0.0.1:8000/docs`.[6][7][9]

### Start the frontend

From the `frontend` folder:

```bash
npm run dev
```

The React app will usually be available at `http://localhost:5173` during development.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/upload/resume` | Upload a resume PDF file. |
| `POST` | `/upload/csv` | Upload a recipients CSV file. |
| `POST` | `/send-emails` | Send personalized emails with the resume attached. |
| `GET` | `/docs` | Open FastAPI interactive API documentation.[7] |

## CSV Format

The recipients CSV file should include these columns:

```csv
name,email
John Doe,john@example.com
Jane Smith,jane@example.com
```

The backend validates the file structure before sending emails so the required columns should exist in the CSV.[11]

## Personalization

The message body can include `{name}` and the backend replaces it with the recipient’s name before sending.

Example:

```text
Hello {name},

I hope you're doing well.

Please find my resume attached.

Regards,
Your Name
```

## CORS note

If the frontend runs on `http://localhost:5173`, the backend should allow that origin in `CORSMiddleware` so browser requests are not blocked by CORS.[7]

Example:

```python
origins = [
    "http://localhost:5173",
]
```

## Recommended `.gitignore`

```gitignore
venv/
node_modules/
.env
__pycache__/
*.pyc
uploads/
dist/
build/
```

This helps avoid committing secrets, virtual environments, uploaded files, and generated dependency folders.

## Common issues

### Missing environment variables

If clicking the send button causes a server error about missing `SENDER_EMAIL` or `APP_PASSWORD`, make sure the `.env` file exists in the backend folder and `load_dotenv()` is called before reading environment variables.[4][5]

### CORS error

If the browser says `No 'Access-Control-Allow-Origin' header is present`, make sure FastAPI `CORSMiddleware` includes the correct frontend origin such as `http://localhost:5173`.[7]

### Gmail authentication error

For Gmail SMTP, an App Password is typically required instead of the normal account password when using scripts or SMTP-based apps.[12][13][14]

## Future improvements

- Add email sending progress in the UI.
- Add support for HTML email templates.
- Add file cleanup after sending.
- Add authentication and rate limiting.
- Deploy the backend and frontend for public use.

## License

This project can use an MIT License or any license of choice added by the repository owner.
