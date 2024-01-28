import pyotp

from config.setting import settings


def generate_otp_secret_key():
    return pyotp.random_base32()


def generate_totp_code(secret_key: str, interval: int, length=6):
    return pyotp.TOTP(secret_key, interval=interval, digits=length).now()


def verify_totp_code(secret_key: str, interval: int, totp_code: str):
    return pyotp.TOTP(secret_key, interval=interval).verify(totp_code, valid_window=1)
