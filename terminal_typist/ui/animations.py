import random
import math
import curses

class AnimationManager:
    """Manages background animations for the UI"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.animation_time = 0
        self.floating_chars = self._init_floating_chars()
        self.wave_chars = self._init_wave_chars()
    
    def _init_floating_chars(self):
        """Initialize floating characters for background animation"""
        chars = []
        char_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        # Adjust number of floating chars based on screen size
        if self.width >= 100:
            char_count = 40
        elif self.width >= 80:
            char_count = 30
        elif self.width >= 60:
            char_count = 20
        else:
            char_count = 10
        
        for _ in range(char_count):
            chars.append({
                'char': random.choice(char_set),
                'x': random.randint(0, self.width - 1),
                'y': random.randint(0, self.height - 1),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.3, 0.3),
                'life': random.randint(100, 300),
                'max_life': random.randint(100, 300),
                'color': random.choice([1, 2, 3, 4, 5])
            })
        return chars
    
    def _init_wave_chars(self):
        """Initialize wave pattern characters"""
        chars = []
        wave_chars = ['~', '-', '=', '≡', '∿', '∼']
        
        for i in range(min(15, self.width // 4)):
            chars.append({
                'char': random.choice(wave_chars),
                'base_x': i * 4,
                'base_y': self.height - 3,
                'offset': random.uniform(0, 2 * math.pi),
                'color': random.choice([3, 4, 5])
            })
        return chars
    
    def update(self):
        """Update animation state"""
        self.animation_time += 0.1
        
        # Update floating characters
        for char in self.floating_chars:
            char['x'] += char['dx']
            char['y'] += char['dy']
            char['life'] -= 1
            
            # Wrap around screen
            if char['x'] < 0:
                char['x'] = self.width - 1
            elif char['x'] >= self.width:
                char['x'] = 0
            if char['y'] < 0:
                char['y'] = self.height - 1
            elif char['y'] >= self.height:
                char['y'] = 0
            
            # Respawn if life is over
            if char['life'] <= 0:
                char['char'] = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
                char['x'] = random.randint(0, self.width - 1)
                char['y'] = random.randint(0, self.height - 1)
                char['dx'] = random.uniform(-0.5, 0.5)
                char['dy'] = random.uniform(-0.3, 0.3)
                char['life'] = char['max_life']
                char['color'] = random.choice([1, 2, 3, 4, 5])
    
    def draw(self, stdscr):
        """Draw animated background elements"""
        # Draw floating characters with fading effect
        for char in self.floating_chars:
            try:
                alpha_factor = char['life'] / char['max_life']
                if alpha_factor > 0.3:
                    x, y = int(char['x']), int(char['y'])
                    if 0 <= x < self.width - 1 and 0 <= y < self.height - 1:
                        # Avoid drawing over menu items and top area
                        menu_area_y_start = max(0, 5)
                        menu_area_y_end = min(self.height, self.height // 2 + 12)
                        menu_area_x_start = max(0, self.width // 2 - 25)
                        menu_area_x_end = min(self.width, self.width // 2 + 25)
                        
                        if not (menu_area_y_start <= y <= menu_area_y_end and 
                               menu_area_x_start <= x <= menu_area_x_end):
                            stdscr.addstr(y, x, char['char'], 
                                        curses.color_pair(char['color']) | curses.A_DIM)
            except:
                pass
        
        # Draw wave pattern at bottom
        for char in self.wave_chars:
            try:
                wave_y = int(self.height - 3 + 1 * math.sin(self.animation_time + char['offset']))
                wave_y = max(self.height - 4, min(wave_y, self.height - 1))
                
                if 0 <= char['base_x'] < self.width - 1 and 0 <= wave_y < self.height - 1:
                    stdscr.addstr(wave_y, char['base_x'], char['char'], 
                                curses.color_pair(char['color']))
            except:
                pass
        
        # Draw corner decorations
        try:
            corner_chars = ['[K]', '[PC]', '[!]', '[>]']
            corners = [
                (self.height - 3, 1), (self.height - 3, self.width - 5), 
                (self.height - 2, 1), (self.height - 2, self.width - 5)
            ]
            
            for i, (cy, cx) in enumerate(corners):
                if 0 <= cy < self.height - 1 and 0 <= cx < self.width - 4:
                    stdscr.addstr(cy, cx, corner_chars[i], curses.color_pair(5))
        except:
            pass
    
    def get_wave_offset(self, index):
        """Get wave offset for menu items"""
        return int(2 * math.sin(self.animation_time + index * 0.5))
    
    def get_pulse_intensity(self):
        """Get pulsing intensity for UI elements"""
        return curses.A_BOLD if int(self.animation_time * 4) % 2 == 0 else curses.A_NORMAL
    
    def get_color_cycle(self, index, base_color=4):
        """Get cycling color for menu items"""
        if (int(self.animation_time * 4) + index) % 4 == 0:
            return curses.color_pair(1)
        return curses.color_pair(base_color)
    
    def get_animated_dots(self):
        """Get animated dots for status"""
        return "." * (int(self.animation_time * 2) % 4 + 1)