import pygame
import math
import time
from supermarket_board import supermarket_layout, PRODUCT_CATEGORIES, get_category_by_key, get_shelf_center
from enhanced_pathfinding import EnhancedPathFinder

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1400
HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)          # Walkways
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

class SimpleSoundManager:
    """Simplified sound manager"""
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False
            print("He thong am thanh khong kha dung")
    
    def play_sound(self, sound_name):
        """Play a simple beep sound"""
        if self.sound_enabled:
            try:
                # Create a simple beep using pygame
                duration = 0.1
                sample_rate = 22050
                frames = int(duration * sample_rate)
                
                # Simple sine wave
                import numpy as np
                frequency = 800 if sound_name == 'navigate' else 1200
                arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
                arr = (arr * 32767).astype(np.int16)
                arr = np.repeat(arr.reshape(frames, 1), 2, axis=1)
                
                sound = pygame.sndarray.make_sound(arr)
                sound.play()
            except:
                pass  # Silently fail if sound doesn't work
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

class FinalSupermarketFindBot:
    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("🤖 FINDBOT - NGON LUA PTIT")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 22)
        self.font_large = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)
        
        # Core systems
        self.layout = supermarket_layout
        self.pathfinder = EnhancedPathFinder(self.layout)
        self.sound_manager = SimpleSoundManager()
        
        # Game state - Start near entrance
        self.user_pos = (26, 17)  # Near entrance at bottom center
        self.target_product = None
        self.current_path = []
        self.path_index = 0
        self.selected_category = None
        
        # UI state
        self.show_help = True
        self.animation_time = 0
        self.path_animation_index = 0
        
        # Statistics
        self.total_searches = 0
        self.total_distance = 0
        
        # Initialize last_direction
        self.last_direction = (0, 0)
        
    def draw_board(self):
        """Draw the supermarket layout with black walkways"""
        board_width = WIDTH - 350  # Leave more space for UI panel
        board_height = HEIGHT - 50
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                x = j * cell_width
                y = i * cell_height + 25  # Offset for title
                cell = self.layout[i][j]
                
                # Draw cell background
                if cell == 0:  # Walkway - BLACK
                    pygame.draw.rect(self.screen, BLACK, (x, y, cell_width, cell_height))
                elif cell == 1:  # Product shelf
                    pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, cell_width, cell_height))
                elif cell == 2:  # Special product
                    pygame.draw.rect(self.screen, PURPLE, (x, y, cell_width, cell_height))
                elif cell == 9:  # Entrance/Exit
                    pygame.draw.rect(self.screen, WHITE, (x, y, cell_width, cell_height))
                elif cell >= 3:  # Walls
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, cell_width, cell_height))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, GRAY, (x, y, cell_width, cell_height), 1)
    
    def draw_products(self):
        """Draw product categories with different colors"""
        board_width = WIDTH - 350
        board_height = HEIGHT - 50
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        for category, info in PRODUCT_CATEGORIES.items():
            color = info['color']
            positions = info['positions']
            shelf_id = info['shelf_id']
            
            for i, (row, col) in enumerate(positions):
                if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
                    x = col * cell_width
                    y = row * cell_height + 25
                    
                    # Draw product area
                    pygame.draw.rect(self.screen, color, (x + 1, y + 1, cell_width - 2, cell_height - 2))
                    
                    # Add shine effect
                    shine_color = tuple(min(255, c + 30) for c in color)
                    pygame.draw.rect(self.screen, shine_color, (x + 1, y + 1, cell_width - 2, 2))
                    
                    # Draw shelf number on center of shelf
                    if i == len(positions) // 2:  # Center position
                        text = self.font_small.render(str(shelf_id), True, WHITE)
                        text_rect = text.get_rect(center=(x + cell_width//2, y + cell_height//2))
                        
                        # Add text background
                        bg_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 1, text_rect.width + 4, text_rect.height + 2)
                        pygame.draw.rect(self.screen, BLACK, bg_rect)
                        
                        self.screen.blit(text, text_rect)
    
    def draw_user(self):
        """Draw user with animation"""
        board_width = WIDTH - 350
        board_height = HEIGHT - 50
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        x = self.user_pos[1] * cell_width + cell_width // 2
        y = self.user_pos[0] * cell_height + cell_height // 2 + 25
        
        # Animated user icon
        pulse = math.sin(self.animation_time * 5) * 2
        radius = 8 + pulse
        
        # Draw shadow
        pygame.draw.circle(self.screen, DARK_GRAY, (x + 2, y + 2), int(radius))
        
        # Draw user (FindBot)
        pygame.draw.circle(self.screen, RED, (x, y), int(radius))
        pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 2)
        
        # Draw "FB" text for FindBot
        fb_text = self.font_small.render("FB", True, WHITE)
        fb_rect = fb_text.get_rect(center=(x, y))
        self.screen.blit(fb_text, fb_rect)
        
        # Draw direction indicator
        if hasattr(self, 'last_direction') and self.last_direction != (0, 0):
            dx, dy = self.last_direction
            end_x = x + dx * 12
            end_y = y + dy * 12
            pygame.draw.line(self.screen, WHITE, (x, y), (end_x, end_y), 3)
    
    def draw_path(self):
        """Draw path with animation"""
        if not self.current_path:
            return
        
        board_width = WIDTH - 350
        board_height = HEIGHT - 50
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        # Animate path drawing
        visible_path_length = min(len(self.current_path), int(self.path_animation_index))
        
        # Draw path segments
        points = []
        for i in range(visible_path_length):
            row, col = self.current_path[i]
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2 + 25
            points.append((x, y))
        
        # Draw path line
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Bright yellow path on black walkways
                pygame.draw.line(self.screen, YELLOW, points[i], points[i + 1], 5)
        
        # Draw path dots
        for i, point in enumerate(points):
            if i < visible_path_length - 1:
                pulse = math.sin(self.animation_time * 3 + i * 0.5) * 2
                radius = 5 + pulse
                pygame.draw.circle(self.screen, YELLOW, point, int(radius))
        
        # Draw target with special effect
        if self.current_path and visible_path_length == len(self.current_path):
            target_row, target_col = self.current_path[-1]
            x = target_col * cell_width + cell_width // 2
            y = target_row * cell_height + cell_height // 2 + 25
            
            # Pulsing target
            pulse = math.sin(self.animation_time * 4) * 4
            radius = 15 + pulse
            
            pygame.draw.circle(self.screen, GREEN, (x, y), int(radius))
            pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 3)
            
            # Target crosshair
            pygame.draw.line(self.screen, WHITE, (x - 10, y), (x + 10, y), 3)
            pygame.draw.line(self.screen, WHITE, (x, y - 10), (x, y + 10), 3)
    
    def draw_entrance(self):
        """Draw entrance marker"""
        board_width = WIDTH - 350
        board_height = HEIGHT - 50
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        # Draw entrance text
        entrance_text = self.font_medium.render("LOI VAO", True, BLACK)
        entrance_x = 16 * cell_width + cell_width // 2
        entrance_y = 27 * cell_height + 25
        entrance_rect = entrance_text.get_rect(center=(entrance_x, entrance_y))
        
        # Background for text
        bg_rect = pygame.Rect(entrance_rect.x - 5, entrance_rect.y - 3, entrance_rect.width + 10, entrance_rect.height + 6)
        pygame.draw.rect(self.screen, WHITE, bg_rect)
        pygame.draw.rect(self.screen, BLACK, bg_rect, 2)
        
        self.screen.blit(entrance_text, entrance_rect)
    
    def draw_ui_panel(self):
        """Draw the UI panel with controls and information"""
        panel_x = WIDTH - 340
        panel_width = 330
        
        # Panel background
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, 0, panel_width, HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (panel_x, 0, panel_width, HEIGHT), 2)
        
        y_offset = 10
        
        # Title
        title = self.font_large.render("🤖 FINDBOT - NGON LUA PTIT", True, WHITE)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 35
        
        # Instructions
        instructions = [
            "🎮 DIEU KHIEN:",
            "So 1-9,0: Ke 1-10",
            "Q,W,E,R,T: Ke 11-15", 
            "Y,U,I,O,P: Ke 16-20",
            "WASD/Mui ten: Di chuyen",
            "M: Bat/tat am thanh",
            "ESC: Huy tim kiem",
            "",
            "📍 DANH SACH KE HANG:"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(text, (panel_x + 5, y_offset))
            y_offset += 18
        
        # Product categories - display in compact format
        shelf_count = 0
        for category, info in PRODUCT_CATEGORIES.items():
            shelf_count += 1
            color = info['color']
            key = info['key']
            name = info['name']
            shelf_id = info['shelf_id']
            
            # Color indicator
            pygame.draw.rect(self.screen, color, (panel_x + 5, y_offset, 12, 12))
            pygame.draw.rect(self.screen, WHITE, (panel_x + 5, y_offset, 12, 12), 1)
            
            # Category text
            text = f"{key.upper()}.{shelf_id:2d} {name}"
            if len(text) > 32:
                text = text[:29] + "..."
            
            color_to_use = WHITE
            if self.selected_category == category:
                color_to_use = YELLOW
            
            category_text = self.font_small.render(text, True, color_to_use)
            self.screen.blit(category_text, (panel_x + 22, y_offset))
            y_offset += 16
            
            # Add spacing every 4 items (one row)
            if shelf_count % 4 == 0:
                y_offset += 5
        
        # Current status
        y_offset += 10
        status_text = self.font_medium.render("📊 TRANG THAI:", True, WHITE)
        self.screen.blit(status_text, (panel_x + 5, y_offset))
        y_offset += 22
        
        if self.selected_category:
            info = PRODUCT_CATEGORIES[self.selected_category]
            status = f"Dich: Ke {info['shelf_id']} - {info['name']}"
            if len(status) > 35:
                status = status[:32] + "..."
            
            text = self.font_small.render(status, True, YELLOW)
            self.screen.blit(text, (panel_x + 5, y_offset))
            y_offset += 18
            
            if self.current_path:
                distance = len(self.current_path) - 1
                dist_text = f"Khoang cach: {distance} buoc"
                text = self.font_small.render(dist_text, True, GREEN)
                self.screen.blit(text, (panel_x + 5, y_offset))
                y_offset += 18
        
        # Statistics
        y_offset += 10
        stats_text = self.font_medium.render("📈 THONG KE:", True, WHITE)
        self.screen.blit(stats_text, (panel_x + 5, y_offset))
        y_offset += 22
        
        search_text = f"Tim kiem: {self.total_searches}"
        text = self.font_small.render(search_text, True, WHITE)
        self.screen.blit(text, (panel_x + 5, y_offset))
        y_offset += 18
        
        if self.total_searches > 0:
            avg_dist = self.total_distance / self.total_searches
            avg_text = f"TB khoang cach: {avg_dist:.1f}"
            text = self.font_small.render(avg_text, True, WHITE)
            self.screen.blit(text, (panel_x + 5, y_offset))
        
        # Directions instead of map info
        y_offset += 30
        directions_text = self.font_medium.render("🧭 HUONG DAN DI:", True, WHITE)
        self.screen.blit(directions_text, (panel_x + 5, y_offset))
        y_offset += 22

        if self.current_path and len(self.current_path) > 1:
            directions = self.generate_directions()
            for i, direction in enumerate(directions[:6]):  # Show max 6 steps
                step_text = f"{i+1}. {direction}"
                if len(step_text) > 35:
                    step_text = step_text[:32] + "..."
                
                color = GREEN if i == 0 else WHITE  # Highlight current step
                text = self.font_small.render(step_text, True, color)
                self.screen.blit(text, (panel_x + 5, y_offset))
                y_offset += 16
            
            if len(directions) > 6:
                more_text = f"... va {len(directions) - 6} buoc nua"
                text = self.font_small.render(more_text, True, GRAY)
                self.screen.blit(text, (panel_x + 5, y_offset))
        else:
            no_path_text = "Chon ke hang de xem huong dan"
            text = self.font_small.render(no_path_text, True, GRAY)
            self.screen.blit(text, (panel_x + 5, y_offset))
    
    def draw_title_bar(self):
        """Draw the title bar"""
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, WIDTH - 350, 25))
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH - 350, 25), 2)
        
        title = self.font_medium.render("🤖 FINDBOT - NGON LUA PTIT", True, WHITE)
        title_rect = title.get_rect(center=((WIDTH - 350) // 2, 12))
        self.screen.blit(title, title_rect)
    
    def handle_keyboard_input(self, key):
        """Handle keyboard input for product selection"""
        # Number keys and letter keys for product selection
        category = get_category_by_key(key)
        if category:
            self.selected_category = category
            self.find_path_to_product(category)
            self.sound_manager.play_sound('select')
            return True
        
        # Movement keys
        elif key in ['w', 'up']:
            self.move_user('up')
        elif key in ['s', 'down']:
            self.move_user('down')
        elif key in ['a', 'left']:
            self.move_user('left')
        elif key in ['d', 'right']:
            self.move_user('right')
        
        # Other controls
        elif key == 'm':
            sound_status = self.sound_manager.toggle_sound()
            print(f"Am thanh: {'Bat' if sound_status else 'Tat'}")
        elif key == 'escape':
            self.selected_category = None
            self.current_path = []
            self.path_animation_index = 0
            self.sound_manager.play_sound('error')
        
        return False
    
    def find_path_to_product(self, category):
        """Find path to the nearest accessible point around the shelf"""
        if category not in PRODUCT_CATEGORIES:
            return
        
        info = PRODUCT_CATEGORIES[category]
        product_positions = info['positions']
        
        result = self.pathfinder.find_nearest_shelf_access(self.user_pos, product_positions)
        
        if result:
            target_pos, path, distance = result
            self.current_path = path
            self.path_animation_index = 0
            
            # Update statistics
            self.total_searches += 1
            self.total_distance += distance
            
            self.sound_manager.play_sound('success')
            print(f"Tim thay duong den Ke {info['shelf_id']} - {info['name']} - Khoang cach: {distance:.1f} buoc")
        else:
            self.current_path = []
            self.sound_manager.play_sound('error')
            print(f"Khong tim thay duong den Ke {info['shelf_id']} - {info['name']}")
    
    def generate_directions(self):
        """Generate step-by-step text directions with proper turn detection"""
        if not self.current_path or len(self.current_path) < 2:
            return []
        
        directions = []
        
        # Get direction for each step
        path_directions = []
        for i in range(len(self.current_path) - 1):
            current_pos = self.current_path[i]
            next_pos = self.current_path[i + 1]
            
            dr = next_pos[0] - current_pos[0]
            dc = next_pos[1] - current_pos[1]
            
            if dr == 0 and dc == 1:
                path_directions.append("PHAI")
            elif dr == 0 and dc == -1:
                path_directions.append("TRAI")
            elif dr == 1 and dc == 0:
                path_directions.append("XUONG")
            elif dr == -1 and dc == 0:
                path_directions.append("LEN")
        
        if not path_directions:
            return ["Da den noi!!!"]
        
        # Group consecutive same directions
        i = 0
        while i < len(path_directions):
            current_dir = path_directions[i]
            count = 1
            
            # Count consecutive same directions
            while i + count < len(path_directions) and path_directions[i + count] == current_dir:
                count += 1
            
            # Determine if this is a turn or straight movement
            if i == 0:
                # First movement
                if current_dir == "LEN":
                    directions.append(f"Di thang {count} buoc")
                elif current_dir == "XUONG":
                    directions.append(f"Di thang {count} buoc")
                elif current_dir == "TRAI":
                    directions.append(f"Re trai {count} buoc")
                elif current_dir == "PHAI":
                    directions.append(f"Re phai {count} buoc")
            else:
                # Check if direction changed (turn)
                prev_dir = path_directions[i - 1]
                if current_dir != prev_dir:
                    # This is a turn
                    if current_dir == "TRAI":
                        directions.append(f"Re trai {count} buoc")
                    elif current_dir == "PHAI":
                        directions.append(f"Re phai {count} buoc")
                    elif current_dir == "LEN":
                        directions.append(f"Di len {count} buoc")
                    elif current_dir == "XUONG":
                        directions.append(f"Di xuong {count} buoc")
                else:
                    # Continue in same direction
                    directions.append(f"Di thang {count} buoc")
            
            i += count
        
        directions.append("Da den noi!!!")
        return directions
    
    def move_user(self, direction):
        """Move user in given direction if possible"""
        row, col = self.user_pos
        new_row, new_col = row, col
        
        direction_map = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        
        if direction in direction_map:
            dr, dc = direction_map[direction]
            new_row, new_col = row + dr, col + dc
            self.last_direction = (dc, dr)  # For drawing direction indicator
        
        if self.pathfinder.is_walkable(new_row, new_col):
            self.user_pos = (new_row, new_col)
            self.sound_manager.play_sound('navigate')
            
            # Update path if user moved
            if self.current_path and self.selected_category:
                self.find_path_to_product(self.selected_category)
    
    def update_animations(self, dt):
        """Update animation timers"""
        self.animation_time += dt
        
        # Animate path drawing
        if self.current_path and self.path_animation_index < len(self.current_path):
            self.path_animation_index += dt * 15  # Speed of path animation
    
    def run(self):
        """Main game loop"""
        running = True
        last_time = time.time()
        
        print("🤖 FindBot - NGON LUA PTIT khoi dong!")
        print("Su dung phim so 1-9,0 cho ke 1-10")
        print("Su dung phim Q,W,E,R,T cho ke 11-15")
        print("Su dung phim Y,U,I,O,P cho ke 16-20")
        print("WASD hoac mui ten de di chuyen")
        print("FindBot dang o gan loi vao sieu thi")
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self.handle_keyboard_input(key_name)
            
            # Update animations
            self.update_animations(dt)
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_title_bar()
            self.draw_board()
            self.draw_products()
            self.draw_entrance()
            self.draw_path()
            self.draw_user()
            self.draw_ui_panel()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        print("👋 Cam on ban da su dung FindBot!")
        pygame.quit()

if __name__ == "__main__":
    try:
        findbot = FinalSupermarketFindBot()
        findbot.run()
    except Exception as e:
        print(f"Loi khoi dong FindBot: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
