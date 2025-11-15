import functools
import logging
import inspect
from datetime import datetime
from typing import Any, Callable

# Создаем директорию для логов
import os
os.makedirs('logs', exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    handlers=[
        logging.FileHandler('logs/actions.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_action(action_name: str = None, verbose: bool = False):
    """
    Декоратор для логирования операций.
    
    Args:
        action_name: Название операции (BUY/SELL/REGISTER/LOGIN)
        verbose: Подробное логирование
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Определяем имя операции
            operation = action_name or func.__name__.upper()
            
            # Базовые данные для лога
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'action': operation,
                'result': 'OK'
            }
            
            try:
                # Извлекаем параметры из аргументов функции
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                # Добавляем основные параметры в лог
                params = bound_args.arguments
                
                if 'user_id' in params:
                    log_data['user'] = params['user_id']
                elif 'username' in params:
                    log_data['user'] = params['username']
                
                if 'currency_code' in params:
                    log_data['currency'] = params['currency_code']
                elif 'currency' in params:
                    log_data['currency'] = params['currency']
                
                if 'amount' in params:
                    log_data['amount'] = f"{params['amount']:.4f}"
                
                if 'from_currency' in params:
                    log_data['from'] = params['from_currency']
                if 'to_currency' in params:
                    log_data['to'] = params['to_currency']
                
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Если функция возвращает словарь с дополнительными данными, добавляем их
                if isinstance(result, dict):
                    if 'rate' in result:
                        log_data['rate'] = f"{result['rate']:.2f}"
                    if 'base' in result:
                        log_data['base'] = result['base']
                
                # Логируем успех
                logger.info(f"{operation} {_format_log_data(log_data)}")
                return result
                
            except Exception as e:
                # Логируем ошибку
                log_data.update({
                    'result': 'ERROR',
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                })
                logger.error(f"{operation} {_format_log_data(log_data)}")
                raise  # Пробрасываем исключение дальше
                
        return wrapper
    return decorator


def _format_log_data(data: dict) -> str:
    """Форматирование данных лога в строку."""
    parts = []
    for key, value in data.items():
        if key != 'action':
            # Для числовых значений не ставим кавычки
            if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '').isdigit()):
                parts.append(f"{key}={value}")
            else:
                parts.append(f"{key}='{value}'")
    return ' '.join(parts)


# Специализированные декораторы для конкретных операций
def log_buy(func: Callable) -> Callable:
    return log_action('BUY', verbose=True)(func)


def log_sell(func: Callable) -> Callable:
    return log_action('SELL', verbose=True)(func)


def log_register(func: Callable) -> Callable:
    return log_action('REGISTER')(func)


def log_login(func: Callable) -> Callable:
    return log_action('LOGIN')(func)


def log_get_rate(func: Callable) -> Callable:
    return log_action('GET_RATE')(func)