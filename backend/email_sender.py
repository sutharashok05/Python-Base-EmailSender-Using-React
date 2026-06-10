import csv
import os
import re
import smtplib
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _smtp_client():
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD") or os.getenv("APP_PASSWORD")

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not sender_email or not password:
        raise RuntimeError("Missing SENDER_EMAIL or EMAIL_PASSWORD/APP_PASSWORD in .env")

    if smtp_port == 465:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(sender_email, password)
        return smtp, sender_email

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, password)
    return smtp, sender_email


def _validate_email(email: str) -> bool:
    return bool(email and _EMAIL_RE.match(email.strip()))


def send_bulk_emails(*, subject: str, body: str, resume_path: str, csv_path: str):
    subject = (subject or "").strip()
    body = (body or "").strip()

    if not subject:
        raise RuntimeError("Subject is required")
    if not body:
        raise RuntimeError("Body is required")

    resume_file = Path(resume_path)
    csv_file = Path(csv_path)

    if not resume_file.exists():
        raise RuntimeError("Resume file not found")
    if not csv_file.exists():
        raise RuntimeError("Recipients CSV not found")

    resume_bytes = resume_file.read_bytes()

    total = 0
    sent = 0
    failed = 0
    failures = []

    with open(csv_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        required_cols = {"name", "email"}
        headers = set(reader.fieldnames or [])
        missing = required_cols - headers
        if missing:
            raise RuntimeError(
                f"CSV missing required columns: {', '.join(sorted(missing))}. Expected: name, email"
            )

        smtp, sender_email = _smtp_client()

        try:
            for idx, row in enumerate(reader, start=2):
                total += 1

                name = (row.get("name") or "").strip()
                to_email = (row.get("email") or "").strip()

                if not _validate_email(to_email):
                    failed += 1
                    failures.append({
                        "row": idx,
                        "email": to_email,
                        "error": "Invalid or missing email"
                    })
                    continue

                msg = MIMEMultipart()
                msg["From"] = formataddr(("", sender_email))
                msg["To"] = to_email
                msg["Subject"] = subject

                personalized_body = body.replace("{name}", name if name else "Candidate")
                msg.attach(MIMEText(personalized_body, "plain", "utf-8"))

                part = MIMEBase("application", "octet-stream")
                part.set_payload(resume_bytes)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", 'attachment; filename="resume.pdf"')
                msg.attach(part)

                try:
                    smtp.send_message(msg)
                    sent += 1
                except Exception as e:
                    failed += 1
                    failures.append({
                        "row": idx,
                        "email": to_email,
                        "error": str(e)
                    })
        finally:
            smtp.quit()

    return {
        "total": total,
        "sent": sent,
        "failed": failed,
        "failures": failures,
    }