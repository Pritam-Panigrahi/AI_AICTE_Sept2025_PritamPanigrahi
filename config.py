import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Hugging Face API configuration
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    
    # App configuration
    APP_NAME = "MindMate"
    APP_VERSION = "1.0.0"
    
    # Model configurations
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
    
    # UI Configuration
    MOOD_EMOJIS = {
        "normal": "😊",
        "happy": "😄", 
        "sad": "😢",
        "angry": "😠",
        "calm": "😌",
        "upset": "😟",
        "cool": "😎",
        "anxious": "😰",
        "excited": "🤩"
    }
    
    PERSONALITIES = {
        "Friendly": {
            "tone": "warm and approachable",
            "style": "casual and supportive",
            "greeting": "Hey there! I'm here to listen and support you. How are you feeling today?"
        },
        "Professional": {
            "tone": "respectful and clinical",
            "style": "structured and evidence-based",
            "greeting": "Good day. I'm MindMate, your mental health companion. How may I assist you today?"
        },
        "Motivational": {
            "tone": "encouraging and energetic",
            "style": "inspiring and goal-oriented",
            "greeting": "Hello champion! Ready to tackle whatever's on your mind? You've got this!"
        },
        "Calm": {
            "tone": "gentle and soothing",
            "style": "mindful and peaceful",
            "greeting": "Welcome to a peaceful space. Take a deep breath. I'm here to help you find your center."
        }
    }
    
    # Crisis keywords that trigger emergency resources
    CRISIS_KEYWORDS = [
        "suicide", "kill myself", "end it all", "hurt myself", "self harm",
        "worthless", "hopeless", "can't go on", "want to die", "no point"
    ]
