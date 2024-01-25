import pyotp

from config.setting import settings


def generate_otp_secret_key():
    return pyotp.random_base32()


def generate_totp_code(secret_key: str, length=6):
    return pyotp.TOTP(secret_key, digits=length).now()


def verify_totp_code(secret_key: str, totp_code):
    return pyotp.TOTP(secret_key).verify(totp_code)
