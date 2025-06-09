import curses
import time
import random
import os
import json
from datetime import datetime
from .words import WordGenerator
from .stats import StatsCalculator
from .ui import GameUI
from .analytics import StatsAnalyzer

class TypingGame:
    def __init__(self):
        self.word_generator = WordGenerator()
        self.stats = StatsCalculator()
        self.analytics = StatsAnalyzer()
        self.ui = None
        self.current_text = ""
        self.user_input = ""
        self.start_time = None
        self.test_duration = 60  # seconds
        self.is_running = False
        self.cursor_pos = 0
        self.results_file = os.path.expanduser("~/.terminal_typist_results.txt")
        
    def run(self):
        """Main game loop"""
        curses.wrapper(self._game_loop)
    
    def _game_loop(self, stdscr):
        """Curses game loop"""
        self.ui = GameUI(stdscr)
        
        while True:
            choice = self.ui.show_menu()
            
            if choice == 'q':
                break
            elif choice == '1':
                self._start_test_with_restart_option(30)
            elif choice == '2':
                self._start_test_with_restart_option(60)
            elif choice == '3':
                self._start_test_with_restart_option(120)
            elif choice == '4':
                self._start_custom_test_with_restart_option()
            elif choice == '5':
                self._show_analytics()
            elif choice == '6':
                self._show_developer_details()
    
    def _start_test_with_restart_option(self, duration):
        """Start test with restart functionality"""
        while True:
            self._start_test(duration)
            
            if self.start_time:  # Test was completed
                elapsed = time.time() - self.start_time
                final_stats = self.stats.calculate_final_stats(
                    self.user_input, self.current_text, elapsed
                )
                
                # Save results to file
                self._save_results(final_stats)
                
                # Save detailed analytics
                test_type = f"{self.test_duration}s" if self.test_duration > 0 else "Custom"
                self.analytics.save_detailed_result(final_stats, test_type)
                
                # Get comprehensive stats for display
                comprehensive_stats = self.analytics.get_comprehensive_stats()
                
                # Show results and get user choice
                result_choice = self.ui.show_results(final_stats, comprehensive_stats)
                
                if result_choice == 'back':
                    break  # Go back to main menu
                elif result_choice == 'restart':
                    continue  # Restart same test
                elif result_choice == 'quit':
                    self.is_running = False
                    return
            else:
                break  # User pressed ESC, go back to menu
    
    def _start_custom_test_with_restart_option(self):
        """Start custom test with restart functionality"""
        word_count = self.ui.get_word_count()
        if not word_count:
            return
            
        while True:
            self._start_custom_test_direct(word_count)
            
            if self.start_time:  # Test was completed
                elapsed = time.time() - self.start_time
                final_stats = self.stats.calculate_final_stats(
                    self.user_input, self.current_text, elapsed
                )
                
                # Save results to file
                self._save_results(final_stats)
                
                # Save detailed analytics
                test_type = "Custom"
                self.analytics.save_detailed_result(final_stats, test_type)
                
                # Get comprehensive stats for display
                comprehensive_stats = self.analytics.get_comprehensive_stats()
                
                # Show results and get user choice
                result_choice = self.ui.show_results(final_stats, comprehensive_stats)
                
                if result_choice == 'back':
                    break  # Go back to main menu
                elif result_choice == 'restart':
                    continue  # Restart same test
                elif result_choice == 'quit':
                    self.is_running = False
                    return
            else:
                break  # User pressed ESC, go back to menu
    
    def _start_custom_test_direct(self, word_count):
        """Start custom test directly with given word count"""
        self.test_duration = 0  # No time limit for custom tests
        self.current_text = self.word_generator.generate_text_by_words(word_count)
        self.user_input = ""
        self.cursor_pos = 0
        self.start_time = None
        self.is_running = True
        self._run_test()
    
    def _start_test(self, duration):
        """Start typing test with given duration"""
        self.test_duration = duration
        # Start with initial text, will add more as needed
        self.current_text = self.word_generator.generate_text(30)  # Start with 30s worth
        self.user_input = ""
        self.cursor_pos = 0
        self.start_time = None
        self.is_running = True
        
        self._run_test()
    
    def _start_custom_test(self):
        """Start custom word count test"""
        word_count = self.ui.get_word_count()
        if word_count:
            self.current_text = self.word_generator.generate_text_by_words(word_count)
            self.user_input = ""
            self.cursor_pos = 0
            self.start_time = None
            self.is_running = True
            self._run_test()
    
    def _run_test(self):
        """Run the actual typing test"""
        while self.is_running:
            # Calculate elapsed time
            elapsed = 0
            if self.start_time:
                elapsed = time.time() - self.start_time
            
            # Check if time is up (for timed tests)
            if self.test_duration > 0 and elapsed >= self.test_duration:
                self._end_test()
                break
            
            # Add more text if user is getting close to the end (for timed tests)
            if (self.test_duration > 0 and 
                self.cursor_pos > len(self.current_text) - 50 and 
                elapsed < self.test_duration):
                additional_text = self.word_generator.generate_text(30)
                self.current_text += " " + additional_text
            
            # Update UI
            wpm, accuracy = self.stats.calculate_live_stats(
                self.user_input, self.current_text, elapsed
            )
            
            self.ui.display_test(
                self.current_text,
                self.user_input,
                self.cursor_pos,
                wpm,
                accuracy,
                elapsed,
                self.test_duration
            )
            
            # Handle input
            key = self.ui.get_key()
            
            if key == 27:  # ESC
                self.is_running = False
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                if self.user_input:
                    self.user_input = self.user_input[:-1]
                    self.cursor_pos = max(0, self.cursor_pos - 1)
            elif 32 <= key <= 126:  # Printable characters
                if not self.start_time:
                    self.start_time = time.time()
                
                char = chr(key)
                if self.cursor_pos < len(self.current_text):
                    self.user_input += char
                    self.cursor_pos += 1
                
                # For word count tests, check if test is complete
                if (self.test_duration == 0 and 
                    len(self.user_input) >= len(self.current_text)):
                    self._end_test()
                    break
    
    def _end_test(self):
        """End the test - results handling moved to game loop"""
        self.is_running = False
    
    def _save_results(self, stats):
        """Save test results to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            test_type = f"{self.test_duration}s" if self.test_duration > 0 else "Custom"
            
            result_line = (
                f"{timestamp} | {test_type} | "
                f"WPM: {stats['wpm']} | "
                f"Accuracy: {stats['accuracy']}% | "
                f"Chars: {stats['chars_typed']} | "
                f"Time: {stats['time_taken']}s\n"
            )
            
            # Create file with header if it doesn't exist
            if not os.path.exists(self.results_file):
                with open(self.results_file, 'w') as f:
                    f.write("=== TERMINAL TYPIST RESULTS ===\n")
                    f.write("Date & Time | Test Type | WPM | Accuracy | Characters | Time\n")
                    f.write("-" * 70 + "\n")
            
            # Append result
            with open(self.results_file, 'a') as f:
                f.write(result_line)
                
        except Exception as e:
            # Silently fail if can't save results
            pass
    
    def _show_analytics(self):
        """Show comprehensive analytics screen"""
        comprehensive_stats = self.analytics.get_comprehensive_stats()
        self.ui.show_analytics_screen(comprehensive_stats)
    
    def _show_developer_details(self):
        """Show developer details screen"""
        self.ui.show_developer_details()