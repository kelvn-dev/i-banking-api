from fastapi import HTTPException
from loguru import logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

from config.setting import settings
from enums.sendgrid_enum import TemplateId
from models import User


class SendGridService:
    def __init__(self):
        self.sendgrid_client = SendGridAPIClient(settings.sendgrid_api_key)

    def send(self, message: Mail):
        message.from_email = settings.sendgrid_email_sender
        try:
            self.sendgrid_client.send(message)
        except Exception as e:
            logger.debug(e)
            raise HTTPException(
                status_code=500, detail="Couldn't make a Twilio SendGrid v3 API request"
            )

    def send_otp_verification(self, user: User, otp_code: str):
        message = Mail(to_emails=user.email)
        message.template_id = TemplateId.OTP_VERIFICATION.value
        message.dynamic_template_data = {
            "full_name": user.full_name,
            "otp_code": otp_code,
        }
        return self.send(message)


sendgrid_service = SendGridService()