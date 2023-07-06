from email.message import EmailMessage
import ssl
import smtplib

def send_email(email_sender, email_password, email_recipients, subject, body):
    # Create the email that we will be sending
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipients
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    # Set up the server and port number for email transmission
    email_server = "smtp.gmail.com"
    email_port = 465

    with smtplib.SMTP_SSL(email_server, email_port, context=context) as smtp:
        # login to the sender's email
        smtp.login(email_sender, email_password)
        # send the email from the email_sender to the email_recipients
        smtp.sendmail(email_sender, email_recipients, em.as_string())
        # success message if email goes through
        print("Email Success!")