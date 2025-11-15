from datetime import datetime
from typing import Tuple

from ..decorators import log_buy, log_get_rate, log_login, log_register, log_sell
from .currencies import get_currency
from .models import User


class UseCases:
    """Класс с бизнес-логикой приложения."""
    
    @log_register
    def register_user(self, username: str, password: str) -> User:
        """
        Регистрация нового пользователя.
        """
        # Заглушка - возвращаем данные для лога
        return {
            'user': username,
            'result': 'registered'
        }
    
    @log_login  
    def authenticate_user(self, username: str, password: str) -> dict:
        """
        Аутентификация пользователя.
        """
        # Заглушка - возвращаем данные для лога
        return {
            'user': username,
            'result': 'authenticated'
        }
    
    @log_buy
    def buy_currency(self, user_id: int, currency_code: str, amount: float) -> dict:
        """
        Покупка валюты с валидацией через currencies.py.
        """
        # Валидация валюты
        currency_obj = get_currency(currency_code)
        
        if amount <= 0:
            raise ValueError("Amount должен быть положительным числом")
        
        # Возвращаем данные для лога
        return {
            'user_id': user_id,
            'currency': currency_code,
            'amount': amount,
            'rate': 59300.00,  # Пример курса
            'base': 'USD'
        }
    
    @log_sell
    def sell_currency(self, user_id: int, currency_code: str, amount: float) -> dict:
        """
        Продажа валюты с валидацией через currencies.py.
        """
        # Валидация валюты
        currency_obj = get_currency(currency_code)
        
        if amount <= 0:
            raise ValueError("Amount должен быть положительным числом")
        
        # Возвращаем данные для лога
        return {
            'user_id': user_id,
            'currency': currency_code,
            'amount': amount,
            'rate': 59800.00,  # Пример курса
            'base': 'USD'
        }
    
    @log_get_rate
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Tuple[float, str]:
        """
        Получение курса валюты с валидацией через currencies.py.
        """
        # Валидация валют
        from_currency_obj = get_currency(from_currency)
        to_currency_obj = get_currency(to_currency)
        
        # Заглушка - возвращаем фиксированный курс
        rate = 59300.0 if to_currency == 'BTC' else 1.08
        return rate, datetime.now().isoformat()


# Глобальный экземпляр
usecases = UseCases()