import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from django.conf import settings


def send_verification_email_html(to_email, code):
    subject = "Verify Your Diamond Casino Account"
    logo_path = 'static/img/casino-logo.png'  # Adjust as needed

    # Base64 inline image
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
        logo_encoded = base64.b64encode(logo_data).decode()

    html_content = f"""
    <html>
      <body style="font-family:sans-serif; text-align:center; background:#1c1c1e; color:#fff; padding:40px;">
        <div style="max-width:500px; margin:0 auto; background:#2a2a2d; padding:30px; border-radius:10px;">
          <img src="cid:gcoinlogo" alt="Diamond Casino" style="width:80px; margin-bottom:20px;" />
          <h2>Diamond Casino Verification</h2>
          <p>Your 6-digit verification code is:</p>
          <div style="font-size:32px; font-weight:bold; background:#111; padding:10px 0; border-radius:5px;">
            {code}
          </div>
          <p style="margin-top:20px;">This code will expire in 10 minutes.</p>
          <hr style="margin:30px 0; border:none; border-top:1px solid #444;" />
          <small style="color:#aaa;">Please do not share this code with anyone.<br>&copy; 2025 Diamond Casino Games</small>
        </div>
      </body>
    </html>
    """

    # Setup email
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = to_email

    # Add HTML content
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(html_content, 'html'))
    msg.attach(alt)

    # Attach logo as inline image
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<gcoinlogo>')
    msg.attach(logo)

    # SMTP configuration
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, to_email, msg.as_string())
