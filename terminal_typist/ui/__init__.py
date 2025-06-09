"""
Terminal Typist UI Module

Modular UI components for the terminal typing test application.
"""

from .base import BaseUI
from .animations import AnimationManager
from .menu import MenuUI
from .test import TestUI
from .results import ResultsUI

# Main UI class that combines all components
class GameUI:
    """Main UI class that orchestrates all UI components"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu_ui = MenuUI(stdscr)
        self.test_ui = TestUI(stdscr)
        self.results_ui = ResultsUI(stdscr)
    
    def show_menu(self):
        """Display main menu"""
        return self.menu_ui.show_menu()
    
    def get_word_count(self):
        """Get custom word count from user"""
        return self.menu_ui.get_word_count()
    
    def display_test(self, target_text, user_input, cursor_pos, wpm, accuracy, elapsed, duration):
        """Display typing test interface"""
        return self.test_ui.display_test(target_text, user_input, cursor_pos, wpm, accuracy, elapsed, duration)
    
    def show_results(self, stats, comprehensive_stats=None):
        """Display test results"""
        return self.results_ui.show_results(stats, comprehensive_stats)
    
    def show_analytics_screen(self, stats):
        """Display analytics screen"""
        return self.results_ui.show_analytics_screen(stats)
    
    def get_key(self):
        """Get key input"""
        return self.stdscr.getch()
    def show_developer_details(self):
        """Display developer details"""
        return self.menu_ui.show_developer_details()

__all__ = ['GameUI', 'BaseUI', 'AnimationManager', 'MenuUI', 'TestUI', 'ResultsUI']