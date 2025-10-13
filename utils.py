import streamlit as st
import uuid
from datetime import datetime, timedelta
import logging

def initialize_session_state():
    """Initialize session state variables"""
    
    # Generate unique session ID if not exists
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Current mood tracking
    if 'current_mood' not in st.session_state:
        st.session_state.current_mood = {"emotion": "normal", "confidence": 0.0}
    
    # Mood history for tracking patterns
    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = []
    
    # Personality selection
    if 'selected_personality' not in st.session_state:
        st.session_state.selected_personality = "Friendly"
    
    # Favorite quotes
    if 'favorite_quotes' not in st.session_state:
        st.session_state.favorite_quotes = []
    
    # Crisis-related states
    if 'crisis_detected' not in st.session_state:
        st.session_state.crisis_detected = False
    
    if 'crisis_acknowledged' not in st.session_state:
        st.session_state.crisis_acknowledged = False
    
    if 'show_crisis_resources' not in st.session_state:
        st.session_state.show_crisis_resources = False
    
    # UI states
    if 'show_quotes' not in st.session_state:
        st.session_state.show_quotes = False
    
    if 'show_mood_history' not in st.session_state:
        st.session_state.show_mood_history = False

def add_mood_to_history(emotion, confidence, timestamp=None):
    """Add detected mood to history for pattern tracking"""
    if timestamp is None:
        timestamp = datetime.now()
    
    mood_entry = {
        "timestamp": timestamp,
        "emotion": emotion,
        "confidence": confidence
    }
    
    st.session_state.mood_history.append(mood_entry)
    
    # Keep only last 50 mood entries to prevent memory issues
    if len(st.session_state.mood_history) > 50:
        st.session_state.mood_history = st.session_state.mood_history[-50:]

def get_mood_trend():
    """Analyze mood trends from recent history"""
    if len(st.session_state.mood_history) < 3:
        return "Not enough data"
    
    recent_moods = st.session_state.mood_history[-10:]  # Last 10 moods
    
    mood_counts = {}
    for mood_entry in recent_moods:
        emotion = mood_entry['emotion']
        mood_counts[emotion] = mood_counts.get(emotion, 0) + 1
    
    dominant_mood = max(mood_counts, key=mood_counts.get)
    
    # Determine trend
    if len(recent_moods) >= 5:
        first_half = recent_moods[:len(recent_moods)//2]
        second_half = recent_moods[len(recent_moods)//2:]
        
        # Count negative emotions
        negative_emotions = {'sad', 'angry', 'upset', 'anxious'}
        
        first_negative = sum(1 for m in first_half if m['emotion'] in negative_emotions)
        second_negative = sum(1 for m in second_half if m['emotion'] in negative_emotions)
        
        if second_negative < first_negative:
            trend = "improving"
        elif second_negative > first_negative:
            trend = "concerning"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    return {
        "dominant_mood": dominant_mood,
        "trend": trend,
        "mood_distribution": mood_counts
    }

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    now = datetime.now()
    diff = now - timestamp
    
    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        return f"{int(diff.total_seconds() / 60)} minutes ago"
    elif diff < timedelta(days=1):
        return f"{int(diff.total_seconds() / 3600)} hours ago"
    else:
        return timestamp.strftime("%B %d, %Y at %I:%M %p")

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return ""
    
    # Remove potential HTML/script tags for safety
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length
    max_length = 1000
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text.strip()

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def get_welcome_message():
    """Get personalized welcome message"""
    from config import Config
    
    personality = st.session_state.get('selected_personality', 'Friendly')
    greeting = Config.PERSONALITIES[personality]["greeting"]
    
    return f"""
    # Welcome to {Config.APP_NAME} 🧠✨
    
    {greeting}
    
    **I'm here to support your mental wellness journey with:**
    - 🎭 Mood detection and tracking
    - 💬 Personalized conversations
    - 🌟 Daily inspiration and quotes  
    - 🆘 Crisis support resources
    
    Feel free to share what's on your mind, and I'll adapt my responses to help you feel heard and supported.
    """

def create_chat_bubble(message, is_user=False, emotion=None, timestamp=None):
    """Create a formatted chat bubble"""
    from config import Config
    
    # Get emoji for emotion if provided
    emotion_emoji = Config.MOOD_EMOJIS.get(emotion, "") if emotion else ""
    
    # Format timestamp
    time_str = format_timestamp(timestamp) if timestamp else ""
    
    if is_user:
        # User message bubble
        st.markdown(f"""
        <div style="text-align: right; margin: 10px 0;">
            <div style="display: inline-block; background: linear-gradient(135deg, #007BFF, #0056B3); 
                        color: white; padding: 10px 15px; border-radius: 20px 20px 5px 20px; 
                        max-width: 70%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                {message} {emotion_emoji}
            </div>
            <div style="font-size: 0.8em; color: #888; margin-top: 5px;">
                {time_str}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message bubble
        st.markdown(f"""
        <div style="text-align: left; margin: 10px 0;">
            <div style="display: inline-block; background: #1a1a3e; color: white; 
                        padding: 10px 15px; border-radius: 20px 20px 20px 5px; 
                        max-width: 70%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        border-left: 3px solid #007BFF;">
                🤖 {message}
            </div>
            <div style="font-size: 0.8em; color: #888; margin-top: 5px;">
                {time_str}
            </div>
        </div>
        """, unsafe_allow_html=True)
