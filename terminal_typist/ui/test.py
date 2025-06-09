import curses
from .base import BaseUI

class TestUI(BaseUI):
    """Typing test interface"""
    
    def display_test(self, target_text, user_input, cursor_pos, wpm, accuracy, elapsed, duration):
        """Display the main typing test interface"""
        self.stdscr.clear()
        
        # Stats header
        if duration > 0:
            time_left = max(0, duration - elapsed)
            stats = f"Time: {time_left:.0f}s | WPM: {wpm} | Accuracy: {accuracy}%"
        else:
            stats = f"Time: {elapsed:.1f}s | WPM: {wpm} | Accuracy: {accuracy}%"
        
        self.safe_addstr(1, self.center_text(stats), stats, 
                        curses.color_pair(4) | curses.A_BOLD)
        
        # Text display area
        text_start_row = 4
        text_area_height = 10
        text_area_width = min(80, self.width - 4)
        text_start_col = self.center_text("", text_area_width)
        
        # Wrap text for display
        wrapped_lines = self._wrap_text(target_text, text_area_width)
        
        # Display text with color coding
        char_index = 0
        for line_num, line in enumerate(wrapped_lines[:text_area_height]):
            if text_start_row + line_num >= self.height - 4:
                break
                
            row = text_start_row + line_num
            col = text_start_col
            
            for char in line:
                if char_index < len(user_input):
                    # Character has been typed
                    if user_input[char_index] == char:
                        # Correct character
                        self.safe_addstr(row, col, char, curses.color_pair(1))
                    else:
                        # Incorrect character
                        self.safe_addstr(row, col, char, 
                                       curses.color_pair(2) | curses.A_BOLD)
                elif char_index == cursor_pos:
                    # Current cursor position
                    self.safe_addstr(row, col, char, 
                                   curses.color_pair(3) | curses.A_REVERSE)
                else:
                    # Untyped character
                    self.safe_addstr(row, col, char)
                
                char_index += 1
                col += 1
                
                if char_index >= len(target_text):
                    break
            
            if char_index >= len(target_text):
                break
        
        # Instructions
        instructions = "ESC to quit | Backspace to correct"
        self.safe_addstr(self.height - 2, self.center_text(instructions), 
                        instructions, curses.color_pair(4))
        
        self.stdscr.refresh()
    
    def _wrap_text(self, text, width):
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines