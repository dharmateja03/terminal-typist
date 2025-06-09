import curses

class BaseUI:
    """Base UI class with common functionality"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self._init_colors()
        self._init_cursor()
    
    def _init_colors(self):
        """Initialize color pairs"""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Correct
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Incorrect
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Cursor
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # UI elements
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Highlights
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Animation
    
    def _init_cursor(self):
        """Initialize cursor and input settings"""
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(50)
    
    def safe_addstr(self, y, x, text, attr=None):
        """Safely add string with emoji fallbacks"""
        try:
            if attr:
                self.stdscr.addstr(y, x, text, attr)
            else:
                self.stdscr.addstr(y, x, text)
        except:
            # Fallback without emojis
            safe_text = self._replace_emojis(text)
            try:
                if attr:
                    self.stdscr.addstr(y, x, safe_text, attr)
                else:
                    self.stdscr.addstr(y, x, safe_text)
            except:
                pass  # Ignore if still fails
    
    def _replace_emojis(self, text):
        """Replace emojis with ASCII alternatives"""
        emoji_replacements = {
            '🚀': '[>]', '⌨️': '[KB]', '🎯': '[*]', '⚡': '[!]', '🏃': '[>>]',
            '📝': '[#]', '📊': '[=]', '🚪': '[X]', '✨': '[*]', '🎉': '[!]',
            '📈': '[^]', '🏆': '[T]', '🔥': '[F]', '🥇': '[1]', '🥈': '[2]',
            '🥉': '[3]', '4️⃣': '[4]', '5️⃣': '[5]', '💾': '[S]', '⏱️': '[T]'
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        return text
    
    def center_text(self, text, width=None):
        """Calculate centered position for text"""
        if width is None:
            width = self.width
        return (width - len(text)) // 2
    
    def clear_and_refresh(self):
        """Clear screen and refresh"""
        self.stdscr.clear()
        self.stdscr.refresh()
    
    def get_key(self):
        """Get key input with timeout"""
        return self.stdscr.getch()
    
    def wait_for_key(self):
        """Wait for any key press"""
        while True:
            key = self.stdscr.getch()
            if key != -1:
                break