import unittest
from terminal_typist.stats import StatsCalculator
from terminal_typist.words import WordGenerator

class TestBasicFunctionality(unittest.TestCase):
    
    def setUp(self):
        self.stats = StatsCalculator()
        self.words = WordGenerator()
    
    def test_accuracy_calculation(self):
        """Test accuracy calculation"""
        user_input = "hello world"
        target_text = "hello world"
        accuracy = self.stats._calculate_accuracy(user_input, target_text)
        self.assertEqual(accuracy, 100.0)
        
        user_input = "hello wrold"
        target_text = "hello world"
        accuracy = self.stats._calculate_accuracy(user_input, target_text)
        self.assertLess(accuracy, 100.0)
    
    def test_word_generation(self):
        """Test word generation"""
        text = self.words.generate_text_by_words(10)
        words = text.split()
        self.assertEqual(len(words), 10)
        
        text = self.words.generate_text(60)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
    
    def test_live_stats(self):
        """Test live statistics calculation"""
        user_input = "hello"
        target_text = "hello world"
        elapsed = 30.0
        
        wpm, accuracy = self.stats.calculate_live_stats(user_input, target_text, elapsed)
        self.assertIsInstance(wpm, int)
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0)
        self.assertLessEqual(accuracy, 100)

if __name__ == '__main__':
    unittest.main()