import re
import random
import datetime
import json
import os

class SupportBot:
    def __init__(self, name="Support Bot"):
        self.name = name
        self.user_name = None
        self.conversation_log = []
        
        # Load responses from knowledge base
        self.responses = self._load_knowledge_base()
    
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
            "bot_response": bot_response
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
    
    def get_response(self, user_input):
        """Generate a response based on user input"""
        if not user_input.strip():
            return random.choice(self.responses["fallback"])
        
        # Convert to lowercase for easier matching
        user_input_lower = user_input.lower()
        
        # Check if user is introducing themselves
        name_match = re.search(r"my name is ([a-z]+)", user_input_lower)
        if name_match or "call me" in user_input_lower:
            if name_match:
                self.user_name = name_match.group(1).capitalize()
            else:
                # Extract name after "call me"
                self.user_name = user_input_lower.split("call me")[1].strip().capitalize()
            
            response = random.choice(self.responses["name_acknowledge"]).format(user_name=self.user_name)
            return response
        
        # Check for greetings
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.responses["greeting"]).format(bot_name=self.name)
            
        # Check for goodbyes
        if any(word in user_input_lower for word in ["bye", "goodbye", "see you", "thank you", "thanks"]):
            return random.choice(self.responses["goodbye"])
        
        # Check for FAQs
        for keyword, responses in self.responses["faq"].items():
            if keyword in user_input_lower:
                return random.choice(responses)
        
        # Fallback response if no match is found
        return random.choice(self.responses["fallback"])
    
    def add_faq(self, keyword, response):
        """Add a new FAQ to the knowledge base"""
        if keyword not in self.responses["faq"]:
            self.responses["faq"][keyword] = []
        
        self.responses["faq"][keyword].append(response)
        self.save_knowledge_base()
        return f"Added new response for '{keyword}'" 