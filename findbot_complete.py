import pygame
import math
import time
from supermarket_board import supermarket_layout, PRODUCT_CATEGORIES, get_category_by_key
from enhanced_pathfinding import EnhancedPathFinder
from sound_manager import SoundManager
from tts_manager import TTSManager

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1000
HEIGHT = 800
CELL_SIZE = 25
FPS = 60

# Colors
BLACK = (0, 0, 0)
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

class SupermarketFindBot:
    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("🤖 FindBot - NGON LUA PTIT")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 48)
        
        # Core systems
        self.layout = supermarket_layout
        self.pathfinder = EnhancedPathFinder(self.layout)
        self.sound_manager = SoundManager()
        self.tts = TTSManager()
        
        # Game state
        self.user_pos = (13, 15)  # Starting position near entrance
        self.target_product = None
        self.current_path = []
        self.path_index = 0
        self.selected_category = None
        
        # UI state
        self.show_help = True
        self.show_history = False
        self.animation_time = 0
        self.path_animation_index = 0
        
        # Statistics
        self.total_searches = 0
        self.total_distance = 0
        
    def draw_board(self):
        """Draw the supermarket layout with enhanced graphics"""
        board_width = WIDTH - 200  # Leave space for UI panel
        board_height = HEIGHT - 100
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                x = j * cell_width
                y = i * cell_height + 50  # Offset for title
                cell = self.layout[i][j]
                
                # Draw cell background
                if cell == 0:  # Walkway
                    pygame.draw.rect(self.screen, WHITE, (x, y, cell_width, cell_height))
                elif cell == 1:  # Product shelf
                    pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, cell_width, cell_height))
                elif cell == 2:  # Special product
                    pygame.draw.rect(self.screen, PURPLE, (x, y, cell_width, cell_height))
                elif cell == 9:  # Entrance/Exit
                    pygame.draw.rect(self.screen, GREEN, (x, y, cell_width, cell_height))
                elif cell >= 3:  # Walls
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, cell_width, cell_height))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, GRAY, (x, y, cell_width, cell_height), 1)
    
    def draw_products(self):
        """Draw product categories with enhanced visuals"""
        board_width = WIDTH - 200
        board_height = HEIGHT - 100
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        for category, info in PRODUCT_CATEGORIES.items():
            color = info['color']
            positions = info['positions']
            
            for i, (row, col) in enumerate(positions):
                if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
                    x = col * cell_width
                    y = row * cell_height + 50
                    
                    # Draw product area with gradient effect
                    pygame.draw.rect(self.screen, color, (x + 2, y + 2, cell_width - 4, cell_height - 4))
                    
                    # Add shine effect
                    shine_color = tuple(min(255, c + 50) for c in color)
                    pygame.draw.rect(self.screen, shine_color, (x + 2, y + 2, cell_width - 4, 3))
                    
                    # Draw category label on first item
                    if i == 0:
                        text = self.font_small.render(f"{info['key']}.{category[:4]}", True, WHITE)
                        text_rect = text.get_rect()
                        
                        # Add text background
                        bg_rect = pygame.Rect(x + 2, y + 2, text_rect.width + 4, text_rect.height + 2)
                        pygame.draw.rect(self.screen, BLACK, bg_rect)
                        pygame.draw.rect(self.screen, WHITE, bg_rect, 1)
                        
                        self.screen.blit(text, (x + 4, y + 3))
    
    def draw_user(self):
        """Draw user with enhanced animation"""
        board_width = WIDTH - 200
        board_height = HEIGHT - 100
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        x = self.user_pos[1] * cell_width + cell_width // 2
        y = self.user_pos[0] * cell_height + cell_height // 2 + 50
        
        # Animated user icon
        pulse = math.sin(self.animation_time * 5) * 2
        radius = 8 + pulse
        
        # Draw shadow
        pygame.draw.circle(self.screen, DARK_GRAY, (x + 2, y + 2), int(radius))
        
        # Draw user
        pygame.draw.circle(self.screen, RED, (x, y), int(radius))
        pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 2)
        
        # Draw direction indicator
        if hasattr(self, 'last_direction'):
            dx, dy = self.last_direction
            end_x = x + dx * 15
            end_y = y + dy * 15
            pygame.draw.line(self.screen, WHITE, (x, y), (end_x, end_y), 3)
    
    def draw_path(self):
        """Draw path with enhanced animation"""
        if not self.current_path:
            return
        
        board_width = WIDTH - 200
        board_height = HEIGHT - 100
        
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        # Animate path drawing
        visible_path_length = min(len(self.current_path), int(self.path_animation_index))
        
        # Draw path segments
        points = []
        for i in range(visible_path_length):
            row, col = self.current_path[i]
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2 + 50
            points.append((x, y))
        
        # Draw path line with gradient
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Color gradient from yellow to green
                progress = i / (len(points) - 1)
                r = int(255 * (1 - progress))
                g = 255
                b = 0
                color = (r, g, b)
                
                pygame.draw.line(self.screen, color, points[i], points[i + 1], 4)
        
        # Draw path dots
        for i, point in enumerate(points):
            if i < visible_path_length - 1:
                pulse = math.sin(self.animation_time * 3 + i * 0.5) * 2
                radius = 4 + pulse
                pygame.draw.circle(self.screen, YELLOW, point, int(radius))
        
        # Draw target with special effect
        if self.current_path and visible_path_length == len(self.current_path):
            target_row, target_col = self.current_path[-1]
            x = target_col * cell_width + cell_width // 2
            y = target_row * cell_height + cell_height // 2 + 50
            
            # Pulsing target
            pulse = math.sin(self.animation_time * 4) * 4
            radius = 12 + pulse
            
            pygame.draw.circle(self.screen, GREEN, (x, y), int(radius))
            pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 3)
            
            # Target crosshair
            pygame.draw.line(self.screen, WHITE, (x - 8, y), (x + 8, y), 2)
            pygame.draw.line(self.screen, WHITE, (x, y - 8), (x, y + 8), 2)
    
    def draw_ui_panel(self):
        """Draw the UI panel with controls and information"""
        panel_x = WIDTH - 190
        panel_width = 180
        
        # Panel background
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, 0, panel_width, HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (panel_x, 0, panel_width, HEIGHT), 2)
        
        y_offset = 10
        
        # Title
        title = self.font_large.render("FindBot", True, WHITE)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 40
        
        # Instructions
        instructions = [
            "🎮 DIEU KHIEN:",
            "So 1-8: Chon ke hang",
            "WASD/Mui ten: Di chuyen",
            "H: An/hien huong dan",
            "R: Lich su tim kiem",
            "M: Bat/tat am thanh",
            "ESC: Huy tim kiem",
            "",
            "📍 KE HANG:"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(text, (panel_x + 5, y_offset))
            y_offset += 20
        
        # Product categories
        for category, info in PRODUCT_CATEGORIES.items():
            color = info['color']
            key = info['key']
            name = info['name']
            
            # Color indicator
            pygame.draw.rect(self.screen, color, (panel_x + 5, y_offset, 15, 15))
            pygame.draw.rect(self.screen, WHITE, (panel_x + 5, y_offset, 15, 15), 1)
            
            # Category text
            text = f"{key}. {name}"
            if len(text) > 20:
                text = text[:17] + "..."
            
            color_to_use = WHITE
            if self.selected_category == category:
                color_to_use = YELLOW
            
            category_text = self.font_small.render(text, True, color_to_use)
            self.screen.blit(category_text, (panel_x + 25, y_offset))
            y_offset += 20
        
        # Current status
        y_offset += 10
        status_text = self.font_medium.render("📊 TRANG THAI:", True, WHITE)
        self.screen.blit(status_text, (panel_x + 5, y_offset))
        y_offset += 25
        
        if self.selected_category:
            info = PRODUCT_CATEGORIES[self.selected_category]
            status = f"Dich: {info['name']}"
            if len(status) > 22:
                status = status[:19] + "..."
            
            text = self.font_small.render(status, True, YELLOW)
            self.screen.blit(text, (panel_x + 5, y_offset))
            y_offset += 20
            
            if self.current_path:
                distance = len(self.current_path) - 1
                dist_text = f"Khoang cach: {distance} buoc"
                text = self.font_small.render(dist_text, True, GREEN)
                self.screen.blit(text, (panel_x + 5, y_offset))
                y_offset += 20
        
        # Statistics
        y_offset += 10
        stats_text = self.font_medium.render("📈 THONG KE:", True, WHITE)
        self.screen.blit(stats_text, (panel_x + 5, y_offset))
        y_offset += 25
        
        search_text = f"Tim kiem: {self.total_searches}"
        text = self.font_small.render(search_text, True, WHITE)
        self.screen.blit(text, (panel_x + 5, y_offset))
        y_offset += 20
        
        if self.total_searches > 0:
            avg_dist = self.total_distance / self.total_searches
            avg_text = f"TB khoang cach: {avg_dist:.1f}"
            text = self.font_small.render(avg_text, True, WHITE)
            self.screen.blit(text, (panel_x + 5, y_offset))
    
    def draw_title_bar(self):
        """Draw the title bar"""
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, WIDTH - 200, 50))
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH - 200, 50), 2)

        title = self.font_title.render("🏪 Sieu thi FindBot - He thong dinh vi thong minh", True, WHITE)
        title_rect = title.get_rect(center=((WIDTH - 200) // 2, 25))
        self.screen.blit(title, title_rect)
    
    def handle_keyboard_input(self, key):
        """Handle keyboard input for product selection"""
        # Number keys for product selection
        if key in ['1', '2', '3', '4', '5', '6', '7', '8']:
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
        elif key == 'h':
            self.show_help = not self.show_help
        elif key == 'r':
            self.show_history = not self.show_history
        elif key == 'm':
            sound_status = self.sound_manager.toggle_sound()
            print(f"Am thanh: {'BBat' if sound_status else 'TTat'}")
        elif key == 'escape':
            self.selected_category = None
            self.current_path = []
            self.path_animation_index = 0
            self.sound_manager.play_sound('error')
        
        return False
    
    def find_path_to_product(self, category):
        """Find path to the nearest product of given category"""
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
            print(f"Tim thay duong den {info['name']} - Khoang cach: {distance:.1f} buoc")
            self.tts.speak(f"Đã tìm thấy đường đến {info['name']} - Khoảng cách: {distance:.1f} bước")
        else:
            self.current_path = []
            self.sound_manager.play_sound('error')
            print(f"Khong tim thay duong den {info['name']}")

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
            self.path_animation_index += dt * 10  # Speed of path animation
    
    def run(self):
        """Main game loop"""
        running = True
        last_time = time.time()
        
        print("🤖 FindBot khoi dong!")
        print("Su dung phim so 1-8 de chon ke hang can tim")
        print("WASD hoac mui ten de di chuyen")

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
            self.screen.fill(BLACK)
            self.draw_title_bar()
            self.draw_board()
            self.draw_products()
            self.draw_path()
            self.draw_user()
            self.draw_ui_panel()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        print("👋 Cảm ơn bạn đã sử dụng FindBot!")
        pygame.quit()

if __name__ == "__main__":
    try:
        findbot = SupermarketFindBot()
        findbot.run()
    except Exception as e:
        print(f"Lỗi khởi động FindBot: {e}")
        pygame.quit()
