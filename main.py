import re
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConsultationRequest(BaseModel):
    name: str
    email: str
    message: str

def is_valid_email(email):
    # Define a regular expression pattern for basic email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def send_email(sender_email, sender_password, recipient_email, cc_emails, subject, message):
    try:
        # Set up the MIMEText object
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Cc'] = ', '.join(cc_emails)

        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to your email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, [recipient_email] + cc_emails, msg.as_string())

        # Close the connection
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

@app.get("/healthcheck/")
def healthcheck():
    return {"message": "AIOverflow API is up and running!"}

@app.post("/request_consultation/")
def request_consultation(consultation_request: ConsultationRequest = Body(...)):
    sender_email = "aioverflow.ml@gmail.com"  # Replace with your email address
    sender_password = "iyfngcdhgfcbkufv"  # Replace with your email password

    recipient_email = consultation_request.email
    cc_emails = ["achethanreddy1921@gmail.com", "subhanu12@gmail.com"]
    subject = "Request for Free Consultation"
    message = f"Dear {consultation_request.name},\n\nThank you for your interest in our consultation service. We will reach out to you soon regarding your project.\n\nBest regards,\nTeam AIOverflow"

    try:
        # Verify the email address
        if not is_valid_email(recipient_email):
            raise HTTPException(status_code=400, detail="Invalid email address")

        # Send the confirmation email
        send_email(sender_email, sender_password, recipient_email, cc_emails, subject, message)

        return {"message": "Confirmation email sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send confirmation email. Error: {e}")
