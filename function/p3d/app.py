from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, DirectionalLight, AmbientLight, LVector3, Filename, NodePath
from panda3d.core import LPoint3, CollisionNode, CollisionRay, CollisionTraverser, CollisionHandlerQueue
from panda3d.core import CardMaker, TransparencyAttrib, CollisionBox, BitMask32, WindowProperties
import math, os, json, time


class Chess3DApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()  # we will control camera manually

        # FPS Camera setup
        self.camera_pos = Vec3(4, 2, 0.9)  # Start in center, lowered height
        self.camera.set_pos(self.camera_pos)
        self.heading = 0  # Yaw
        self.pitch = 0    # Pitch
        
        # Mouse control
        self.mouse_sensitivity = 0.2
        self.invert_mouse = True  # Инвертированное управление
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Hide mouse cursor and confine to window
        props = WindowProperties()
        props.set_cursor_hidden(True)
        props.set_mouse_mode(WindowProperties.M_confined)  # Confined instead of relative
        self.win.request_properties(props)
        
        # Center mouse initially
        self.center_mouse()
        
        # Movement keys
        self.keys = {
            'w': False, 'a': False, 's': False, 'd': False,
            'space': False, 'shift': False
        }
        self.accept('w', self._set_key, ['w', True])
        self.accept('w-up', self._set_key, ['w', False])
        self.accept('a', self._set_key, ['a', True])
        self.accept('a-up', self._set_key, ['a', False])
        self.accept('s', self._set_key, ['s', True])
        self.accept('s-up', self._set_key, ['s', False])
        self.accept('d', self._set_key, ['d', True])
        self.accept('d-up', self._set_key, ['d', False])
        self.accept('space', self._set_key, ['space', True])
        self.accept('space-up', self._set_key, ['space', False])
        self.accept('shift', self._set_key, ['shift', True])
        self.accept('shift-up', self._set_key, ['shift', False])
        self.accept('escape', self._toggle_mouse)

        # Lighting
        dlight = DirectionalLight('dlight')
        dlight.set_color((0.9, 0.9, 1.0, 1))
        dlnp = self.render.attach_new_node(dlight)
        dlnp.set_hpr(45, -60, 0)
        self.render.set_light(dlnp)

        alight = AmbientLight('alight')
        alight.set_color((0.25, 0.25, 0.3, 1))
        alnp = self.render.attach_new_node(alight)
        self.render.set_light(alnp)

        # Theme colors
        self.theme = self._load_theme()
        self.color_bg = self._norm_color(self.theme.get('Game', {}).get('bg', [30, 30, 35]))
        self.color_light = self._norm_color(self.theme.get('Game', {}).get('light_cell', [110, 110, 120]))
        self.color_dark = self._norm_color(self.theme.get('Game', {}).get('dark_cell', [70, 70, 80]))
        self.color_sel = self._norm_color(self.theme.get('Game', {}).get('selected_cell', [140, 170, 255]))

        # Background color
        self.set_background_color(*self.color_bg)

        # State
        self.selected = None  # (x, y)
        self.piece_nodes = {}  # (x, y) -> NodePath
        self.current_turn = 'white'  # Чей ход
        self.board_state = {}  # (x, y) -> 'team_piece'
        
        # Multiplayer setup: 3D player plays as BLACK, 2D player plays as WHITE
        self.my_team = 'black'
        
        # 2D player marker
        self.player_2d_marker = None
        self.marker_pulse_time = 0

        # Load piece sprites
        self._load_piece_textures()
        
        # Board root
        self.board_np = self.render.attach_new_node('board_root')
        self._build_board()
        self._spawn_start_position()
        self._create_2d_player_marker()

        # FPS update task
        self.task_mgr.add(self._update_fps, 'update-fps')
        
        # Sync check task (для мультиплеера 2D-3D)
        self.last_sync_check = 0
        self.task_mgr.add(self._check_sync, 'check-sync')

        # Picking setup (ray and queue)
        self.picker_ray = CollisionRay()
        self.picker_node = CollisionNode('mouseRay')
        self.picker_node.add_solid(self.picker_ray)
        self.picker_np = self.cam.attach_new_node(self.picker_node)
        self.picker = CollisionTraverser()
        self.pq = CollisionHandlerQueue()
        self.picker.add_collider(self.picker_np, self.pq)
        # Masks
        self.picker_node.set_from_collide_mask(BitMask32.bit(1))
        self.accept('mouse1', self._on_click)

    def _norm_color(self, c):
        # Convert 0..255 rgb to 0..1 rgba
        if isinstance(c, (list, tuple)):
            r, g, b = c[0], c[1], c[2]
            return (r/255.0, g/255.0, b/255.0, 1.0)
        return (0.2, 0.2, 0.25, 1.0)

    def _load_theme(self):
        try:
            with open(os.path.join('data', 'config.json'), 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            theme_name = cfg.get('them', 'base')
            with open(os.path.join('data', 'them', f'{theme_name}.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _load_piece_textures(self):
        """Load 2D sprite textures for chess pieces"""
        self.piece_textures = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        teams = ['white', 'black']
        
        for team in teams:
            for piece in pieces:
                filename = f'{team}_{piece}.png'
                path = os.path.join('data', 'assets', filename)
                if os.path.exists(path):
                    try:
                        tex = self.loader.loadTexture(path)
                        tex.set_magfilter(tex.FT_nearest)
                        tex.set_minfilter(tex.FT_nearest)
                        self.piece_textures[f'{team}_{piece}'] = tex
                    except Exception as e:
                        print(f"Failed to load {filename}: {e}")

    def _build_board(self):
        # Create 8x8 grid of thin boxes/cards as tiles
        self.tiles = []
        cm = CardMaker('tile')
        cm.set_frame(-0.5, 0.5, -0.5, 0.5)
        for x in range(8):
            row = []
            for y in range(8):
                tile_np = self.board_np.attach_new_node(cm.generate())
                tile_np.set_pos(x, y, 0)
                tile_np.set_hpr(0, -90, 0)  # lie flat
                color = self.color_dark if (x + y) % 2 else self.color_light
                tile_np.set_color(*color)

                # Add collision box per tile for picking
                cnode = CollisionNode(f'tile-{x}-{y}')
                cnode.add_solid(CollisionBox(LPoint3(0, 0, 0), 0.49, 0.49, 0.05))
                cpath = tile_np.attach_new_node(cnode)
                cpath.set_collide_mask(BitMask32.bit(1))

                # Tag for identifying tile
                tile_np.set_tag('tile', f'{x},{y}')
                row.append(tile_np)
            self.tiles.append(row)

    def _set_key(self, key, value):
        self.keys[key] = value
    
    def center_mouse(self):
        """Center mouse in window"""
        if self.win:
            props = self.win.get_properties()
            w = props.get_x_size() // 2
            h = props.get_y_size() // 2
            self.win.move_pointer(0, w, h)
            self.last_mouse_x = w
            self.last_mouse_y = h
    
    def _toggle_mouse(self):
        # Toggle mouse capture (ESC to free mouse)
        props = WindowProperties()
        if self.win.get_properties().get_cursor_hidden():
            props.set_cursor_hidden(False)
            props.set_mouse_mode(WindowProperties.M_absolute)
        else:
            props.set_cursor_hidden(True)
            props.set_mouse_mode(WindowProperties.M_confined)
            self.center_mouse()
        self.win.request_properties(props)
    
    def _update_fps(self, task):
        dt = globalClock.get_dt()
        
        # Mouse look
        if self.mouseWatcherNode.has_mouse() and self.win.get_properties().get_cursor_hidden():
            md = self.win.get_pointer(0)
            x = md.get_x()
            y = md.get_y()
            
            if self.last_mouse_x != 0:
                dx = x - self.last_mouse_x
                dy = y - self.last_mouse_y
                
                self.heading -= dx * self.mouse_sensitivity
                # Инвертирование вертикального управления
                if self.invert_mouse:
                    self.pitch -= dy * self.mouse_sensitivity
                else:
                    self.pitch += dy * self.mouse_sensitivity
                self.pitch = max(-89, min(89, self.pitch))
            
            self.last_mouse_x = x
            self.last_mouse_y = y
            
            # Keep mouse near center for smooth control
            props = self.win.get_properties()
            w = props.get_x_size() // 2
            h = props.get_y_size() // 2
            # Recenter if too far from center
            if abs(x - w) > w * 0.4 or abs(y - h) > h * 0.4:
                self.win.move_pointer(0, w, h)
                self.last_mouse_x = w
                self.last_mouse_y = h
        
        # Apply camera rotation
        self.camera.set_hpr(self.heading, self.pitch, 0)
        
        # Movement
        move_speed = 5.0 if self.keys['shift'] else 3.0
        forward = self.camera.get_quat().get_forward()
        right = self.camera.get_quat().get_right()
        
        # Forward/backward (ignore Y vertical component for ground movement)
        forward_flat = Vec3(forward.x, forward.y, 0)
        forward_flat.normalize()
        right_flat = Vec3(right.x, right.y, 0)
        right_flat.normalize()
        
        if self.keys['w']:
            self.camera_pos += forward_flat * move_speed * dt
        if self.keys['s']:
            self.camera_pos -= forward_flat * move_speed * dt
        if self.keys['a']:
            self.camera_pos -= right_flat * move_speed * dt
        if self.keys['d']:
            self.camera_pos += right_flat * move_speed * dt
        if self.keys['space']:
            self.camera_pos.z += move_speed * dt
        if self.keys['shift'] and not (self.keys['w'] or self.keys['a'] or self.keys['s'] or self.keys['d']):
            self.camera_pos.z -= move_speed * dt
        
        # Clamp height (optional - stay above ground)
        self.camera_pos.z = max(0.3, self.camera_pos.z)
        
        self.camera.set_pos(self.camera_pos)
        
        # Периодически сохраняем позицию камеры (20 раз в секунду для плавности)
        if not hasattr(self, 'last_camera_save'):
            self.last_camera_save = 0
        if time.time() - self.last_camera_save >= 0.05:
            self.last_camera_save = time.time()
            self._save_state()
        
        return task.cont
    
    def _check_sync(self, task):
        """Проверяет синхронизацию с 2D режимом"""
        current_time = time.time()
        if current_time - self.last_sync_check >= 0.1:
            self.last_sync_check = current_time
            
            # Загружаем состояние из файла
            try:
                if os.path.exists('data/game_state.json'):
                    with open('data/game_state.json', 'r', encoding='utf-8') as f:
                        state = json.load(f)
                    
                    # Если изменение пришло из 2D режима
                    if state.get('mode') == '2d':
                        # Проверяем изменился ли ход
                        if state.get('current_turn') != self.current_turn:
                            print(f"🔄 [SYNC] Противник походил! Обновляем доску...")
                            self._apply_2d_state(state)
            except Exception as e:
                pass  # Игнорируем ошибки синхронизации
        
        # Обновляем маркер 2D игрока
        self._update_2d_player_marker()
        
        return task.cont
    
    def _apply_2d_state(self, state):
        """Применяет состояние от 2D режима"""
        if not state or 'board' not in state:
            return
        
        try:
            # Удаляем все фигуры
            for node in self.piece_nodes.values():
                node.remove_node()
            self.piece_nodes.clear()
            self.board_state.clear()
            
            # Восстанавливаем фигуры из состояния
            for pos_str, piece_name in state['board'].items():
                x, y = map(int, pos_str.split(','))
                if 0 <= x < 8 and 0 <= y < 8:
                    team, piece_type = piece_name.split('_')
                    self._create_piece(x, y, piece_type, team)
            
            # Обновляем текущий ход
            self.current_turn = state.get('current_turn', 'white')
            print(f"✅ [SYNC] Доска обновлена! Ход: {self.current_turn}")
            
        except Exception as e:
            print(f"❌ [SYNC] Ошибка применения состояния: {e}")

    def _on_click(self):
        if not self.mouseWatcherNode.has_mouse():
            return
        mpos = self.mouseWatcherNode.get_mouse()
        self.picker_ray.set_from_lens(self.camNode, mpos.get_x(), mpos.get_y())
        # Use built-in picking against geometry
        self.pq.clear_entries()
        self.picker.traverse(self.render)
        if self.pq.get_num_entries() == 0:
            return
        self.pq.sort_entries()
        entry = self.pq.get_entry(0)
        node = entry.get_into_node_path()
        np = node.find_net_tag('tile')
        if not np.is_empty():
            tag = np.get_tag('tile')
            x, y = map(int, tag.split(','))
            self._handle_tile_click(x, y)

    def _handle_tile_click(self, x, y):
        tile = self.tiles[x][y]
        # If selecting a piece
        if self.selected is None:
            if (x, y) in self.board_state:
                piece_info = self.board_state[(x, y)]
                team = piece_info.split('_')[0]
                # Can only select own pieces on your turn (3D player = black)
                if team == self.current_turn and team == self.my_team:
                    tile.set_color(*self.color_sel)
                    self.selected = (x, y)
                    print(f"Selected {piece_info} at ({x}, {y})")
                elif team != self.my_team:
                    print(f"⚠️ Сейчас не твой ход! Ты играешь за {self.my_team}, а сейчас ход {self.current_turn}")
            return
        # If clicking same tile -> deselect
        if self.selected == (x, y):
            self._refresh_tile_color(x, y)
            self.selected = None
            return
        # Try to move selected piece
        if self.selected in self.board_state:
            from_x, from_y = self.selected
            piece_info = self.board_state[self.selected]
            team, piece_type = piece_info.split('_')
            
            # Check if move is legal
            if self._is_legal_move(from_x, from_y, x, y, piece_type, team):
                # Remove piece at destination if exists (capture)
                if (x, y) in self.board_state:
                    target_team = self.board_state[(x, y)].split('_')[0]
                    if target_team != team:  # Can only capture opponent
                        self.piece_nodes[(x, y)].remove_node()
                        del self.piece_nodes[(x, y)]
                        del self.board_state[(x, y)]
                        print(f"Captured at ({x}, {y})")
                    else:
                        # Can't capture own piece
                        print("Can't capture your own piece!")
                        self._refresh_tile_color(from_x, from_y)
                        self.selected = None
                        return
                
                # Move piece
                node = self.piece_nodes.pop(self.selected)
                node.set_pos(x, y, 0.5)
                self.piece_nodes[(x, y)] = node
                self.board_state[(x, y)] = self.board_state.pop(self.selected)
                
                # Switch turn
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                print(f"Moved {piece_info} from ({from_x}, {from_y}) to ({x}, {y}). Turn: {self.current_turn}")
                
                # Save state to file for sync
                self._save_state()
            else:
                print(f"Illegal move for {piece_type}")
        
        # Clear selection visuals
        if self.selected:
            sx, sy = self.selected
            self._refresh_tile_color(sx, sy)
        self.selected = None
        # Flash destination briefly
        tile.set_color(*self.color_sel)
        def flash_done(task):
            self._refresh_tile_color(x, y)
            return task.done
        self.do_method_later(0.12, flash_done, 'flash-dest')

    def _refresh_tile_color(self, x, y):
        base_color = self.color_dark if (x + y) % 2 else self.color_light
        self.tiles[x][y].set_color(*base_color)

    def _spawn_start_position(self):
        # Standard chess initial placement
        white_back = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        black_back = white_back
        for i, piece in enumerate(white_back):
            self._create_piece(i, 0, piece, team='white')
            self._create_piece(i, 7, piece, team='black')
        for i in range(8):
            self._create_piece(i, 1, 'pawn', team='white')
            self._create_piece(i, 6, 'pawn', team='black')

    def _create_piece(self, x, y, piece, team='white'):
        # Create 2D sprite billboard as a piece
        key = f'{team}_{piece}'
        if key not in self.piece_textures:
            print(f"Warning: texture {key} not found")
            return
        
        # Create card with texture
        cm = CardMaker(f'piece_{key}')
        cm.set_frame(-0.25, 0.25, -0.25, 0.25)  # Size of sprite
        node = self.render.attach_new_node(cm.generate())
        node.set_texture(self.piece_textures[key])
        node.set_transparency(TransparencyAttrib.M_alpha)
        node.set_pos(x, y, 0.5)  # Lift pieces above board
        node.set_billboard_point_eye()  # Always face camera
        node.set_scale(1.2)  # Scale up for visibility
        
        self.piece_nodes[(x, y)] = node
        self.board_state[(x, y)] = key
    
    def _is_legal_move(self, from_x, from_y, to_x, to_y, piece_type, team):
        """Check if move is legal for given piece"""
        dx = to_x - from_x
        dy = to_y - from_y
        
        # Check bounds
        if not (0 <= to_x < 8 and 0 <= to_y < 8):
            return False
        
        # Can't move to same square
        if dx == 0 and dy == 0:
            return False
        
        # Check destination is not occupied by own piece
        if (to_x, to_y) in self.board_state:
            target_team = self.board_state[(to_x, to_y)].split('_')[0]
            if target_team == team:
                return False
        
        # Piece-specific rules
        if piece_type == 'pawn':
            direction = 1 if team == 'white' else -1
            # Forward move
            if dx == 0 and dy == direction:
                return (to_x, to_y) not in self.board_state
            # Starting double move
            start_row = 1 if team == 'white' else 6
            if from_y == start_row and dx == 0 and dy == 2 * direction:
                mid_y = from_y + direction
                return (to_x, to_y) not in self.board_state and (from_x, mid_y) not in self.board_state
            # Capture diagonal
            if abs(dx) == 1 and dy == direction:
                return (to_x, to_y) in self.board_state
            return False
        
        elif piece_type == 'rook':
            if dx == 0 or dy == 0:
                return self._is_path_clear(from_x, from_y, to_x, to_y)
            return False
        
        elif piece_type == 'knight':
            return (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)
        
        elif piece_type == 'bishop':
            if abs(dx) == abs(dy):
                return self._is_path_clear(from_x, from_y, to_x, to_y)
            return False
        
        elif piece_type == 'queen':
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                return self._is_path_clear(from_x, from_y, to_x, to_y)
            return False
        
        elif piece_type == 'king':
            return abs(dx) <= 1 and abs(dy) <= 1
        
        return False
    
    def _is_path_clear(self, from_x, from_y, to_x, to_y):
        """Check if path between two squares is clear"""
        dx = 0 if to_x == from_x else (1 if to_x > from_x else -1)
        dy = 0 if to_y == from_y else (1 if to_y > from_y else -1)
        
        x, y = from_x + dx, from_y + dy
        while (x, y) != (to_x, to_y):
            if (x, y) in self.board_state:
                return False
            x += dx
            y += dy
        return True
    
    def _save_state(self):
        """Save game state to file for sync with 2D mode"""
        try:
            state = {
                'board': {f'{x},{y}': piece for (x, y), piece in self.board_state.items()},
                'current_turn': self.current_turn,
                'camera_pos': [self.camera_pos.x, self.camera_pos.y, self.camera_pos.z],
                'camera_heading': self.heading,
                'camera_pitch': self.pitch,
                'last_update': time.time(),
                'mode': '3d'
            }
            with open('data/game_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")


    def _create_2d_player_marker(self):
        """Создаёт маркер для 2D игрока (синяя пульсирующая сфера)"""
        # Создаём простую сферу используя CardMaker (как спрайты фигур)
        try:
            from panda3d.core import CardMaker
            
            # Создаём карту для маркера
            cm = CardMaker('2d_player_marker')
            cm.set_frame(-0.2, 0.2, -0.2, 0.2)  # Размер маркера
            
            self.player_2d_marker = self.render.attach_new_node(cm.generate())
            self.player_2d_marker.set_color(0.3, 0.7, 1.0, 0.7)  # Синий полупрозрачный
            self.player_2d_marker.set_transparency(TransparencyAttrib.M_alpha)
            self.player_2d_marker.set_billboard_point_eye()  # Всегда смотрит на камеру
            self.player_2d_marker.hide()  # Скрываем до получения данных
            print("✅ Маркер 2D игрока создан")
        except Exception as e:
            print(f"⚠️ Не удалось создать маркер 2D игрока: {e}")
            self.player_2d_marker = None
    
    def _update_2d_player_marker(self):
        """Обновляет позицию маркера 2D игрока"""
        if not self.player_2d_marker:
            return
        
        # Читаем позицию из game_state.json
        try:
            if os.path.exists('data/game_state.json'):
                with open('data/game_state.json', 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Если это данные от 2D игрока
                if state.get('mode') == '2d':
                    # Вычисляем позицию на основе хода (не камеры, т.к. у 2D нет камеры)
                    # Показываем маркер над последней походившей фигурой или в центре доски
                    # Для упрощения - ставим в центр доски (4, 4)
                    marker_x = 4
                    marker_y = 4
                    marker_z = 1.5  # Над доской
                    
                    # Пульсация
                    self.marker_pulse_time += 0.05
                    pulse = abs(math.sin(self.marker_pulse_time * 3.0))
                    scale = 0.12 + pulse * 0.05
                    
                    self.player_2d_marker.set_pos(marker_x, marker_y, marker_z)
                    self.player_2d_marker.set_scale(scale)
                    self.player_2d_marker.show()
                    return
        except:
            pass
        
        # Если нет данных, скрываем маркер
        self.player_2d_marker.hide()

def run_panda_app():
    app = Chess3DApp()
    app.run()


