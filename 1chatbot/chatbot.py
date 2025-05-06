import nltk
import json
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests
from datetime import datetime
import time

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class HumanLikeChatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.rules = self._load_rules()
        self.conversation_history = []
        self.user_name = None
        self.last_interaction_time = time.time()
        
    def _load_rules(self):
        return {
            'greetings': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
                'responses': [
                    "Hi there! How are you doing today?",
                    "Hello! It's great to meet you. How can I help you?",
                    "Hey! I'm excited to chat with you. What's on your mind?",
                    "Hi! I hope you're having a wonderful day. How can I assist you?"
                ]
            },
            'farewell': {
                'patterns': ['bye', 'goodbye', 'see you', 'farewell'],
                'responses': [
                    "Goodbye! It was nice chatting with you. Take care!",
                    "See you later! Have a great day ahead!",
                    "Bye for now! Feel free to come back if you need anything.",
                    "Take care! Looking forward to our next conversation!"
                ]
            },
            'thanks': {
                'patterns': ['thank', 'thanks', 'appreciate'],
                'responses': [
                    "You're very welcome! I'm happy I could help.",
                    "My pleasure! Is there anything else you'd like to know?",
                    "Anytime! I'm here to help whenever you need me.",
                    "You're welcome! I'm glad I could be of assistance."
                ]
            },
            'weather': {
                'patterns': ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy'],
                'responses': [
                    "I can help you with the weather! Just let me know which city you're interested in.",
                    "I'd be happy to check the weather for you. Which city would you like to know about?",
                    "I can tell you about the weather conditions. Which location are you curious about?"
                ]
            },
            'time': {
                'patterns': ['time', 'current time', 'what time'],
                'responses': [
                    f"The current time is {datetime.now().strftime('%I:%M %p')}. How's your day going?",
                    f"It's {datetime.now().strftime('%I:%M %p')} right now. Time flies, doesn't it?",
                    f"The clock shows {datetime.now().strftime('%I:%M %p')}. What are you up to?"
                ]
            },
            'how_are_you': {
                'patterns': ['how are you', 'how do you do', 'how\'s it going'],
                'responses': [
                    "I'm doing great, thanks for asking! How about you?",
                    "I'm wonderful! I love helping people and learning new things. How are you feeling today?",
                    "I'm having a good day! I'm here to chat and help. How's your day going?"
                ]
            },
            'name': {
                'patterns': ['what is your name', 'who are you', 'your name'],
                'responses': [
                    "I'm ChatBot, your friendly AI assistant! I'm here to help and chat with you.",
                    "You can call me ChatBot! I'm your digital friend and helper.",
                    "I'm ChatBot, and I'm excited to get to know you better!"
                ]
            },
            'capabilities': {
                'patterns': ['what can you do', 'help me', 'your abilities', 'features'],
                'responses': [
                    "I can help you with various things! I can tell you the weather, current time, and engage in friendly conversation. I'm also learning new things every day!",
                    "I'm here to chat, provide information about weather and time, and be a friendly companion. What would you like to know?",
                    "I can check the weather for you, tell you the time, and have natural conversations. I'm always happy to help and learn!"
                ]
            },
            'default': {
                'responses': [
                    "That's interesting! Could you tell me more about that?",
                    "I'm still learning, but I'd love to hear more about what you're saying.",
                    "That's a fascinating topic! What else would you like to know?",
                    "I'm curious about that! Could you elaborate a bit more?"
                ]
            }
        }

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return tokens

    def get_weather(self, city):
        api_key = "YOUR_API_KEY"  # Replace with your API key
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                temp = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['main'].get('wind_speed', 'N/A')
                
                return f"In {city}, it's currently {temp}°C with {weather_desc}. The humidity is {humidity}% and the wind speed is {wind_speed} m/s. How's the weather where you are?"
            else:
                return "I'm having trouble getting the weather information. Could you double-check the city name?"
        except:
            return "I apologize, but I'm having trouble accessing the weather data right now. Could you try again in a moment?"

    def get_response(self, user_input):
        # Update conversation history
        self.conversation_history.append(("user", user_input))
        
        # Check for time since last interaction
        current_time = time.time()
        time_diff = current_time - self.last_interaction_time
        self.last_interaction_time = current_time
        
        # Add a natural delay response if it's been a while
        if time_diff > 300:  # 5 minutes
            self.conversation_history.append(("bot", "Oh, welcome back! I was wondering where you went. "))
        
        # Preprocess the input
        tokens = self.preprocess_text(user_input)
        
        # Check for weather-related queries
        if any(word in tokens for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']):
            words = user_input.lower().split()
            if 'in' in words:
                city_index = words.index('in') + 1
                if city_index < len(words):
                    city = words[city_index]
                    response = self.get_weather(city)
                    self.conversation_history.append(("bot", response))
                    return response
        
        # Check for time-related queries
        if any(word in tokens for word in ['time', 'current time']):
            response = f"The current time is {datetime.now().strftime('%I:%M %p')}. How's your day going?"
            self.conversation_history.append(("bot", response))
            return response
        
        # Check other rules
        for intent, data in self.rules.items():
            if intent != 'default':
                if any(pattern in tokens for pattern in data['patterns']):
                    response = random.choice(data['responses'])
                    self.conversation_history.append(("bot", response))
                    return response
        
        # Default response if no rules match
        response = random.choice(self.rules['default']['responses'])
        self.conversation_history.append(("bot", response))
        return response

def main():
    print("ChatBot: Hello! I'm your friendly AI assistant. I'm here to chat and help you with various things. What's your name?")
    chatbot = HumanLikeChatbot()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("ChatBot: Goodbye! It was wonderful chatting with you. Take care!")
            break
            
        response = chatbot.get_response(user_input)
        print("ChatBot:", response)

if __name__ == "__main__":
    main() 