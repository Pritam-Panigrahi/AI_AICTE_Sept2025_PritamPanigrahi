import streamlit as st
import json
from datetime import datetime

class CrisisResources:
    def __init__(self, resources_file="data/crisis_contacts.json"):
        self.resources_file = resources_file
        self.resources = self.load_resources()
    
    def load_resources(self):
        """Load crisis resources from JSON file"""
        try:
            with open(self.resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.get_default_resources()
    
    def get_default_resources(self):
        """Return default crisis resources"""
        return {
            "emergency": {
                "title": "🚨 Emergency Services",
                "contacts": [
                    {"name": "Emergency Services", "number": "911", "description": "Immediate emergency response"},
                    {"name": "Crisis Text Line", "number": "Text HOME to 741741", "description": "24/7 crisis counseling via text"}
                ]
            },
            "suicide_prevention": {
                "title": "🆘 Suicide Prevention",
                "contacts": [
                    {"name": "988 Suicide & Crisis Lifeline", "number": "988", "description": "24/7 confidential support for people in distress"},
                    {"name": "International Association for Suicide Prevention", "number": "Visit iasp.info/resources/Crisis_Centres/", "description": "Global crisis center directory"}
                ]
            },
            "mental_health": {
                "title": "🧠 Mental Health Support",
                "contacts": [
                    {"name": "NAMI Helpline", "number": "1-800-950-NAMI (6264)", "description": "National Alliance on Mental Illness support"},
                    {"name": "SAMHSA National Helpline", "number": "1-800-662-4357", "description": "Mental health and substance abuse treatment referrals"}
                ]
            },
            "student_resources": {
                "title": "🎓 Student Support",
                "contacts": [
                    {"name": "Campus Counseling Center", "number": "Contact your institution", "description": "On-campus mental health services"},
                    {"name": "Student Health Services", "number": "Available at most colleges", "description": "Medical and psychological support for students"}
                ]
            },
            "online_resources": {
                "title": "💻 Online Support",
                "contacts": [
                    {"name": "BetterHelp", "number": "betterhelp.com", "description": "Online counseling and therapy"},
                    {"name": "7 Cups", "number": "7cups.com", "description": "Free emotional support and online therapy"},
                    {"name": "MindfulnessApps", "number": "Headspace, Calm, Insight Timer", "description": "Meditation and mindfulness apps"}
                ]
            }
        }
    
    def display_crisis_popup(self):
        """Display crisis resources in a prominent way"""
        st.error("🚨 **CRISIS DETECTED** - You may be experiencing a mental health emergency")
        
        st.markdown("### 🆘 **Immediate Help Available**")
        
        # Emergency contacts
        emergency_contacts = self.resources["emergency"]["contacts"]
        for contact in emergency_contacts:
            st.markdown(f"**{contact['name']}**: {contact['number']}")
            st.caption(contact['description'])
        
        # Prominent call-to-action
        st.markdown("---")
        st.markdown("### 🤝 **You are not alone. Help is available 24/7.**")
        
        # Quick access buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📞 View All Crisis Resources", type="primary", use_container_width=True):
                st.session_state.show_crisis_resources = True
        
        with col2:
            if st.button("💬 Continue Conversation", type="secondary", use_container_width=True):
                st.session_state.crisis_acknowledged = True
    
    def display_resources_page(self):
        """Display comprehensive crisis resources page"""
        st.markdown("# 🆘 Crisis Resources & Support")
        
        st.markdown("""
        **If you're having thoughts of self-harm or suicide, please reach out immediately. 
        You matter, and help is available 24/7.**
        """)
        
        # Emergency notice
        st.error("**🚨 If this is an emergency, call 911 or go to your nearest emergency room immediately.**")
        
        # Display all resource categories
        for category_key, category_data in self.resources.items():
            st.markdown(f"## {category_data['title']}")
            
            for contact in category_data['contacts']:
                with st.container():
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.markdown(f"**{contact['name']}**")
                        st.caption(contact['description'])
                    
                    with col2:
                        st.markdown(f"`{contact['number']}`")
            
            st.markdown("---")
        
        # Additional resources
        st.markdown("## 📚 Additional Resources")
        
        with st.expander("🧘 Self-Care & Coping Strategies"):
            st.markdown("""
            - **Breathing Exercise**: Try the 4-7-8 technique (inhale 4, hold 7, exhale 8)
            - **Grounding**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste
            - **Movement**: Take a short walk, do gentle stretches, or try yoga
            - **Connection**: Reach out to a trusted friend, family member, or counselor
            - **Creative Expression**: Draw, write, play music, or engage in any creative activity
            """)
        
        with st.expander("⚠️ Warning Signs to Watch For"):
            st.markdown("""
            - Persistent thoughts of death or suicide
            - Feeling hopeless or trapped
            - Extreme mood changes
            - Withdrawal from friends and activities
            - Increased use of alcohol or drugs
            - Giving away prized possessions
            - Saying goodbye to loved ones
            - Putting affairs in order
            """)
        
        with st.expander("🤝 How to Help Others"):
            st.markdown("""
            - **Listen** without judgment
            - **Ask directly** about suicide if you're concerned
            - **Take it seriously** - don't dismiss their feelings
            - **Stay with them** or ensure they're not alone
            - **Help them connect** with professional resources
            - **Follow up** regularly to show you care
            """)
    
    def get_quick_resources(self):
        """Get a condensed list of the most important resources"""
        quick_resources = []
        
        # Add emergency and suicide prevention resources
        for category in ["emergency", "suicide_prevention"]:
            if category in self.resources:
                quick_resources.extend(self.resources[category]["contacts"][:2])  # First 2 from each
        
        return quick_resources
    
    def log_crisis_interaction(self, user_message):
        """Log crisis interactions for monitoring (anonymized)"""
        # In a real application, this would log to a secure system
        # For now, we'll just log the timestamp and fact that crisis resources were shown
        timestamp = datetime.now().isoformat()
        
        # This would be sent to a secure logging system in production
        crisis_log = {
            "timestamp": timestamp,
            "crisis_keywords_detected": True,
            "resources_shown": True,
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        # In production, send this to appropriate monitoring/logging system
        print(f"Crisis interaction logged: {timestamp}")
