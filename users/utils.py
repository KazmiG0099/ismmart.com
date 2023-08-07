# users/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_otp_code(email, otp_code):
    subject = 'OTP Code for Registration'
    message = f'Your OTP Code is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"Sending OTP code {otp_code} to {email}")
    try:
        send_mail(subject, message, from_email, recipient_list)
        print("OTP code sent successfully.")
    except Exception as e:
        print(f"Error sending OTP code: {e}")