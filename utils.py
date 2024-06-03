from kavenegar import KavenegarAPI, APIException, HTTPException

from django.core.mail import send_mail
from django.utils.crypto import get_random_string


def send_otp_sms(phone, code):
    try:
        api = KavenegarAPI(
            "344D62384730452F39584D7670726E4F30343143376F4838473854416B6C77682F684D73356450417757413D"
        )
        params = {
            "sender": "",
            "receptor": phone,
            "message": f"your code is {code}",
        }
        print(code)
        response = api.sms_send(params)
        print(response)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_otp_email(email, code):
    subject = "Your code for verification"
    message = (
        f"Hi there,\n\n"
        f"Thank you for choosing us! Your verification code is: {code}\n\n"
        f"Best regards,\n"
        f"Room Reservation System"
    )
    # Sender email address
    from_email = "djangod081@gmail.com"
    print(code)

    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending OTP email: {e}")
