import hmac
import hashlib
from app.core.config import settings

class TelegramAuthService:
    secret: str = settings.BOT_TOKEN

    @classmethod
    def verify(cls, data: dict) -> bool:
        check_hash = data.pop('hash', None)
        data_list = [f"{k}={v}" for k, v in sorted(data.items())]
        data_string = "\n".join(data_list)
        secret_key = hashlib.sha256(cls.secret.encode()).digest()
        hmac_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
        return hmac_hash == check_hash