# Rule-Based Chatbot with NLP

This is a simple rule-based chatbot that uses Natural Language Processing (NLP) techniques to understand and respond to user queries. The chatbot implements pattern matching and can handle basic conversations, weather queries, and time-related questions.

## Features

- Natural Language Processing using NLTK
- Rule-based response system
- Weather information using OpenWeatherMap API
- Time and date information
- Basic conversation handling
- Text preprocessing (tokenization, lemmatization, stopword removal)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get an API key from OpenWeatherMap:
   - Go to https://openweathermap.org/
   - Sign up for a free account
   - Get your API key
   - Replace `YOUR_API_KEY` in `chatbot.py` with your actual API key

## Usage

Run the chatbot:
```bash
python chatbot.py
```

### Example Interactions

- Greetings: "Hello", "Hi", "Hey"
- Weather: "What's the weather in London?"
- Time: "What time is it?"
- Farewell: "Goodbye", "Bye"

Type 'quit' to exit the chatbot.

## Customization

You can customize the chatbot by:
1. Adding new rules in the `_load_rules` method
2. Implementing new features in the `get_response` method
3. Adding more sophisticated NLP techniques
4. Integrating additional APIs for more functionality

## Dependencies

- nltk
- requests
- python-dotenv
- scikit-learn
- numpy 