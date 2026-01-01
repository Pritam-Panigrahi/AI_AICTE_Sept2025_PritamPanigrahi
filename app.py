import streamlit as st
import logging
from datetime import datetime
import traceback

# Import custom modules
from config import Config
from mood_detector import MoodDetector
from chatbot import MindMateChatbot
from quotes_manager import QuotesManager
from crisis_resources import CrisisResources
from utils import (
    initialize_session_state, add_mood_to_history, 
    get_mood_trend, sanitize_input, setup_logging, 
    get_welcome_message, create_chat_bubble
)

# Setup logging
setup_logging()

# Configure Streamlit page
st.set_page_config(
    page_title="MindMate - AI Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for dark theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0A0A23, #1a1a3e);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
    }
    
    .mood-indicator {
        background: linear-gradient(135deg, #007BFF, #0056B3);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        color: white;
    }
    
    .crisis-alert {
        background: linear-gradient(135deg, #DC3545, #B02A37);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .quote-card {
        background: linear-gradient(135deg, #1a1a3e, #2a2a4e);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #007BFF;
        color: white;
    }
    
    .personality-selector {
        background: #1a1a3e;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0A0A23, #1a1a3e);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    try:
        mood_detector = MoodDetector()
        chatbot = MindMateChatbot()
        quotes_manager = QuotesManager()
        crisis_resources = CrisisResources()
    except Exception as e:
        st.error(f"Error initializing application components: {str(e)}")
        st.error("Please ensure all required dependencies are installed.")
        return
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 MindMate - Your AI Mental Health Companion</h1>
        <p>Supporting your mental wellness journey with empathy, understanding, and resources</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    setup_sidebar(mood_detector, quotes_manager, crisis_resources)
    
    # Main content area
    if st.session_state.get('show_crisis_resources', False):
        display_crisis_resources_page(crisis_resources)
    elif st.session_state.get('show_quotes', False):
        display_quotes_page(quotes_manager)
    elif st.session_state.get('show_mood_history', False):
        display_mood_history_page()
    else:
        display_chat_interface(mood_detector, chatbot, crisis_resources)

def setup_sidebar(mood_detector, quotes_manager, crisis_resources):
    """Setup the sidebar with mood tracking, personality selection, and resources"""
    
    with st.sidebar:
        st.markdown("## 🎭 Current Mood")
        
        # Display current mood
        current_mood = st.session_state.get('current_mood', {"emotion": "normal", "confidence": 0.0})
        mood_emoji = Config.MOOD_EMOJIS.get(current_mood['emotion'], "😊")
        confidence = current_mood['confidence']
        
        st.markdown(f"""
        <div class="mood-indicator">
            <h2>{mood_emoji}</h2>
            <h4>{current_mood['emotion'].title()}</h4>
            <p>Confidence: {confidence:.2%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mood trend
        try:
            trend = get_mood_trend()
            if isinstance(trend, dict):
                st.markdown(f"**Trend**: {trend['trend'].title()}")
        except Exception as e:
            logging.error(f"Error getting mood trend: {str(e)}")
        
        st.markdown("---")
        
        # Personality selector
        st.markdown("## 🤖 Chatbot Personality")
        
        personalities = list(Config.PERSONALITIES.keys())
        selected_personality = st.selectbox(
            "Choose conversation style:",
            personalities,
            index=personalities.index(st.session_state.get('selected_personality', 'Friendly')),
            help="Select how you'd like me to respond to you"
        )
        
        if selected_personality != st.session_state.get('selected_personality'):
            st.session_state.selected_personality = selected_personality
            st.success(f"Switched to {selected_personality} personality!")
            st.rerun()
        
        # Display current personality info
        personality_info = Config.PERSONALITIES[selected_personality]
        st.markdown(f"""
        <div class="personality-selector">
            <small><strong>Style:</strong> {personality_info['tone']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## 🌟 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 View Mood History", use_container_width=True):
                st.session_state.show_mood_history = True
                st.rerun()
        
        with col2:
            if st.button("💡 Browse Quotes", use_container_width=True):
                st.session_state.show_quotes = True
                st.rerun()
        
        # Daily quote
        st.markdown("## 🌅 Quote of the Day")
        
        daily_quote = quotes_manager.get_daily_quote()
        st.markdown(f"""
        <div class="quote-card">
            <p style="font-style: italic; margin-bottom: 10px;">"{daily_quote['text']}"</p>
            <p style="text-align: right; font-size: 0.9em; margin: 0;">— {daily_quote['author']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Favorite quote button
        if st.button("⭐ Add to Favorites", key="fav_daily"):
            if quotes_manager.add_to_favorites(daily_quote):
                st.success("Added to favorites!")
            else:
                st.info("Already in favorites!")
        
        st.markdown("---")
        
        # Crisis resources - always visible
        st.markdown("## 🆘 Need Help?")
        
        if st.button("🚨 Crisis Resources", type="primary", use_container_width=True):
            st.session_state.show_crisis_resources = True
            st.rerun()
        
        # Quick crisis contacts
        quick_resources = crisis_resources.get_quick_resources()
        with st.expander("Quick Contacts"):
            for resource in quick_resources[:2]:  # Show top 2
                st.markdown(f"**{resource['name']}**")
                st.markdown(f"`{resource['number']}`")

def display_chat_interface(mood_detector, chatbot, crisis_resources):
    """Display the main chat interface"""
    
    # Set chatbot personality if changed
    chatbot.set_personality(st.session_state.selected_personality)
    
    # Welcome message for new sessions
    if not st.session_state.chat_history:
        welcome_msg = get_welcome_message()
        st.markdown(welcome_msg)
        
        # Add welcome to chat history
        st.session_state.chat_history.append({
            "timestamp": datetime.now(),
            "user_message": None,
            "bot_response": welcome_msg,
            "detected_emotion": "normal",
            "is_welcome": True
        })
    
    # Display chat history
    st.markdown("## 💬 Conversation")
    
    # Create chat container
    chat_container = st.container()
    
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat.get('is_welcome'):
                continue  # Skip welcome message in chat bubbles
            
            if chat['user_message']:
                create_chat_bubble(
                    chat['user_message'], 
                    is_user=True, 
                    emotion=chat.get('detected_emotion'),
                    timestamp=chat['timestamp']
                )
            
            if chat['bot_response']:
                create_chat_bubble(
                    chat['bot_response'], 
                    is_user=False,
                    timestamp=chat['timestamp']
                )
    
    # Chat input
    st.markdown("---")
    
    # Crisis detection warning
    if st.session_state.get('crisis_detected') and not st.session_state.get('crisis_acknowledged'):
        crisis_resources.display_crisis_popup()
        return
    
    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Share what's on your mind...",
            placeholder="Type your message here. I'm here to listen and support you.",
            height=100,
            key="user_input"
        )
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write("")
        
        with col2:
            submit_button = st.form_submit_button("Send 💬", type="primary", use_container_width=True)
    
    # Process user input
    if submit_button and user_input.strip():
        try:
            with st.spinner("MindMate is thinking..."):
                # Sanitize input
                clean_input = sanitize_input(user_input)
                
                # Detect mood and crisis indicators
                mood_result = mood_detector.detect_emotion(clean_input)
                is_crisis = mood_detector.detect_crisis_indicators(clean_input)
                
                # Update current mood
                st.session_state.current_mood = {
                    "emotion": mood_result['emotion'],
                    "confidence": mood_result['confidence']
                }
                
                # Add to mood history
                add_mood_to_history(mood_result['emotion'], mood_result['confidence'])
                
                # Handle crisis detection
                if is_crisis:
                    st.session_state.crisis_detected = True
                    crisis_resources.log_crisis_interaction(clean_input)
                    bot_response = chatbot.get_crisis_response()
                else:
                    # Generate normal response
                    bot_response = chatbot.get_personality_response(mood_result['emotion'], clean_input)
                
                # Add to chat history
                chat_entry = {
                    "timestamp": datetime.now(),
                    "user_message": clean_input,
                    "bot_response": bot_response,
                    "detected_emotion": mood_result['emotion']
                }
                
                st.session_state.chat_history.append(chat_entry)
                chatbot.add_to_history(clean_input, bot_response, mood_result['emotion'])
                
                # Rerun to show new messages
                st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred while processing your message: {str(e)}")
            logging.error(f"Chat processing error: {str(e)}\n{traceback.format_exc()}")

def display_quotes_page(quotes_manager):
    """Display the quotes browsing page"""
    
    st.markdown("# 💡 Inspirational Quotes")
    
    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Chat"):
            st.session_state.show_quotes = False
            st.rerun()
    
    # Quote categories
    st.markdown("## Browse by Category")
    
    categories = quotes_manager.get_quote_categories()
    selected_category = st.selectbox("Choose a category:", ["All"] + categories)
    
    # Search functionality
    search_term = st.text_input("🔍 Search quotes:", placeholder="Search by text or author...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random Quote", use_container_width=True):
            if selected_category == "All":
                quote = quotes_manager.get_random_quote()
            else:
                quote = quotes_manager.get_random_quote(selected_category)
            
            st.markdown(f"""
            <div class="quote-card">
                <h4>Random Quote</h4>
                <p style="font-style: italic;">"{quote['text']}"</p>
                <p style="text-align: right;">— {quote['author']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⭐ View Favorites", use_container_width=True):
            favorites = quotes_manager.get_favorites()
            if favorites:
                st.markdown("### ⭐ Your Favorite Quotes")
                for i, fav_quote in enumerate(favorites):
                    with st.container():
                        st.markdown(f"""
                        <div class="quote-card">
                            <p style="font-style: italic;">"{fav_quote['text']}"</p>
                            <p style="text-align: right;">— {fav_quote['author']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"❌ Remove from Favorites", key=f"remove_fav_{i}"):
                            quotes_manager.remove_from_favorites(fav_quote)
                            st.success("Removed from favorites!")
                            st.rerun()
            else:
                st.info("No favorite quotes yet. Add some by clicking the ⭐ button!")
    
    with col3:
        if st.button("🔄 Refresh Daily Quote", use_container_width=True):
            daily_quote = quotes_manager.get_daily_quote()
            st.markdown(f"""
            <div class="quote-card">
                <h4>Quote of the Day</h4>
                <p style="font-style: italic;">"{daily_quote['text']}"</p>
                <p style="text-align: right;">— {daily_quote['author']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display quotes based on search/category
    if search_term:
        results = quotes_manager.search_quotes(search_term)
        st.markdown(f"### 🔍 Search Results ({len(results)} found)")
        
        for quote in results:
            with st.container():
                st.markdown(f"""
                <div class="quote-card">
                    <p style="font-style: italic;">"{quote['text']}"</p>
                    <p style="text-align: right;">— {quote['author']}</p>
                    <small>Category: {quote.get('category', 'Unknown')}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⭐ Add to Favorites", key=f"fav_{quote['text'][:20]}"):
                    if quotes_manager.add_to_favorites(quote):
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")
    
    elif selected_category != "All":
        # Display quotes from selected category
        category_quotes = quotes_manager.quotes.get(selected_category, [])
        st.markdown(f"### 📚 {selected_category.replace('_', ' ').title()} Quotes")
        
        for quote in category_quotes:
            with st.container():
                st.markdown(f"""
                <div class="quote-card">
                    <p style="font-style: italic;">"{quote['text']}"</p>
                    <p style="text-align: right;">— {quote['author']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⭐ Add to Favorites", key=f"fav_cat_{quote['text'][:20]}"):
                    if quotes_manager.add_to_favorites(quote):
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")

def display_mood_history_page():
    """Display mood tracking history and analytics"""
    
    st.markdown("# 📊 Mood History & Analytics")
    
    # Navigation
    if st.button("← Back to Chat"):
        st.session_state.show_mood_history = False
        st.rerun()
    
    mood_history = st.session_state.get('mood_history', [])
    
    if not mood_history:
        st.info("No mood data available yet. Start chatting to see your mood patterns!")
        return
    
    # Mood trend analysis
    try:
        trend = get_mood_trend()
        
        if isinstance(trend, dict):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Dominant Mood", trend['dominant_mood'].title())
            
            with col2:
                st.metric("Current Trend", trend['trend'].title())
            
            with col3:
                st.metric("Mood Entries", len(mood_history))
            
            # Mood distribution
            st.markdown("## 📈 Mood Distribution")
            
            mood_dist = trend['mood_distribution']
            
            # Create a simple chart using Streamlit's built-in charting
            import pandas as pd
            
            df = pd.DataFrame(list(mood_dist.items()), columns=['Mood', 'Count'])
            st.bar_chart(df.set_index('Mood'))
            
    except Exception as e:
        logging.error(f"Error displaying mood analytics: {str(e)}")
        st.error("Unable to generate mood analytics at this time.")
    
    # Recent mood history
    st.markdown("## 📝 Recent Mood History")
    
    # Show last 20 entries
    recent_moods = mood_history[-20:] if len(mood_history) > 20 else mood_history
    
    for mood_entry in reversed(recent_moods):  # Most recent first
        timestamp = mood_entry['timestamp']
        emotion = mood_entry['emotion']
        confidence = mood_entry['confidence']
        emoji = Config.MOOD_EMOJIS.get(emotion, "😊")
        
        # Format timestamp
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        
        st.markdown(f"""
        <div class="mood-indicator" style="margin: 5px 0; padding: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.5em;">{emoji}</span>
                    <strong style="margin-left: 10px;">{emotion.title()}</strong>
                </div>
                <div style="text-align: right;">
                    <div>{confidence:.1%} confidence</div>
                    <small>{time_str}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_crisis_resources_page(crisis_resources):
    """Display comprehensive crisis resources"""
    
    # Navigation
    if st.button("← Back to Chat"):
        st.session_state.show_crisis_resources = False
        st.rerun()
    
    crisis_resources.display_resources_page()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("An unexpected error occurred. Please refresh the page.")
        logging.error(f"Main application error: {str(e)}\n{traceback.format_exc()}")
