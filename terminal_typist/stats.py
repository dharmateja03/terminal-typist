import time
from collections import defaultdict

class StatsCalculator:
    def __init__(self):
        self.error_count = 0
        self.correct_chars = 0
        self.total_chars = 0
        
    def calculate_live_stats(self, user_input, target_text, elapsed_time):
        """Calculate WPM and accuracy in real-time"""
        if elapsed_time <= 0:
            return 0, 100
        
        # Calculate WPM (words per minute)
        chars_typed = len(user_input)
        wpm = (chars_typed / 5) / (elapsed_time / 60)  # Standard: 5 chars = 1 word
        
        # Calculate accuracy
        accuracy = self._calculate_accuracy(user_input, target_text)
        
        return round(wpm), round(accuracy, 1)
    
    def calculate_final_stats(self, user_input, target_text, elapsed_time):
        """Calculate final comprehensive statistics"""
        if elapsed_time <= 0:
            return {}
        
        # Basic metrics
        chars_typed = len(user_input)
        wpm = (chars_typed / 5) / (elapsed_time / 60)
        accuracy = self._calculate_accuracy(user_input, target_text)
        
        # Character analysis
        correct_chars = 0
        incorrect_chars = 0
        
        for i, char in enumerate(user_input):
            if i < len(target_text):
                if char == target_text[i]:
                    correct_chars += 1
                else:
                    incorrect_chars += 1
        
        # Error rate
        error_rate = (incorrect_chars / max(1, chars_typed)) * 100
        
        # Consistency (simplified)
        consistency = max(0, 100 - error_rate)
        
        return {
            'wpm': round(wpm),
            'accuracy': round(accuracy, 1),
            'chars_typed': chars_typed,
            'correct_chars': correct_chars,
            'incorrect_chars': incorrect_chars,
            'error_rate': round(error_rate, 1),
            'consistency': round(consistency, 1),
            'time_taken': round(elapsed_time, 1),
            'chars_per_second': round(chars_typed / elapsed_time, 1)
        }
    
    def _calculate_accuracy(self, user_input, target_text):
        """Calculate typing accuracy percentage"""
        if not user_input:
            return 100
        
        correct = 0
        total = len(user_input)
        
        for i, char in enumerate(user_input):
            if i < len(target_text) and char == target_text[i]:
                correct += 1
        
        return (correct / total) * 100 if total > 0 else 100