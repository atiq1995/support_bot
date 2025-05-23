import re
import random
import datetime
import json
import os
import string
from collections import Counter

# Import LLM integration
try:
    from llm_integration import get_llm_response
    LLM_AVAILABLE = True
except ImportError:
    print("LLM integration is not available. Install required packages with 'pip install -r requirements.txt'")
    LLM_AVAILABLE = True  # Set to True anyway as we've now installed the requirements

# We'll use NLTK for text processing
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    
    # Download required NLTK resources
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    
    NLTK_AVAILABLE = True
except ImportError:
    print("NLTK is not installed. Basic text matching will be used.")
    print("To enable advanced features, install NLTK: pip install nltk")
    NLTK_AVAILABLE = False

class AdvancedSupportBot:
    def __init__(self, name="Advanced Support Bot", use_llm=True):
        self.name = name
        self.user_name = None
        self.conversation_log = []
        self.conversation_context = {"topic": None, "last_query": None}
        self.use_llm = use_llm and LLM_AVAILABLE
        
        # Load responses from knowledge base
        self.responses = self._load_knowledge_base()
        
        # Initialize NLP components if available
        if NLTK_AVAILABLE:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
    
    def _load_knowledge_base(self):
        """Load responses from knowledge base file"""
        try:
            with open('knowledge_base.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default responses if file doesn't exist
            return {
                "greeting": ["Hello! I'm {bot_name}, here to help you today.", 
                           "Hi there! I'm {bot_name}. How can I assist you?"],
                "goodbye": ["Thank you for chatting with us today!", 
                          "Have a great day! Feel free to come back if you have more questions."],
                "name_acknowledge": ["Nice to meet you, {user_name}!", 
                                   "Hello, {user_name}! How can I help you today?"],
                "fallback": ["I'm not sure I understand. Could you rephrase that?",
                           "I don't have information on that. Could you try asking something else?"],
                "faq": {
                    "hours": ["Our store is open Monday-Friday 9AM-6PM and Saturday 10AM-4PM. We're closed on Sundays."],
                    "return policy": ["You can return any unused item within 30 days with a receipt for a full refund."],
                    "shipping": ["We offer free shipping on orders over $50. Standard shipping typically takes 3-5 business days."],
                    "contact": ["You can reach our customer service team at support@example.com or call us at (555) 123-4567."],
                    "payment": ["We accept all major credit cards, PayPal, and Apple Pay."]
                }
            }
    
    def save_knowledge_base(self):
        """Save the current knowledge base to file"""
        with open('knowledge_base.json', 'w') as f:
            json.dump(self.responses, f, indent=4)
    
    def log_conversation(self, user_input, bot_response):
        """Log the conversation for later analysis"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "user": self.user_name if self.user_name else "User",
            "user_input": user_input,
            "bot_response": bot_response,
            "context": self.conversation_context.copy()
        }
        
        self.conversation_log.append(log_entry)
        
        # Save conversation log to file
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = f"{log_dir}/conversation_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # Try to load existing logs
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Append new log
            logs.append(log_entry)
            
            # Save updated logs
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=4)
        except Exception as e:
            print(f"Warning: Could not save conversation log: {e}")
    
    def _preprocess_text(self, text):
        """Preprocess text for better matching using NLP techniques"""
        if not NLTK_AVAILABLE:
            # Basic preprocessing if NLTK is not available
            return text.lower().translate(str.maketrans('', '', string.punctuation)).split()
        
        # Tokenize, remove stopwords and lemmatize
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token.isalnum() and token not in self.stop_words]
        return tokens
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity between two text inputs"""
        if not NLTK_AVAILABLE:
            # Simple word overlap for basic similarity
            words1 = set(self._preprocess_text(text1))
            words2 = set(self._preprocess_text(text2))
            
            if not words1 or not words2:
                return 0.0
                
            overlap = len(words1.intersection(words2))
            return overlap / min(len(words1), len(words2))
        
        # More sophisticated similarity using TF approach
        tokens1 = self._preprocess_text(text1)
        tokens2 = self._preprocess_text(text2)
        
        if not tokens1 or not tokens2:
            return 0.0
            
        # Count word frequencies
        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)
        
        # Find common words
        common_words = set(counter1.keys()) & set(counter2.keys())
        
        if not common_words:
            return 0.0
            
        # Sum of minimum counts for each common word
        sum_common = sum(min(counter1[word], counter2[word]) for word in common_words)
        
        # Total words in both texts
        total_words = sum(counter1.values()) + sum(counter2.values())
        
        return 2.0 * sum_common / total_words if total_words > 0 else 0.0
    
    def _find_best_faq_match(self, user_input):
        """Find the best matching FAQ for the user's input"""
        best_similarity = 0.0
        best_keyword = None
        
        # Calculate similarity for each FAQ keyword
        for keyword in self.responses["faq"].keys():
            # Combine the keyword with its responses for better matching
            keyword_text = keyword + " " + " ".join(self.responses["faq"][keyword])
            similarity = self._calculate_similarity(user_input, keyword_text)
            
            if similarity > best_similarity and similarity > 0.2:  # Threshold
                best_similarity = similarity
                best_keyword = keyword
        
        return best_keyword, best_similarity
    
    def _extract_name(self, user_input):
        """Extract user's name from input"""
        user_input_lower = user_input.lower()
        
        # Check for "my name is X" pattern
        name_match = re.search(r"my name is ([a-z]+)", user_input_lower)
        if name_match:
            return name_match.group(1).capitalize()
        
        # Check for "call me X" pattern
        if "call me" in user_input_lower:
            name = user_input_lower.split("call me")[1].strip().split()[0]
            return name.capitalize()
        
        # Check for "I am X" pattern
        name_match = re.search(r"i am ([a-z]+)", user_input_lower)
        if name_match:
            potential_name = name_match.group(1).capitalize()
            if potential_name.lower() not in self.stop_words:
                return potential_name
        
        return None
    
    def _update_context(self, user_input, matched_intent=None):
        """Update conversation context"""
        # Save the last query
        self.conversation_context["last_query"] = user_input
        
        # Update topic if an intent was matched
        if matched_intent:
            self.conversation_context["topic"] = matched_intent
    
    def get_response(self, user_input):
        """Generate a response based on user input"""
        if not user_input.strip():
            return random.choice(self.responses["fallback"])
        
        # Try to extract name
        extracted_name = self._extract_name(user_input)
        if extracted_name:
            self.user_name = extracted_name
            return random.choice(self.responses["name_acknowledge"]).format(user_name=self.user_name)
        
        # Check for greetings
        if any(word in user_input.lower() for word in ["hello", "hi", "hey", "greetings"]):
            self._update_context(user_input, "greeting")
            return random.choice(self.responses["greeting"]).format(bot_name=self.name)
            
        # Check for goodbyes
        if any(word in user_input.lower() for word in ["bye", "goodbye", "see you", "thank you", "thanks"]):
            self._update_context(user_input, "goodbye")
            return random.choice(self.responses["goodbye"])
        
        # Find best FAQ match using similarity
        best_keyword, similarity = self._find_best_faq_match(user_input)
        
        if best_keyword:
            self._update_context(user_input, best_keyword)
            return random.choice(self.responses["faq"][best_keyword])
        
        # If no match is found, try using the LLM if available
        if self.use_llm and LLM_AVAILABLE:
            self._update_context(user_input, "llm_response")
            try:
                llm_response = get_llm_response(user_input, self.conversation_log, self.user_name)
                return llm_response
            except Exception as e:
                print(f"Error getting LLM response: {e}")
                # Fall back to default responses if LLM fails
        
        # Fallback response if no match is found and LLM is not available or fails
        self._update_context(user_input)
        return random.choice(self.responses["fallback"])
    
    def add_faq(self, keyword, response):
        """Add a new FAQ to the knowledge base"""
        if keyword not in self.responses["faq"]:
            self.responses["faq"][keyword] = []
        
        self.responses["faq"][keyword].append(response)
        self.save_knowledge_base()
        return f"Added new response for '{keyword}'"


# Demo code
if __name__ == "__main__":
    # Create bot with LLM capabilities if available
    bot = AdvancedSupportBot(use_llm=True)
    print(f"{bot.name}: {bot.get_response('hello')}")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"{bot.name}: {bot.get_response('goodbye')}")
            break
            
        response = bot.get_response(user_input)
        print(f"{bot.name}: {response}")
        
        # Log the conversation
        bot.log_conversation(user_input, response) 