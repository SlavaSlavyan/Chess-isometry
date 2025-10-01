import traceback
import sys
import os
from datetime import datetime
from typing import Optional, Callable

class ErrorHandler:
    """Система обработки ошибок с визуальным отображением в игре"""
    
    def __init__(self):
        self.error_log_file = "data/error_log.txt"
        self.current_error = None
        self.error_visible = False
        self.is_handling_error = False  # Флаг для предотвращения бесконечного цикла
        
        # Создаем папку для логов если не существует
        os.makedirs(os.path.dirname(self.error_log_file), exist_ok=True)
    
    def handle_error(self, error_type: type, error_value: Exception, error_traceback):
        """Обрабатывает ошибку и сохраняет информацию"""
        # Защита от бесконечного цикла ошибок
        if self.is_handling_error:
            print("⚠️ Ошибка при обработке ошибки! Пропускаем...")
            return
        
        self.is_handling_error = True
        
        try:
            # Получаем полный traceback
            tb_lines = traceback.format_exception(error_type, error_value, error_traceback)
            tb_text = ''.join(tb_lines)
            
            # Парсим информацию об ошибке
            tb_list = traceback.extract_tb(error_traceback)
            if tb_list:
                last_frame = tb_list[-1]
                file_name = os.path.basename(last_frame.filename)
                line_number = last_frame.lineno
                function_name = last_frame.name
                code_line = last_frame.line
            else:
                file_name = "Unknown"
                line_number = 0
                function_name = "Unknown"
                code_line = ""
            
            # Сохраняем информацию об ошибке
            self.current_error = {
                'type': error_type.__name__,
                'message': str(error_value),
                'file': file_name,
                'line': line_number,
                'function': function_name,
                'code': code_line,
                'full_traceback': tb_text,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Показываем окно ошибки
            self.error_visible = True
            
            # Логируем в файл
            self.log_error_to_file()
            
            # Выводим в консоль
            print("\n" + "="*80)
            print("🔴 КРИТИЧЕСКАЯ ОШИБКА ПЕРЕХВАЧЕНА!")
            print("="*80)
            print(tb_text)
            print("="*80 + "\n")
            
        finally:
            # Сбрасываем флаг обработки ошибки
            self.is_handling_error = False
    
    def log_error_to_file(self):
        """Сохраняет ошибку в лог-файл"""
        if not self.current_error:
            return
        
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*80 + "\n")
                f.write(f"[{self.current_error['timestamp']}]\n")
                f.write(f"Тип: {self.current_error['type']}\n")
                f.write(f"Сообщение: {self.current_error['message']}\n")
                f.write(f"Файл: {self.current_error['file']}\n")
                f.write(f"Строка: {self.current_error['line']}\n")
                f.write(f"Функция: {self.current_error['function']}\n")
                f.write(f"Код: {self.current_error['code']}\n")
                f.write("\nПолный traceback:\n")
                f.write(self.current_error['full_traceback'])
                f.write("="*80 + "\n")
        except Exception as e:
            print(f"❌ Не удалось записать в лог: {e}")
    
    def clear_error(self):
        """Закрывает окно ошибки"""
        self.error_visible = False
        self.current_error = None
        self.is_handling_error = False  # Сбрасываем флаг
    
    def is_error_visible(self) -> bool:
        """Проверяет, видно ли окно ошибки"""
        return self.error_visible and self.current_error is not None
    
    def get_error_info(self) -> Optional[dict]:
        """Возвращает информацию об текущей ошибке"""
        return self.current_error

def safe_call(func: Callable):
    """Декоратор для безопасного вызова функций с обработкой ошибок"""
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            if hasattr(self, 'ErrorHandler'):
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.ErrorHandler.handle_error(exc_type, exc_value, exc_traceback)
            else:
                raise
    return wrapper
