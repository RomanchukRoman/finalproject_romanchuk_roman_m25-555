import hashlib
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional


class User:
    """Класс пользователя системы с аутентификацией и валидацией."""
    
    def __init__(self, user_id: int, username: str, password: str, 
                 registration_date: datetime = None, salt: str = None, 
                 hashed_password: str = None):
        """
        Инициализация пользователя.
        
        Args:
            user_id: Уникальный идентификатор пользователя
            username: Имя пользователя
            password: Пароль (если hashed_password не указан)
            registration_date: Дата регистрации (по умолчанию текущее время)
            salt: Соль для хеширования (генерируется автоматически)
            hashed_password: Уже захэшированный пароль (для загрузки из БД)
        """
        self._user_id = user_id
        self._username = username
        
        if registration_date is None:
            self._registration_date = datetime.now()
        else:
            self._registration_date = registration_date
            
        if salt is None:
            self._salt = secrets.token_hex(8)
        else:
            self._salt = salt
            
        if hashed_password is not None:
            self._hashed_password = hashed_password
        else:
            self._hashed_password = self._hash_password(password)
    
    @property
    def user_id(self) -> int:
        """Геттер для ID пользователя."""
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int) -> None:
        """Сеттер для ID пользователя."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
        self._user_id = value
    
    @property
    def username(self) -> str:
        """Геттер для имени пользователя."""
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        """Сеттер для имени пользователя."""
        if not value or not value.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self._username = value.strip()
    
    @property
    def hashed_password(self) -> str:
        """Геттер для хэшированного пароля."""
        return self._hashed_password
    
    @property
    def salt(self) -> str:
        """Геттер для соли."""
        return self._salt
    
    @property
    def registration_date(self) -> datetime:
        """Геттер для даты регистрации."""
        return self._registration_date
    
    @registration_date.setter
    def registration_date(self, value: datetime) -> None:
        """Сеттер для даты регистрации."""
        if not isinstance(value, datetime):
            raise ValueError("Дата регистрации должна быть объектом datetime")
        self._registration_date = value
    
    def _hash_password(self, password: str) -> str:
        """
        Хэширование пароля с солью.
        
        Args:
            password: Пароль для хэширования
            
        Returns:
            Хэшированный пароль
        """
        if len(password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")
        
        password_bytes = password.encode('utf-8')
        salt_bytes = self._salt.encode('utf-8')
        return hashlib.sha256(password_bytes + salt_bytes).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """
        Проверка пароля на совпадение.
        
        Args:
            password: Пароль для проверки
            
        Returns:
            True если пароль верный, иначе False
        """
        try:
            return self._hashed_password == self._hash_password(password)
        except ValueError:
            return False
    
    def change_password(self, new_password: str) -> None:
        """
        Изменение пароля пользователя.
        
        Args:
            new_password: Новый пароль
            
        Raises:
            ValueError: Если пароль слишком короткий
        """
        self._hashed_password = self._hash_password(new_password)
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Получение информации о пользователе (без пароля).
        
        Returns:
            Словарь с информацией о пользователе
        """
        return {
            'user_id': self._user_id,
            'username': self._username,
            'registration_date': self._registration_date.isoformat(),
            'salt': self._salt
        }
    

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализация пользователя в словарь для JSON.
        
        Returns:
            Словарь для сохранения в JSON
        """
        return {
            'user_id': self._user_id,
            'username': self._username,
            'hashed_password': self._hashed_password,
            'salt': self._salt,
            'registration_date': self._registration_date.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Создание пользователя из словаря (из JSON).
        
        Args:
            data: Данные пользователя
            
        Returns:
            Объект User
        """
        registration_date = datetime.fromisoformat(data['registration_date'])
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            password="",  # Пароль не используется при загрузке из хэша
            registration_date=registration_date,
            salt=data['salt'],
            hashed_password=data['hashed_password']
        )
    
    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"User(id={self._user_id}, username='{self._username}', registered={self._registration_date.strftime('%Y-%m-%d')})"
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"User(user_id={self._user_id}, username='{self._username}')"
    
class Wallet:
    """Класс кошелька пользователя для одной конкретной валюты."""
    
    def __init__(self, currency_code: str, balance: float = 0.0):
        """
        Инициализация кошелька.
        
        Args:
            currency_code: Код валюты (например, "USD", "BTC")
            balance: Начальный баланс (по умолчанию 0.0)
        """
        self.currency_code = currency_code
        self._balance = 0.0  # Инициализируем через сеттер для валидации
        self.balance = balance  # Используем сеттер для установки начального баланса
    
    @property
    def currency_code(self) -> str:
        """Геттер для кода валюты."""
        return self._currency_code
    
    @currency_code.setter
    def currency_code(self, value: str) -> None:
        """Сеттер для кода валюты."""
        if not value or not isinstance(value, str):
            raise ValueError("Код валюты не может быть пустым")
        self._currency_code = value.upper().strip()
    
    @property
    def balance(self) -> float:
        """Геттер для баланса."""
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        """
        Сеттер для баланса с валидацией.
        
        Args:
            value: Новое значение баланса
            
        Raises:
            ValueError: Если значение отрицательное или некорректного типа
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Баланс должен быть числом")
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = float(value)
    
    def deposit(self, amount: float) -> None:
        """
        Пополнение баланса.
        
        Args:
            amount: Сумма для пополнения
            
        Raises:
            ValueError: Если сумма не положительная
        """
        if not isinstance(amount, (int, float)):
            raise ValueError("Сумма пополнения должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        
        self.balance += amount
    
    def withdraw(self, amount: float) -> None:
        """
        Снятие средств с кошелька.
        
        Args:
            amount: Сумма для снятия
            
        Raises:
            ValueError: Если сумма не положительная
            InsufficientFundsError: Если недостаточно средств
        """
        if not isinstance(amount, (int, float)):
            raise ValueError("Сумма снятия должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        
        if amount > self._balance:
            raise InsufficientFundsError(
                available=self._balance,
                required=amount,
                currency_code=self.currency_code
            )
        
        self.balance -= amount
    
    def get_balance_info(self) -> str:
        """
        Получение информации о текущем балансе.
        
        Returns:
            Строка с информацией о балансе
        """
        return f"{self.currency_code}: {self._balance:.4f}"
    
    
    def to_dict(self) -> dict:
        """
        Сериализация кошелька в словарь для JSON.
        
        Returns:
            Словарь для сохранения в JSON
        """
        return {
            "currency_code": self.currency_code,
            "balance": self._balance
        }
    
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Wallet':
        """
        Создание кошелька из словаря (из JSON).
        
        Args:
            data: Данные кошелька
            
        Returns:
            Объект Wallet
        """
        return cls(
            currency_code=data["currency_code"],
            balance=data["balance"]
        )
    
    def __str__(self) -> str:
        """Строковое представление кошелька."""
        return f"Wallet({self.currency_code}: {self._balance:.4f})"
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Wallet(currency_code='{self.currency_code}', balance={self._balance})"
    
class Portfolio:
    """Класс для управления всеми кошельками одного пользователя."""
    
    def __init__(self, user_id: int, wallets: Dict[str, 'Wallet'] = None):
        """
        Инициализация портфеля.
        
        Args:
            user_id: Уникальный идентификатор пользователя
            wallets: Словарь кошельков (ключ - код валюты, значение - Wallet)
        """
        self._user_id = user_id
        self._wallets = wallets if wallets is not None else {}
    
    @property
    def user_id(self) -> int:
        """Геттер для ID пользователя."""
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int) -> None:
        """Сеттер для ID пользователя."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
        self._user_id = value
    
    @property
    def wallets(self) -> Dict[str, 'Wallet']:
        """Геттер, который возвращает копию словаря кошельков."""
        return self._wallets.copy()
    
    @property
    def user(self) -> int:
        """Геттер, который возвращает ID пользователя."""
        return self._user_id
    
    def add_currency(self, currency_code: str, initial_balance: float = 0.0) -> 'Wallet':
        """
        Добавляет новый кошелёк в портфель.
        
        Args:
            currency_code: Код валюты
            initial_balance: Начальный баланс (по умолчанию 0.0)
            
        Returns:
            Созданный объект Wallet
            
        Raises:
            ValueError: Если валюта уже существует в портфеле
        """
        if currency_code in self._wallets:
            raise ValueError(f"Валюта '{currency_code}' уже существует в портфеле")
        
        wallet = Wallet(currency_code, initial_balance)
        self._wallets[currency_code] = wallet
        return wallet
    
    def get_wallet(self, currency_code: str) -> Optional['Wallet']:
        """
        Возвращает объект Wallet по коду валюты.
        
        Args:
            currency_code: Код валюты
            
        Returns:
            Объект Wallet или None если не найден
        """
        return self._wallets.get(currency_code.upper())
    
    def get_or_create_wallet(self, currency_code: str) -> 'Wallet':
        """
        Получает кошелёк или создаёт новый, если не существует.
        
        Args:
            currency_code: Код валюты
            
        Returns:
            Существующий или новый объект Wallet
        """
        currency_code = currency_code.upper()
        wallet = self.get_wallet(currency_code)
        if wallet is None:
            wallet = self.add_currency(currency_code)
        return wallet
    
    def get_total_value(self, base_currency: str = 'USD', 
                       exchange_rates: Dict[str, float] = None) -> float:
        """
        Возвращает общую стоимость всех валют в указанной базовой валюте.
        
        Args:
            base_currency: Базовая валюта для конвертации
            exchange_rates: Словарь курсов валют (если None, используется заглушка)
            
        Returns:
            Общая стоимость в базовой валюте
        """
        if not self._wallets:
            return 0.0
        
        # Заглушка курсов валют (в реальном приложении брать из rates.json)
        if exchange_rates is None:
            exchange_rates = {
                'USD_USD': 1.0,
                'EUR_USD': 1.08,
                'BTC_USD': 50000.0,
                'ETH_USD': 3000.0,
                'RUB_USD': 0.011
            }
        
        total_value = 0.0
        
        for currency_code, wallet in self._wallets.items():
            if currency_code == base_currency:
                # Если валюта совпадает с базовой, просто добавляем баланс
                total_value += wallet.balance
            else:
                # Ищем курс для конвертации
                rate_key = f"{currency_code}_{base_currency}"
                reverse_rate_key = f"{base_currency}_{currency_code}"
                
                if rate_key in exchange_rates:
                    # Прямой курс найден
                    rate = exchange_rates[rate_key]
                    total_value += wallet.balance * rate
                elif reverse_rate_key in exchange_rates:
                    # Обратный курс найден - инвертируем
                    rate = 1.0 / exchange_rates[reverse_rate_key]
                    total_value += wallet.balance * rate
                else:
                    # Курс не найден - пропускаем валюту
                    print(f"Предупреждение: Курс для {currency_code}→{base_currency} не найден")
                    continue
        
        return total_value
    
    def get_portfolio_info(self, base_currency: str = 'USD',
                          exchange_rates: Dict[str, float] = None) -> List[str]:
        """
        Возвращает детальную информацию о портфеле.
        
        Args:
            base_currency: Базовая валюта для конвертации
            exchange_rates: Словарь курсов валют
            
        Returns:
            Список строк с информацией о каждом кошельке
        """
        info_lines = []
        
        for currency_code, wallet in sorted(self._wallets.items()):
            balance = wallet.balance
            
            if currency_code == base_currency:
                value_in_base = balance
                info_lines.append(f"- {currency_code}: {balance:.2f} → {value_in_base:.2f} {base_currency}")
            else:
                # Упрощенный расчет (в реальном приложении использовать get_total_value логику)
                value_in_base = balance * self._get_exchange_rate(currency_code, base_currency, exchange_rates)
                info_lines.append(f"- {currency_code}: {balance:.4f} → {value_in_base:.2f} {base_currency}")
        
        return info_lines
    
    def _get_exchange_rate(self, from_currency: str, to_currency: str,
                          exchange_rates: Dict[str, float] = None) -> float:
        """
        Вспомогательный метод для получения курса валют.
        
        Args:
            from_currency: Исходная валюта
            to_currency: Целевая валюта
            exchange_rates: Словарь курсов
            
        Returns:
            Курс обмена
        """
        if exchange_rates is None:
            exchange_rates = {
                'EUR_USD': 1.08,
                'BTC_USD': 50000.0,
                'ETH_USD': 3000.0,
                'RUB_USD': 0.011
            }
        
        if from_currency == to_currency:
            return 1.0
        
        rate_key = f"{from_currency}_{to_currency}"
        if rate_key in exchange_rates:
            return exchange_rates[rate_key]
        
        # Если прямого курса нет, пытаемся найти через USD
        if from_currency != 'USD' and to_currency != 'USD':
            usd_to_target = self._get_exchange_rate('USD', to_currency, exchange_rates)
            source_to_usd = self._get_exchange_rate(from_currency, 'USD', exchange_rates)
            if usd_to_target and source_to_usd:
                return source_to_usd * usd_to_target
        
        return 1.0  # Заглушка если курс не найден
    
    def has_currency(self, currency_code: str) -> bool:
        """
        Проверяет наличие валюты в портфеле.
        
        Args:
            currency_code: Код валюты
            
        Returns:
            True если валюта есть, иначе False
        """
        return currency_code.upper() in self._wallets
    
    def remove_currency(self, currency_code: str) -> bool:
        """
        Удаляет валюту из портфеля.
        
        Args:
            currency_code: Код валюты
            
        Returns:
            True если удалено, False если не найдено
        """
        currency_code = currency_code.upper()
        if currency_code in self._wallets:
            del self._wallets[currency_code]
            return True
        return False
    
    def get_currencies(self) -> List[str]:
        """
        Возвращает список кодов валют в портфеле.
        
        Returns:
            Список кодов валют
        """
        return list(self._wallets.keys())
    

    def to_dict(self) -> dict:
        """
        Сериализация портфеля в словарь для JSON.
        
        Returns:
            Словарь для сохранения в JSON
        """
        wallets_dict = {}
        for currency_code, wallet in self._wallets.items():
            wallets_dict[currency_code] = wallet.to_dict()
        
        return {
            "user_id": self._user_id,
            "wallets": wallets_dict
        }


    @classmethod
    def from_dict(cls, data: dict) -> 'Portfolio':
        """
        Создание портфеля из словаря (из JSON).
        
        Args:
            data: Данные портфеля
            
        Returns:
            Объект Portfolio
        """
        wallets = {}
        for currency_code, wallet_data in data["wallets"].items():
            wallets[currency_code] = Wallet.from_dict(wallet_data)
        
        return cls(
            user_id=data["user_id"],
            wallets=wallets
        )
    
    def __str__(self) -> str:
        """Строковое представление портфеля."""
        currencies = ", ".join(self._wallets.keys())
        return f"Portfolio(user_id={self._user_id}, currencies=[{currencies}])"
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Portfolio(user_id={self._user_id}, wallets_count={len(self._wallets)})"
    
    def __len__(self) -> int:
        """Количество кошельков в портфеле."""
        return len(self._wallets)
    
    def __contains__(self, currency_code: str) -> bool:
        """Проверка наличия валюты в портфеле."""
        return currency_code.upper() in self._wallets