# account/utils.py
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

signer = TimestampSigner()


def generate_deletion_token(user):
    """
    Подписываем PK пользователя, получаем строку '<pk>:<signature>:<timestamp>'
    """
    return signer.sign(str(user.pk))


def verify_deletion_token(token):
    """
    Проверяем токен:
      - если в настройках PROFILE_DELETION_TOKEN_EXPIRY <= 0, сразу считаем токен устаревшим
      - иначе вызываем signer.unsign(max_age=…), который может бросить SignatureExpired или BadSignature
    В любом случае возвращаем PK пользователя или бросаем ValueError с нужным текстом.
    """
    max_age = getattr(settings, 'PROFILE_DELETION_TOKEN_EXPIRY', 3600)
    if max_age <= 0:
        raise ValueError("Токен устарел")

    try:
        unsigned = signer.unsign(token, max_age=max_age)
    except SignatureExpired:
        raise ValueError("Токен устарел")
    except BadSignature:
        raise ValueError("Неверный токен")

    return int(unsigned)
