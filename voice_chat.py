"""
Простой голосовой чат для локальной сети
Использует PyAudio для записи/воспроизведения и сокеты для передачи данных
"""

import socket
import pyaudio
import threading
import sys
import time

# Настройки аудио
CHUNK = 1024  # Размер буфера
FORMAT = pyaudio.paInt16  # Формат аудио (16-bit)
CHANNELS = 1  # Моно
RATE = 44100  # Частота дискретизации

# Настройки сети
PORT = 5050


class VoiceChat:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.is_running = False
        self.is_connected = False
        self.sock = None
        self.conn = None
        
    def start_server(self, host='0.0.0.0'):
        """Запуск в режиме сервера (ожидание подключения)"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((host, PORT))
            self.sock.listen(1)
            
            print(f"[СЕРВЕР] Ожидание подключения на порту {PORT}...")
            print(f"[СЕРВЕР] Ваш IP для подключения клиента:")
            
            # Получаем локальный IP
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                print(f"[СЕРВЕР] {local_ip}:{PORT}")
            except:
                print(f"[СЕРВЕР] localhost:{PORT}")
            
            self.conn, addr = self.sock.accept()
            print(f"[СЕРВЕР] Подключение установлено с {addr}")
            self.is_connected = True
            self.is_running = True
            
            # Запускаем потоки для отправки и получения
            send_thread = threading.Thread(target=self.send_audio, args=(self.conn,))
            receive_thread = threading.Thread(target=self.receive_audio, args=(self.conn,))
            
            send_thread.start()
            receive_thread.start()
            
            print("[ГОЛОСОВОЙ ЧАТ] Соединение активно! Говорите в микрофон.")
            print("[ГОЛОСОВОЙ ЧАТ] Нажмите Ctrl+C для выхода")
            
            send_thread.join()
            receive_thread.join()
            
        except KeyboardInterrupt:
            print("\n[СЕРВЕР] Завершение работы...")
        except Exception as e:
            print(f"[ОШИБКА СЕРВЕРА] {e}")
        finally:
            self.cleanup()
    
    def start_client(self, host):
        """Запуск в режиме клиента (подключение к серверу)"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[КЛИЕНТ] Подключение к {host}:{PORT}...")
            
            self.sock.connect((host, PORT))
            print(f"[КЛИЕНТ] Подключено к серверу!")
            self.is_connected = True
            self.is_running = True
            
            # Запускаем потоки для отправки и получения
            send_thread = threading.Thread(target=self.send_audio, args=(self.sock,))
            receive_thread = threading.Thread(target=self.receive_audio, args=(self.sock,))
            
            send_thread.start()
            receive_thread.start()
            
            print("[ГОЛОСОВОЙ ЧАТ] Соединение активно! Говорите в микрофон.")
            print("[ГОЛОСОВОЙ ЧАТ] Нажмите Ctrl+C для выхода")
            
            send_thread.join()
            receive_thread.join()
            
        except KeyboardInterrupt:
            print("\n[КЛИЕНТ] Завершение работы...")
        except ConnectionRefusedError:
            print(f"[ОШИБКА] Не удалось подключиться к {host}:{PORT}")
            print("[ОШИБКА] Убедитесь, что сервер запущен и IP адрес верный")
        except Exception as e:
            print(f"[ОШИБКА КЛИЕНТА] {e}")
        finally:
            self.cleanup()
    
    def send_audio(self, connection):
        """Отправка аудио через сокет"""
        stream = None
        try:
            # Открываем поток для записи с микрофона
            stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            while self.is_running:
                try:
                    # Читаем данные с микрофона
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    # Отправляем данные
                    connection.sendall(data)
                except Exception as e:
                    if self.is_running:
                        print(f"[ОШИБКА ОТПРАВКИ] {e}")
                    break
                    
        except Exception as e:
            print(f"[ОШИБКА МИКРОФОНА] {e}")
            print("[ПОДСКАЗКА] Убедитесь, что микрофон подключен и доступен")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            self.is_running = False
    
    def receive_audio(self, connection):
        """Получение и воспроизведение аудио"""
        stream = None
        try:
            # Открываем поток для воспроизведения
            stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK
            )
            
            while self.is_running:
                try:
                    # Получаем данные
                    data = connection.recv(CHUNK * 2)
                    if not data:
                        print("\n[СОЕДИНЕНИЕ] Связь прервана")
                        break
                    # Воспроизводим данные
                    stream.write(data)
                except Exception as e:
                    if self.is_running:
                        print(f"[ОШИБКА ПОЛУЧЕНИЯ] {e}")
                    break
                    
        except Exception as e:
            print(f"[ОШИБКА ДИНАМИКОВ] {e}")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            self.is_running = False
    
    def cleanup(self):
        """Очистка ресурсов"""
        self.is_running = False
        self.is_connected = False
        
        time.sleep(0.5)  # Даем потокам время на завершение
        
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        
        self.audio.terminate()


def print_menu():
    """Вывод меню"""
    print("\n" + "="*50)
    print("    ГОЛОСОВОЙ ЧАТ ДЛЯ ЛОКАЛЬНОЙ СЕТИ")
    print("="*50)
    print("\n1. Запустить как СЕРВЕР (ожидать подключения)")
    print("2. Подключиться как КЛИЕНТ")
    print("3. Выход")
    print("\n" + "="*50)


def main():
    """Главная функция"""
    print("\n[ИНИЦИАЛИЗАЦИЯ] Проверка аудиоустройств...")
    
    # Проверяем доступность PyAudio
    try:
        p = pyaudio.PyAudio()
        
        # Проверяем наличие устройств ввода
        input_devices = 0
        output_devices = 0
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices += 1
            if info['maxOutputChannels'] > 0:
                output_devices += 1
        
        p.terminate()
        
        if input_devices == 0:
            print("[ВНИМАНИЕ] Микрофон не обнаружен!")
        else:
            print(f"[OK] Найдено устройств ввода: {input_devices}")
            
        if output_devices == 0:
            print("[ВНИМАНИЕ] Устройство вывода не обнаружено!")
        else:
            print(f"[OK] Найдено устройств вывода: {output_devices}")
            
    except Exception as e:
        print(f"[ОШИБКА] Проблема с аудио: {e}")
        return
    
    while True:
        print_menu()
        choice = input("\nВыберите опцию (1-3): ").strip()
        
        if choice == '1':
            # Режим сервера
            chat = VoiceChat()
            chat.start_server()
            
        elif choice == '2':
            # Режим клиента
            host = input("\nВведите IP адрес сервера: ").strip()
            if not host:
                print("[ОШИБКА] IP адрес не может быть пустым!")
                continue
            
            chat = VoiceChat()
            chat.start_client(host)
            
        elif choice == '3':
            print("\n[ВЫХОД] До свидания!")
            break
            
        else:
            print("\n[ОШИБКА] Неверный выбор! Введите 1, 2 или 3")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ВЫХОД] Программа завершена")
    except Exception as e:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] {e}")
        input("\nНажмите Enter для выхода...")

