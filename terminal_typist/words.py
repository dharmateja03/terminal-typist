import random
import os

class WordGenerator:
    def __init__(self):
        self.common_words = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "she", "or", "an", "will",
            "my", "one", "all", "would", "there", "their", "what", "so", "up", "out",
            "if", "about", "who", "get", "which", "go", "me", "when", "make", "can",
            "like", "time", "no", "just", "him", "know", "take", "people", "into", "year",
            "your", "good", "some", "could", "them", "see", "other", "than", "then", "now",
            "look", "only", "come", "its", "over", "think", "also", "back", "after", "use",
            "two", "how", "our", "work", "first", "well", "way", "even", "new", "want",
            "because", "any", "these", "give", "day", "most", "us", "is", "water", "long",
            "find", "here", "thing", "tell", "try", "large", "call", "ask", "turn", "move",
            "live", "point", "small", "every", "right", "much", "spell", "animal", "house", "air",
    "a", "about", "above", "after", "again", "against", "all", "almost", "also", "always",
    "am", "among", "an", "and", "another", "any", "are", "around", "as", "at",
    "back", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "came", "can", "come", "could", "called", "case", "change", "children", "city", "company",
    "day", "did", "different", "do", "does", "done", "down", "during", "each", "early",
    "earth", "east", "end", "enough", "even", "ever", "every", "example", "eye", "face",
    "fact", "family", "far", "father", "feel", "few", "find", "first", "for", "form",
    "found", "four", "friend", "from", "full", "game", "gave", "get", "girl", "give",
    "go", "good", "got", "great", "group", "grow", "had", "half", "hand", "happen",
    "has", "have", "he", "head", "hear", "help", "her", "here", "high", "him",
    "his", "home", "house", "how", "however", "hundred", "I", "idea", "if", "important",
    "in", "interest", "into", "is", "it", "its", "just", "keep", "kind", "knew",
    "know", "land", "large", "last", "later", "learn", "leave", "left", "less", "let",
    "life", "light", "like", "line", "list", "little", "live", "long", "look", "made",
    "make", "man", "many", "may", "me", "mean", "men", "might", "more", "most",
    "mother", "move", "much", "must", "my", "name", "need", "never", "new", "next",
    "night", "no", "not", "nothing", "now", "number", "of", "off", "often", "old",
    "on", "once", "one", "only", "open", "or", "other", "our", "out", "over",
    "own", "part", "people", "place", "play", "point", "put", "question", "quick", "quite",
    "read", "really", "right", "room", "run", "said", "same", "saw", "say", "school",
    "see", "seem", "set", "she", "should", "show", "side", "since", "small", "so",
    "some", "something", "sometimes", "soon", "sound", "still", "such", "sure", "system", "take",
    "tell", "than", "that", "the", "their", "them", "then", "there", "these", "they",
    "thing", "think", "this", "those", "though", "thought", "three", "through", "time", "to",
    "today", "together", "too", "took", "toward", "turn", "two", "under", "until", "up",
    "us", "use", "used", "very", "want", "was", "watch", "way", "we", "well",
    "went", "were", "what", "when", "where", "which", "while", "who", "why", "will",
    "with", "without", "woman", "word", "work", "world", "would", "write", "year", "yes",
    "yet", "you", "young", "your", "able", "act", "add", "age", "air", "animal",
    "answer", "appear", "area", "arrive", "art", "baby", "ball", "bank", "base", "beat",
    "beauty", "bed", "begin", "behind", "believe", "best", "better", "big", "bill", "bit",
    "black", "blue", "board", "body", "book", "bottom", "box", "boy", "break", "bring",
    "broken", "brother", "build", "burn", "buy", "car", "care", "carry", "center", "chance",
    "check", "child", "clear", "cold", "color", "continue", "control", "copy", "corner", "cost",
    "country", "cover", "cross", "cut", "dance", "dark", "deal", "death", "decide", "deep",
    "develop", "die", "direction", "discover", "draw", "dream", "drive", "drop", "dry", "during",
    "Luke", "Leia", "Han", "Chewbacca", "Yoda", "Vader", "ObiWan", "Anakin", "Padme", "Palpatine",
    "Rey", "Kylo", "Finn", "Poe", "Dooku", "Grievous", "Maul", "Ahsoka", "Grogu", "Mando",
    "IronMan", "CaptainAmerica", "Thor", "Hulk", "BlackWidow", "Hawkeye", "SpiderMan", "DoctorStrange", "Loki", "Thanos",
    "Wanda", "Vision", "Falcon", "WinterSoldier", "AntMan", "Wasp", "StarLord", "Gamora", "Drax", "Rocket",
    "Batman", "Superman", "WonderWoman", "Flash", "Aquaman", "Cyborg", "Joker", "HarleyQuinn", "LexLuthor", "Riddler",
    "Catwoman", "Penguin", "Bane", "Shazam", "GreenLantern", "Zod", "Robin", "Batgirl", "TwoFace", "Scarecrow",
    "Harry", "Hermione", "Ron", "Dumbledore", "Voldemort", "Snape", "Hagrid", "Draco", "Sirius", "Luna",
    "Neville", "Bellatrix", "McGonagall", "Newt", "Grindelwald", "Cho", "Cedric", "Tonks", "Moody", "Dobby",
"Frodo", "Sam", "Gandalf", "Aragorn", "Legolas", "Gimli", "Boromir", "Gollum", "Sauron", "Elrond"
]


        
        self.punctuation_words = [
            "hello,", "world!", "test?", "code;", "python:", "fast.", "slow,", "good!",
            "bad?", "nice;", "cool:", "warm.", "cold,", "hot!", "big?", "small;",
        ]
    
    def generate_text(self, duration_seconds):
        """Generate text based on expected typing duration"""
        # Assume average typing speed of 40 WPM
        estimated_words = max(20, int(duration_seconds * 40 / 60))
        return self.generate_text_by_words(estimated_words)
    
    def generate_text_by_words(self, word_count):
        """Generate text with specific word count"""
        words = []
        
        # 90% common words, 10% with punctuation
        for _ in range(word_count):
            if random.random() < 0.9:
                words.append(random.choice(self.common_words))
            else:
                words.append(random.choice(self.punctuation_words))
        
        return " ".join(words)
    
    def get_quote(self):
        """Get a random quote for practice"""
        quotes = [
            "The only way to do great work is to love what you do.",
            "Life is what happens to you while you're busy making other plans.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "It is during our darkest moments that we must focus to see the light.",
            "The only impossible journey is the one you never begin.",
        ]
        return random.choice(quotes)