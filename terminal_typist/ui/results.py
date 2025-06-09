import curses
from .base import BaseUI

class ResultsUI(BaseUI):
    """Results and analytics display interface"""
    
    def show_results(self, stats, comprehensive_stats=None):
        """Display final test results with analytics"""
        while True:
            self.stdscr.clear()
            
            # Title
            title = "[!] TEST RESULTS [!]"
            self.safe_addstr(1, self.center_text(title), title, 
                           curses.color_pair(5) | curses.A_BOLD)
            
            # Current test results
            main_results = [
                f"[=] WPM: {stats['wpm']}",
                f"[*] Accuracy: {stats['accuracy']}%", 
                f"[T] Time: {stats['time_taken']}s",
                f"[>] Chars/Second: {stats['chars_per_second']}",
            ]
            
            start_row = 3
            for i, result in enumerate(main_results):
                color = curses.color_pair(4)
                if "WPM:" in result:
                    color = curses.color_pair(1) | curses.A_BOLD
                elif "Accuracy:" in result:
                    color = curses.color_pair(3) | curses.A_BOLD
                elif "Time:" in result or "Chars/Second:" in result:
                    color = curses.color_pair(2) | curses.A_BOLD
                
                self.safe_addstr(start_row + i, self.center_text(result), 
                               result, color)
            
            # Analytics section
            save_row = start_row + 8
            if comprehensive_stats and comprehensive_stats.get('total_tests', 0) > 0:
                save_row = self._display_analytics_preview(comprehensive_stats, start_row + 5)
            
            # Results saved message
            save_msg = "[S] Results saved to ~/.terminal_typist_results.txt"
            self.safe_addstr(save_row, self.center_text(save_msg), 
                           save_msg, curses.color_pair(3))
            
            # Navigation instructions
            nav_instructions = [
                "Press 'b' to go Back to main menu",
                "Press 'r' to Restart same test",
                "Press 's' to view full Statistics",
                "Press 'q' to Quit"
            ]
            
            instruction_start_row = self.height - 5
            for i, instruction in enumerate(nav_instructions):
                self.safe_addstr(instruction_start_row + i, 
                               self.center_text(instruction), 
                               instruction, curses.color_pair(4))
            
            self.stdscr.refresh()
            
            # Get user input
            key = self.get_key()
            if key == ord('b') or key == ord('B'):
                return 'back'
            elif key == ord('r') or key == ord('R'):
                return 'restart'
            elif key == ord('s') or key == ord('S'):
                if comprehensive_stats:
                    self.show_analytics_screen(comprehensive_stats)
            elif key == ord('q') or key == ord('Q'):
                return 'quit'
    
    def _display_analytics_preview(self, comprehensive_stats, start_row):
        """Display analytics preview in results"""
        analytics_title = "[^] YOUR PERFORMANCE ANALYTICS"
        self.safe_addstr(start_row, self.center_text(analytics_title), 
                       analytics_title, curses.color_pair(5) | curses.A_BOLD)
        
        analytics_data = [
            f"[T] Best WPM: {comprehensive_stats['best_wpm']} | Avg: {comprehensive_stats['avg_wpm']}",
            f"[F] Current Streak: {comprehensive_stats['current_streak']} days | Best: {comprehensive_stats['longest_streak']} days",
            f"[=] Tests Completed: {comprehensive_stats['total_tests']} | This Month: {comprehensive_stats['last_30_days_tests']}",
            f"[^] Trend: {comprehensive_stats['improvement_trend']} | Consistency: {comprehensive_stats['consistency_score']}%"
        ]
        
        for i, data in enumerate(analytics_data):
            self.safe_addstr(start_row + 2 + i, self.center_text(data), 
                           data, curses.color_pair(4))
        
        # Top 3 WPM scores
        if comprehensive_stats['top_5_wpm']:
            top_title = "[1] TOP 3 SPEEDS"
            self.safe_addstr(start_row + 7, self.center_text(top_title), 
                           top_title, curses.color_pair(3) | curses.A_BOLD)
            
            for i, top_score in enumerate(comprehensive_stats['top_5_wpm'][:3]):
                medal = ["[1]", "[2]", "[3]"][i]
                score_text = f"{medal} {top_score['wpm']} WPM ({top_score['accuracy']}%) - {top_score['date']}"
                self.safe_addstr(start_row + 9 + i, self.center_text(score_text), 
                               score_text, curses.color_pair(1))
        
        return start_row + 13
    
    def show_analytics_screen(self, stats):
        """Display comprehensive analytics screen"""
        while True:
            self.stdscr.clear()
            
            if stats.get('total_tests', 0) == 0:
                self._show_no_data_screen()
                return
            
            # Title
            title = "[=] YOUR TYPING STATISTICS & ANALYTICS"
            self.safe_addstr(1, self.center_text(title), title, 
                           curses.color_pair(5) | curses.A_BOLD)
            
            # Create analytics sections
            sections = self._create_analytics_sections(stats)
            
            # Display sections
            current_row = 3
            max_display_rows = self.height - 6
            
            for section in sections:
                for line in section:
                    if current_row >= max_display_rows:
                        break
                    
                    if line.startswith("   "):  # Indented line
                        color = curses.color_pair(4)
                    elif line.endswith(":"):  # Section header
                        color = curses.color_pair(3) | curses.A_BOLD
                    elif line == "":  # Empty line
                        current_row += 1
                        continue
                    else:
                        color = curses.color_pair(4)
                    
                    self.safe_addstr(current_row, self.center_text(line), 
                                   line, color)
                    current_row += 1
                
                if current_row >= max_display_rows:
                    scroll_msg = "... (scroll down for more)"
                    self.safe_addstr(max_display_rows, self.center_text(scroll_msg), 
                                   scroll_msg, curses.color_pair(2))
                    break
            
            # Navigation
            prompt = "Press any key to go back to menu..."
            self.safe_addstr(self.height - 2, self.center_text(prompt), 
                           prompt, curses.color_pair(4))
            
            self.stdscr.refresh()
            self.wait_for_key()
            return
    
    def _show_no_data_screen(self):
        """Show screen when no analytics data is available"""
        title = "[=] STATISTICS & ANALYTICS"
        self.safe_addstr(2, self.center_text(title), title, 
                       curses.color_pair(5) | curses.A_BOLD)
        
        message = "No tests completed yet. Start typing to see your statistics!"
        self.safe_addstr(self.height // 2, self.center_text(message), 
                       message, curses.color_pair(4))
        
        prompt = "Press any key to go back..."
        self.safe_addstr(self.height - 3, self.center_text(prompt), 
                       prompt, curses.color_pair(3))
        
        self.stdscr.refresh()
        self.wait_for_key()
    
    def _create_analytics_sections(self, stats):
        """Create analytics sections for display"""
        sections = []
        
        # Overall Performance
        sections.append([
            "[*] OVERALL PERFORMANCE:",
            f"   Tests Completed: {stats['total_tests']}",
            f"   Total Time: {stats['total_time_spent']:.1f} min",
            f"   Total Characters: {stats['total_chars_typed']:,}",
            ""
        ])
        
        # Speed Statistics
        sections.append([
            "[!] SPEED STATISTICS:",
            f"   Best WPM: {stats['best_wpm']} | Worst: {stats['worst_wpm']}",
            f"   Average WPM: {stats['avg_wpm']} | Median: {stats['median_wpm']}",
            f"   This Week: {stats['this_week_avg']} | This Month: {stats['this_month_avg']}",
            ""
        ])
        
        # Accuracy & Consistency
        sections.append([
            "[*] ACCURACY & CONSISTENCY:",
            f"   Best Accuracy: {stats['best_accuracy']}% | Worst: {stats['worst_accuracy']}%",
            f"   Average Accuracy: {stats['avg_accuracy']}%",
            f"   Consistency Score: {stats['consistency_score']}%",
            ""
        ])
        
        # Streaks & Activity
        sections.append([
            "[F] STREAKS & ACTIVITY:",
            f"   Current Streak: {stats['current_streak']} days",
            f"   Longest Streak: {stats['longest_streak']} days",
            f"   Tests Last 30 Days: {stats['last_30_days_tests']}",
            ""
        ])
        
        # Progress & Insights
        sections.append([
            "[^] PROGRESS & INSIGHTS:",
            f"   Improvement Trend: {stats['improvement_trend']}",
            f"   Best Day: {stats['best_day']}",
            f"   Most Active Day: {stats['most_active_day']}",
            f"   Peak Time: {stats['peak_performance_time']}",
            ""
        ])
        
        # Top 5 WPM Scores
        if stats['top_5_wpm']:
            top_section = ["[T] TOP 5 BEST SPEEDS:"]
            for i, score in enumerate(stats['top_5_wpm']):
                medal = ["[1]", "[2]", "[3]", "[4]", "[5]"][i]
                top_section.append(f"   {medal} {score['wpm']} WPM ({score['accuracy']}%) - {score['date']}")
            top_section.append("")
            sections.append(top_section)
        
        # Test Type Breakdown
        if stats['test_type_stats']:
            breakdown_section = ["[=] TEST TYPE BREAKDOWN:"]
            for test_type, type_stats in stats['test_type_stats'].items():
                breakdown_section.append(f"   {test_type}: {type_stats['count']} tests, {type_stats['avg_wpm']} avg WPM")
            breakdown_section.append("")
            sections.append(breakdown_section)
        
        return sections