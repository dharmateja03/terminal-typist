import curses
import time
from .base import BaseUI
from .animations import AnimationManager

class MenuUI(BaseUI):
    """Main menu interface"""
    
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.animation_manager = AnimationManager(self.width, self.height)
    
    def show_menu(self):
        """Display main menu with animations and return user choice"""
        while True:
            # Update window size in case it changed
            self.height, self.width = self.stdscr.getmaxyx()
            self.animation_manager = AnimationManager(self.width, self.height)
            
            self.stdscr.clear()
            
            # Update and draw animations
            self.animation_manager.update()
            self.animation_manager.draw(self.stdscr)
            
            # Responsive title based on window size
            self._draw_responsive_title()
            
            # Animated border around menu (only for larger screens)
            if self.width > 60 and self.height > 20:
                self._draw_animated_border()
            
            # Menu options with responsive styling
            menu_items = self._get_responsive_menu_items()
            self._draw_menu_items(menu_items)
            
            # Instructions with pulsing effect
            instruction = self._get_responsive_instruction()
            pulse_intensity = self.animation_manager.get_pulse_intensity()
            self.safe_addstr(self.height - 4, self.center_text(instruction), 
                           instruction, curses.color_pair(3) | pulse_intensity)
            
            # Status line with moving dots (only for larger screens)
            if self.height > 15:
                dots = self.animation_manager.get_animated_dots()
                status = f"Ready for typing challenge{dots}"
                self.safe_addstr(self.height - 2, self.center_text(status), 
                               status, curses.color_pair(4) | curses.A_DIM)
            
            self.stdscr.refresh()
            
            # Check for key input
            key = self.get_key()
            if key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('q'), ord('Q')]:
                return chr(key).lower()
            
            # Small delay to control animation speed
            time.sleep(0.05)
    
    def _draw_responsive_title(self):
        """Draw title responsive to window size"""
        if self.width >= 80 and self.height >= 25:
            # Large screen - ASCII art title
            title_lines = [
                "▀█▀ █▀▀ █▀█ █▄█ █ █▄█ █▀█ █   ",
                " █  █▀▀ █▀▄ █▀█ █ █▀█ █▀█ █   ",
                " ▀  ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ",
                "",
                "▀█▀ █ █ █▀█ █ █▀▀ ▀█▀",
                " █  █▄█ █▀▀ █ ▀▀█  █ ",
                " ▀   ▀  ▀   ▀ ▀▀▀  ▀ "
            ]
            start_row = 2
        elif self.width >= 60 and self.height >= 20:
            # Medium screen - simple ASCII
            title_lines = [
                "╔══════════════════════════╗",
                "║    TERMINAL TYPIST       ║",
                "║  Master Your Speed!      ║", 
                "╚══════════════════════════╝"
            ]
            start_row = 3
        else:
            # Small screen - minimal text
            title_lines = [
                ">> TERMINAL TYPIST <<",
                "    Type Fast!    "
            ]
            start_row = 1
        
        for i, line in enumerate(title_lines):
            if start_row + i < self.height - 10:
                self.safe_addstr(start_row + i, self.center_text(line), line, 
                               curses.color_pair(5) | curses.A_BOLD)
    
    def _get_responsive_menu_items(self):
        """Get menu items based on screen size"""
        if self.width >= 70:
            # Large screen - full descriptions
            return [
                "1. [!] Quick Test (30 seconds)",
                "2. [*] Standard Test (60 seconds)", 
                "3. [>>] Long Test (2 minutes)",
                "4. [#] Custom Word Count",
                "5. [=] View Statistics & Analytics",
                "6. [DEV] Developer Details",
                "q. [X] Quit"
            ]
        elif self.width >= 50:
            # Medium screen - shorter descriptions
            return [
                "1. [!] Quick (30s)",
                "2. [*] Standard (60s)", 
                "3. [>>] Long (2m)",
                "4. [#] Custom Words",
                "5. [=] Statistics",
                "6. [DEV] Developer",
                "q. [X] Quit"
            ]
        else:
            # Small screen - minimal
            return [
                "1. Quick",
                "2. Standard", 
                "3. Long",
                "4. Custom",
                "5. Stats",
                "6. Dev",
                "q. Quit"
            ]
    
    def _get_responsive_instruction(self):
        """Get instruction text based on screen size"""
        if self.width >= 60:
            return "[*] Press a key to select an option [*]"
        elif self.width >= 40:
            return "Press a key to select"
        else:
            return "Select option"
    
    def _draw_animated_border(self):
        """Draw animated border around menu"""
        try:
            border_chars = ['│', '║', '┃']
            border_char = border_chars[int(self.animation_manager.animation_time * 3) % 3]
            menu_width = 35
            menu_start_x = (self.width - menu_width) // 2
            menu_start_y = 10
            menu_height = 14
            
            # Draw animated side borders
            for y in range(menu_start_y, menu_start_y + menu_height):
                if 0 <= y < self.height - 1:
                    # Left border
                    if menu_start_x - 2 >= 0:
                        self.stdscr.addstr(y, menu_start_x - 2, border_char, 
                                         curses.color_pair(4))
                    # Right border  
                    if menu_start_x + menu_width + 1 < self.width:
                        self.stdscr.addstr(y, menu_start_x + menu_width + 1, border_char, 
                                         curses.color_pair(4))
        except:
            pass
    
    def _draw_menu_items(self, menu_items):
        """Draw menu items with animation effects"""
        # Calculate start row based on window size
        if self.height >= 25:
            start_row = 12
        elif self.height >= 20:
            start_row = 8
        else:
            start_row = 4
        
        # Adjust spacing based on screen height
        spacing = 2 if self.height >= 20 else 1
        
        for i, item in enumerate(menu_items):
            # Skip items that won't fit
            if start_row + i * spacing >= self.height - 4:
                break
            
            # Add animation only for larger screens
            if self.width > 50:
                wave_offset = self.animation_manager.get_wave_offset(i)
                item_x = self.center_text(item) + wave_offset
                item_x = max(0, min(item_x, self.width - len(item) - 1))
            else:
                item_x = self.center_text(item)
            
            # Color effects
            if i < 4:  # Test options
                color = self.animation_manager.get_color_cycle(i) if self.width > 50 else curses.color_pair(1)
            elif i == 4:  # Statistics
                color = curses.color_pair(3)
            elif i == 5:  # Developer Details
                color = curses.color_pair(5)
            else:  # Quit
                color = curses.color_pair(2)
            
            self.safe_addstr(start_row + i * spacing, item_x, item, color)
    
    def get_word_count(self):
        """Get custom word count from user"""
        self.stdscr.clear()
        prompt = "Enter number of words (10-200): "
        self.safe_addstr(self.height // 2, self.center_text(prompt), prompt)
        
        curses.echo()
        curses.curs_set(1)
        
        try:
            input_str = self.stdscr.getstr(self.height // 2, 
                                         self.center_text(prompt) + len(prompt), 
                                         10).decode('utf-8')
            word_count = int(input_str)
            if 10 <= word_count <= 200:
                return word_count
        except (ValueError, KeyboardInterrupt):
            pass
        finally:
            curses.noecho()
            curses.curs_set(0)
        
        return None
    
    def show_developer_details(self):
        """Display developer details with ASCII art"""
        while True:
            self.stdscr.clear()
            
            # Developer ASCII Art
            dev_art = [
                "██████╗ ███████╗██╗   ██╗███████╗██╗      ██████╗ ██████╗ ███████╗██████╗ ",
                "██╔══██╗██╔════╝██║   ██║██╔════╝██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗",
                "██║  ██║█████╗  ██║   ██║█████╗  ██║     ██║   ██║██████╔╝█████╗  ██████╔╝",
                "██║  ██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║     ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗",
                "██████╔╝███████╗ ╚████╔╝ ███████╗███████╗╚██████╔╝██║     ███████╗██║  ██║",
                "╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝",
                "",
                "██████╗ ███████╗████████╗ █████╗ ██╗██╗     ███████╗",
                "██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     ██╔════╝",
                "██║  ██║█████╗     ██║   ███████║██║██║     ███████╗",
                "██║  ██║██╔══╝     ██║   ██╔══██║██║██║     ╚════██║",
                "██████╔╝███████╗   ██║   ██║  ██║██║███████╗███████║",
                "╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝"
            ]
            
            # Display ASCII art (smaller version if screen is too small)
            start_row = 2
            if self.height < 25:  # Use smaller version for small screens
                dev_art = [
                    "╔═══════════════════════════════════╗",
                    "║         DEVELOPER DETAILS         ║",
                    "╚═══════════════════════════════════╝"
                ]
            
            for i, line in enumerate(dev_art):
                if start_row + i < self.height - 10:
                    self.safe_addstr(start_row + i, self.center_text(line), line, 
                                   curses.color_pair(5) | curses.A_BOLD)
            
            # Developer Information
            info_start = start_row + len(dev_art) + 2
            dev_info = [
                "[>] Created by: Dharma Teja",
                "[KB] GitHub: github.com/dharmteja03/terminal-typist", 
                "[*] Version: 1.0.0",
                "[!] Built with: Python + Curses",
                "[=] Features: Real-time WPM tracking, Analytics, Animations",
                "",
                "[F] Special Thanks:",
                "   - MonkeyType for inspiration",
                "   - Python Curses library",
                "   - Open source community",
                "",
                "",
                "╔══════════════════════════════════════════════════╗",
                "║  Thanks for using Terminal Typist! Happy typing! ║",
                "╚══════════════════════════════════════════════════╝"
            ]
            
            for i, info in enumerate(dev_info):
                if info_start + i < self.height - 3:
                    color = curses.color_pair(4)
                    if info.startswith("[>]") or info.startswith("[KB]"):
                        color = curses.color_pair(1) | curses.A_BOLD
                    elif info.startswith("[*]") or info.startswith("[!]"):
                        color = curses.color_pair(3) | curses.A_BOLD
                    elif info.startswith("╔") or info.startswith("╚") or info.startswith("║"):
                        color = curses.color_pair(2) | curses.A_BOLD
                    elif info.startswith("[F]") or info.startswith("[T]"):
                        color = curses.color_pair(5) | curses.A_BOLD
                    
                    self.safe_addstr(info_start + i, self.center_text(info), info, color)
            
            # Navigation
            nav_text = "Press any key to return to main menu..."
            self.safe_addstr(self.height - 2, self.center_text(nav_text), 
                           nav_text, curses.color_pair(3) | self.animation_manager.get_pulse_intensity())
            
            self.stdscr.refresh()
            
            # Wait for any key
            key = self.get_key()
            if key != -1:
                break
            
            time.sleep(0.05)