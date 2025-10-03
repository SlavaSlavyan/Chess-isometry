"""
Система логирования с поддержкой эмодзи
"""
import sys
import io

class Logger:
    """Безопасный логгер с поддержкой эмодзи"""
    
    def __init__(self):
        # Устанавливаем UTF-8 для корректного вывода
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        # Словарь замен эмодзи на ASCII (на случай проблем)
        self.emoji_fallback = {
            '✅': '[OK]',
            '❌': '[X]',
            '⚠️': '[!]',
            '🎨': '[ART]',
            '🔧': '[CFG]',
            '🎴': '[CARD]',
            '🎯': '[TARGET]',
            '💚': '[+]',
            '🔄': '[>>]',
            '🎉': '[WIN]',
            '⚡': '[!]',
            '🌫️': '[FOG]',
            '🔊': '[SND]',
            '♪': '[MUSIC]',
            '♟️': '[PAWN]',
            '🚀': '[READY]',
        }
        
        self.use_fallback = False
    
    def log(self, message, level='INFO'):
        """
        Логирование сообщения
        
        Args:
            message: Текст сообщения
            level: Уровень (INFO, WARNING, ERROR, SUCCESS)
        """
        try:
            # Пытаемся вывести с эмодзи
            if self.use_fallback:
                message = self._replace_emoji(message)
            print(message)
        except UnicodeEncodeError:
            # Если не получилось - переключаемся на ASCII
            self.use_fallback = True
            message = self._replace_emoji(message)
            print(message)
        except Exception as e:
            # На всякий случай - самый простой вывод
            print(f"[LOG] {message.encode('ascii', 'ignore').decode('ascii')}")
    
    def _replace_emoji(self, text):
        """Заменяет эмодзи на ASCII"""
        for emoji, replacement in self.emoji_fallback.items():
            text = text.replace(emoji, replacement)
        return text
    
    def info(self, message):
        """Информационное сообщение"""
        self.log(f"ℹ️ {message}", 'INFO')
    
    def success(self, message):
        """Успешное выполнение"""
        self.log(f"✅ {message}", 'SUCCESS')
    
    def warning(self, message):
        """Предупреждение"""
        self.log(f"⚠️ {message}", 'WARNING')
    
    def error(self, message):
        """Ошибка"""
        self.log(f"❌ {message}", 'ERROR')
    
    def card(self, message):
        """Действие с картой"""
        self.log(f"🎴 {message}", 'CARD')
    
    def game(self, message):
        """Игровое событие"""
        self.log(f"🎯 {message}", 'GAME')

# Глобальный логгер
_logger = None

def get_logger():
    """Получить глобальный логгер"""
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger

def safe_print(message):
    """Безопасный вывод с автоматической обработкой эмодзи"""
    get_logger().log(message)

