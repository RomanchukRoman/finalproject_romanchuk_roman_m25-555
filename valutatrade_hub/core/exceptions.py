class InsufficientFundsError(Exception):
    """Исключение при недостатке средств."""
    
    def __init__(self, available: float, required: float, currency_code: str):
        self.available = available
        self.required = required
        self.currency_code = currency_code
        super().__init__(f"Недостаточно средств: доступно {available} {currency_code}, требуется {required} {currency_code}")


class CurrencyNotFoundError(Exception):
    """Исключение при неизвестной валюте."""
    
    def __init__(self, currency_code: str):
        self.currency_code = currency_code
        super().__init__(f"Неизвестная валюта '{currency_code}'")


class ApiRequestError(Exception):
    """Исключение при ошибке API."""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Ошибка при обращении к внешнему API: {reason}")


class UserNotFoundError(Exception):
    """Исключение при отсутствии пользователя."""
    
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Пользователь '{username}' не найден")


class AuthenticationError(Exception):
    """Исключение при ошибке аутентификации."""
    
    def __init__(self, message: str = "Неверный пароль"):
        super().__init__(message)