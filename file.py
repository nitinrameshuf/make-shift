import smtplib
from email.message import EmailMessage
import mimetypes

# === Configuration ===
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your_email@gmail.com"
receiver_email = "recipient@example.com"
password = "your_app_password"  # Use App Password for Gmail

# === Create the Email ===
msg = EmailMessage()
msg["Subject"] = "Test Email with Attachment"
msg["From"] = sender_email
msg["To"] = receiver_email
msg.set_content("Please find the attachment.")

# === Add an Attachment ===
file_path = "document.pdf"

# Guess the MIME type
mime_type, _ = mimetypes.guess_type(file_path)
mime_type = mime_type or "application/octet-stream"
main_type, sub_type = mime_type.split("/", 1)

with open(file_path, "rb") as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(file_data, maintype=main_type, subtype=sub_type, filename=file_name)

# === Send the Email ===
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Secure the connection
    server.login(sender_email, password)
    server.send_message(msg)

print("Email sent successfully.")
