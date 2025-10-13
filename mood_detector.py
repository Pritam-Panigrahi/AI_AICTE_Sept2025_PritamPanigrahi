import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from config import Config
import logging

class MoodDetector:
    def __init__(self):
        self.emotion_classifier = None
        self.sentiment_classifier = None
        self.setup_models()
    
    def setup_models(self):
        """Initialize the emotion and sentiment analysis models"""
        try:
            # Initialize emotion classifier
            self.emotion_classifier = pipeline(
                "text-classification",
                model=Config.EMOTION_MODEL,
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Initialize sentiment classifier for backup
            self.sentiment_classifier = pipeline(
                "sentiment-analysis",
                model=Config.SENTIMENT_MODEL,
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1
            )
            
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            logging.error(f"Model loading error: {str(e)}")
    
    def detect_emotion(self, text):
        """Detect emotion from text input"""
        if not text or not self.emotion_classifier:
            return {"emotion": "normal", "confidence": 0.0, "all_scores": []}
        
        try:
            # Get emotion predictions
            results = self.emotion_classifier(text)
            
            # Process results
            if results and len(results) > 0:
                # Get the highest scoring emotion
                top_emotion = max(results[0], key=lambda x: x['score'])
                
                emotion_mapping = {
                    'joy': 'happy',
                    'sadness': 'sad',
                    'anger': 'angry',
                    'fear': 'anxious',
                    'surprise': 'excited',
                    'disgust': 'upset',
                    'neutral': 'normal'
                }
                
                detected_emotion = emotion_mapping.get(top_emotion['label'].lower(), 'normal')
                
                return {
                    "emotion": detected_emotion,
                    "confidence": top_emotion['score'],
                    "all_scores": results[0]
                }
        
        except Exception as e:
            st.error(f"Error detecting emotion: {str(e)}")
            logging.error(f"Emotion detection error: {str(e)}")
        
        return {"emotion": "normal", "confidence": 0.0, "all_scores": []}
    
    def get_mood_emoji(self, emotion):
        """Get emoji for detected emotion"""
        return Config.MOOD_EMOJIS.get(emotion, "😊")
    
    def analyze_sentiment_intensity(self, text):
        """Analyze sentiment intensity for more nuanced responses"""
        if not text or not self.sentiment_classifier:
            return {"label": "NEUTRAL", "score": 0.5}
        
        try:
            results = self.sentiment_classifier(text)
            if results and len(results) > 0:
                return max(results[0], key=lambda x: x['score'])
        except Exception as e:
            logging.error(f"Sentiment analysis error: {str(e)}")
        
        return {"label": "NEUTRAL", "score": 0.5}
    
    def detect_crisis_indicators(self, text):
        """Check for crisis-related keywords in the text"""
        if not text:
            return False
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in Config.CRISIS_KEYWORDS)
