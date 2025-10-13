import streamlit as st
from transformers import pipeline
import random
from config import Config
import logging
from datetime import datetime

class MindMateChatbot:
    def __init__(self):
        self.conversation_history = []
        self.current_personality = "Friendly"
        self.setup_conversation_model()
    
    def setup_conversation_model(self):
        """Initialize conversation model if needed"""
        # Using rule-based responses for now, can be enhanced with language models
        self.response_templates = {
            "Friendly": {
                "happy": [
                    "That's wonderful to hear! Your positive energy is really shining through. What's been making you feel so good?",
                    "I love seeing you happy! It sounds like things are going well for you. Want to share what's bringing you joy?",
                    "Your happiness is contagious! I'm so glad you're feeling great today."
                ],
                "sad": [
                    "I hear that you're going through a tough time, and I want you to know that it's okay to feel sad. Your feelings are valid.",
                    "I'm sorry you're feeling down. Sometimes sadness can feel overwhelming, but you're not alone in this.",
                    "It sounds like you're carrying some heavy feelings right now. I'm here to listen and support you through this."
                ],
                "angry": [
                    "I can sense your frustration, and that's completely understandable. Anger often comes from caring deeply about something.",
                    "It sounds like something really got under your skin. Want to talk about what's bothering you?",
                    "Your anger is valid. Sometimes we need to feel these intense emotions to work through what's bothering us."
                ],
                "anxious": [
                    "I can hear the worry in your words. Anxiety can feel really overwhelming, but you're taking a brave step by reaching out.",
                    "It sounds like your mind might be racing with concerns. Let's take this one step at a time together.",
                    "Anxiety can make everything feel more intense. Remember, you've handled difficult situations before, and you can get through this too."
                ],
                "normal": [
                    "Thanks for sharing with me. How has your day been treating you?",
                    "I'm here and listening. What's on your mind today?",
                    "It's good to hear from you. What would you like to talk about?"
                ]
            },
            "Professional": {
                "happy": [
                    "I observe positive emotional indicators in your communication. This suggests effective coping mechanisms are currently in place.",
                    "Your current emotional state appears stable and positive. What strategies have you been using to maintain this wellbeing?",
                    "The positive affect you're demonstrating is encouraging. Let's explore what factors are contributing to this state."
                ],
                "sad": [
                    "I recognize you're experiencing emotional distress. This is a normal human response to challenging circumstances.",
                    "Your emotional expression indicates you may be processing difficult experiences. This is part of healthy emotional functioning.",
                    "I acknowledge the sadness you're experiencing. These feelings often signal areas that require attention and care."
                ],
                "angry": [
                    "Your emotional response suggests you may be encountering situations that conflict with your values or boundaries.",
                    "Anger often serves as an indicator of unmet needs or perceived injustices. Let's explore what might be underlying these feelings.",
                    "I recognize the intensity of your emotional state. Anger can be a protective mechanism signaling important concerns."
                ],
                "anxious": [
                    "Anxiety responses often indicate your system is preparing for perceived challenges. This is a normal adaptive function.",
                    "I observe indicators of heightened stress response. Let's work together to identify effective coping strategies.",
                    "Your anxiety suggests your mind is actively processing potential concerns. We can explore grounding techniques to help manage this."
                ],
                "normal": [
                    "I'm available to provide support and guidance. What areas of your wellbeing would you like to focus on today?",
                    "How may I assist you in exploring your current mental and emotional state?",
                    "I'm here to provide professional support. What would you like to discuss in our session today?"
                ]
            },
            "Motivational": {
                "happy": [
                    "YES! This is the energy I love to see! You're absolutely crushing it right now. Keep riding this wave of positivity!",
                    "You're GLOWING with positive vibes! This is proof that you have the power to create amazing moments in your life!",
                    "Look at you being absolutely amazing! Your happiness is proof of your resilience and strength!"
                ],
                "sad": [
                    "I know it's tough right now, but here's what I see: a warrior who's still fighting. That takes incredible strength!",
                    "Every champion faces difficult rounds, but you're still standing. This sadness is temporary, but your strength is permanent!",
                    "You're going through the storm right now, but storms pass and make us stronger. You've got everything it takes to get through this!"
                ],
                "angry": [
                    "That fire inside you? That's your passion speaking! Let's channel that powerful energy into something that moves you forward!",
                    "Your anger shows you care deeply about something - that's the spirit of a fighter! Let's turn that intensity into your superpower!",
                    "I feel that energy! You're not backing down, and that's the attitude of someone who creates change. Let's direct that power!"
                ],
                "anxious": [
                    "Your anxiety means you care about the outcome - that's actually a sign of someone who strives for excellence!",
                    "Those butterflies? They're just excitement in disguise! Your body is getting ready for you to do something amazing!",
                    "Anxiety is often just excitement without breath. Let's take some deep breaths and turn this nervous energy into unstoppable momentum!"
                ],
                "normal": [
                    "You showed up today, and that's already a victory! What amazing thing are we going to tackle together?",
                    "Every conversation is a chance to grow stronger and more awesome. What's your next goal, champion?",
                    "You're here, you're present, and you're ready to make things happen. That's the attitude of a winner!"
                ]
            },
            "Calm": {
                "happy": [
                    "Your joy flows like a gentle stream, bringing light to this moment. Rest in this beautiful feeling.",
                    "Like sunshine breaking through clouds, your happiness illuminates the space around you. Breathe it in deeply.",
                    "This happiness is a gift to yourself and others. Let it settle gently into your heart."
                ],
                "sad": [
                    "Sadness, like rain, nourishes growth in ways we cannot always see. Your tears are valid and healing.",
                    "In this quiet space, your sadness can exist without judgment. You are held and supported in this feeling.",
                    "Like winter preparing the earth for spring, your sadness may be preparing you for new growth. Be gentle with yourself."
                ],
                "angry": [
                    "Your anger is like a wave - powerful and temporary. Let it wash through you without resistance.",
                    "This fire within you speaks of boundaries that need honoring. Breathe and listen to what it's teaching you.",
                    "Anger can be a teacher, showing us what matters deeply. Observe it with curiosity rather than judgment."
                ],
                "anxious": [
                    "Your mind is like a busy sky, filled with swirling thoughts. Breathe deeply and find the still space within.",
                    "Anxiety is your mind trying to protect you. Thank it, then gently return your attention to this present moment.",
                    "Like clouds passing across the sky, these anxious thoughts will move through you. You are the vast, peaceful sky."
                ],
                "normal": [
                    "In this peaceful moment, we can simply be present together. What would bring you comfort today?",
                    "Like sitting by a quiet lake, we can find stillness here together. What's flowing through your mind?",
                    "This is a sacred space for whatever you need to express. Speak from your heart."
                ]
            }
        }
    
    def get_personality_response(self, emotion, text=""):
        """Generate a response based on current personality and detected emotion"""
        personality_responses = self.response_templates.get(self.current_personality, {})
        emotion_responses = personality_responses.get(emotion, personality_responses.get("normal", []))
        
        if emotion_responses:
            base_response = random.choice(emotion_responses)
        else:
            base_response = "I understand. Tell me more about how you're feeling."
        
        # Add contextual follow-ups based on personality
        follow_ups = self.get_contextual_followup(emotion)
        
        return f"{base_response}\n\n{follow_ups}"
    
    def get_contextual_followup(self, emotion):
        """Add personality-specific follow-up questions or suggestions"""
        followups = {
            "Friendly": {
                "sad": "Would you like to share what's been weighing on your mind? Sometimes talking helps lighten the load.",
                "anxious": "Have you tried any relaxation techniques that work for you? I'd love to suggest some if you're interested.",
                "angry": "It might help to talk through what's frustrating you. I'm here to listen without judgment.",
                "happy": "This positivity is amazing! What advice would you give to someone who's having a tough day?",
                "normal": "Is there anything specific you'd like to explore or talk through today?"
            },
            "Professional": {
                "sad": "Would you like to explore coping strategies that might help you navigate these feelings?",
                "anxious": "I can guide you through some evidence-based techniques for managing anxiety if you're interested.",
                "angry": "Let's identify the underlying triggers and work on constructive responses to these situations.",
                "happy": "What factors have contributed to this positive emotional state? Understanding these can help maintain wellbeing.",
                "normal": "What therapeutic goals would you like to focus on in our interaction today?"
            },
            "Motivational": {
                "sad": "You're stronger than you realize! What's one small step you could take today to move forward?",
                "anxious": "You've overcome challenges before - you have that same strength now! What's helped you succeed in the past?",
                "angry": "That passion can fuel incredible achievements! How can we channel this energy into something empowering?",
                "happy": "You're on fire! What goals are you excited to crush next?",
                "normal": "What amazing potential are we going to unlock today? I believe in you!"
            },
            "Calm": {
                "sad": "Would you like to try a gentle breathing exercise together, or would you prefer to simply rest in this space?",
                "anxious": "Perhaps we could explore some grounding techniques to help settle your mind and body?",
                "angry": "Would it help to sit with this feeling for a moment, breathing through it mindfully?",
                "happy": "How beautiful. Would you like to savor this moment with a brief mindfulness practice?",
                "normal": "Would you like to explore what's present in your inner landscape right now?"
            }
        }
        
        return followups.get(self.current_personality, {}).get(emotion, "How can I best support you right now?")
    
    def add_to_history(self, user_message, bot_response, emotion, timestamp=None):
        """Add conversation to history"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.conversation_history.append({
            "timestamp": timestamp,
            "user_message": user_message,
            "bot_response": bot_response,
            "detected_emotion": emotion,
            "personality": self.current_personality
        })
    
    def set_personality(self, personality):
        """Change chatbot personality"""
        if personality in Config.PERSONALITIES:
            self.current_personality = personality
            return True
        return False
    
    def get_greeting(self):
        """Get personality-specific greeting"""
        return Config.PERSONALITIES[self.current_personality]["greeting"]
    
    def get_crisis_response(self):
        """Generate crisis-specific response"""
        crisis_responses = {
            "Friendly": "I'm really concerned about you right now. Your safety and wellbeing are the most important things. Please consider reaching out to a crisis helpline - they have people specially trained to help in situations like this.",
            "Professional": "I've detected language that suggests you may be experiencing a mental health crisis. I strongly recommend immediate professional intervention. Please contact a crisis helpline or emergency services.",
            "Motivational": "Hey, I need you to know that you matter more than you realize. Right now, the most important thing is getting you proper support. Please reach out to a crisis helpline - they're there specifically for you.",
            "Calm": "I sense you're in deep pain right now. In this moment, the most loving thing you can do for yourself is reach out for professional help. You deserve care and support."
        }
        
        return crisis_responses.get(self.current_personality, crisis_responses["Friendly"])
