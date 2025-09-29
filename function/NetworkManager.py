import socket
import threading
import json
import time
from typing import Dict, Any, Optional, Callable

class NetworkManager:
    """Менеджер сетевых соединений для локального мультиплеера"""
    
    def __init__(self):
        self.socket = None
        self.is_host = False
        self.is_connected = False
        self.client_socket = None
        self.client_address = None
        
        # Callbacks для обработки событий
        self.on_message_received: Optional[Callable] = None
        self.on_client_connected: Optional[Callable] = None
        self.on_client_disconnected: Optional[Callable] = None
        self.on_connection_lost: Optional[Callable] = None
        
        # Потоки для прослушивания
        self.listen_thread = None
        self.running = False
        
        # Буфер сообщений
        self.message_queue = []
        self.queue_lock = threading.Lock()
        
    def start_host(self, port: int = 12345) -> bool:
        """Запускает хост-сервер"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', port))
            self.socket.listen(1)
            
            self.is_host = True
            self.running = True
            
            # Запускаем поток для прослушивания подключений
            self.listen_thread = threading.Thread(target=self._host_listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            
            print(f"🌐 Хост запущен на порту {port}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка запуска хоста: {e}")
            return False
    
    def connect_to_host(self, host_ip: str, port: int = 12345) -> bool:
        """Подключается к хосту"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host_ip, port))
            
            self.is_host = False
            self.is_connected = True
            self.running = True
            
            # Запускаем поток для прослушивания сообщений
            self.listen_thread = threading.Thread(target=self._client_listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            
            print(f"🔗 Подключен к хосту {host_ip}:{port}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False
    
    def _host_listen_loop(self):
        """Основной цикл прослушивания для хоста"""
        while self.running:
            try:
                client_socket, client_address = self.socket.accept()
                self.client_socket = client_socket
                self.client_address = client_address
                self.is_connected = True
                
                print(f"🎮 Игрок подключился: {client_address}")
                
                if self.on_client_connected:
                    self.on_client_connected(client_address)
                
                # Начинаем прослушивать сообщения от клиента
                self._receive_messages(client_socket)
                
            except Exception as e:
                if self.running:
                    print(f"❌ Ошибка в host_listen_loop: {e}")
                break
    
    def _client_listen_loop(self):
        """Основной цикл прослушивания для клиента"""
        try:
            self._receive_messages(self.socket)
        except Exception as e:
            if self.running:
                print(f"❌ Ошибка в client_listen_loop: {e}")
            self._handle_connection_lost()
    
    def _receive_messages(self, sock):
        """Получает сообщения от удаленного клиента"""
        buffer = ""
        while self.running:
            try:
                data = sock.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                buffer += data
                
                # Обрабатываем завершенные сообщения (разделенные \n)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            message = json.loads(line.strip())
                            self._handle_message(message)
                        except json.JSONDecodeError:
                            print(f"❌ Ошибка декодирования JSON: {line}")
                            
            except Exception as e:
                if self.running:
                    print(f"❌ Ошибка получения сообщения: {e}")
                break
        
        self._handle_connection_lost()
    
    def _handle_message(self, message: Dict[str, Any]):
        """Обрабатывает полученное сообщение"""
        with self.queue_lock:
            self.message_queue.append(message)
        
        if self.on_message_received:
            self.on_message_received(message)
    
    def _handle_connection_lost(self):
        """Обрабатывает потерю соединения"""
        self.is_connected = False
        
        if self.on_connection_lost:
            self.on_connection_lost()
        
        print("🔌 Соединение потеряно")
    
    def send_message(self, message_type: str, data: Dict[str, Any] = None) -> bool:
        """Отправляет сообщение"""
        if not self.is_connected:
            return False
        
        message = {
            'type': message_type,
            'timestamp': time.time(),
            'data': data or {}
        }
        
        try:
            json_message = json.dumps(message) + '\n'
            
            if self.is_host and self.client_socket:
                self.client_socket.send(json_message.encode('utf-8'))
            elif not self.is_host and self.socket:
                self.socket.send(json_message.encode('utf-8'))
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            return False
    
    def get_messages(self) -> list:
        """Получает все накопленные сообщения"""
        with self.queue_lock:
            messages = self.message_queue.copy()
            self.message_queue.clear()
            return messages
    
    def get_local_ip(self) -> str:
        """Получает локальный IP адрес"""
        try:
            # Создаем временное соединение для определения IP
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def disconnect(self):
        """Закрывает соединение"""
        self.running = False
        self.is_connected = False
        
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.socket:
                self.socket.close()
        except:
            pass
        
        print("🚪 Соединение закрыто")
    
    def __del__(self):
        """Деструктор"""
        self.disconnect()
