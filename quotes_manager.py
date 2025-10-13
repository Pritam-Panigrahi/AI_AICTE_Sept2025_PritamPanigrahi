import json
import random
import streamlit as st
from datetime import date
import logging

class QuotesManager:
    def __init__(self, quotes_file="data/quotes.json"):
        self.quotes_file = quotes_file
        self.quotes = self.load_quotes()
        self.initialize_favorites()
    
    def load_quotes(self):
        """Load quotes from JSON file"""
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Quotes file {self.quotes_file} not found. Using default quotes.")
            return self.get_default_quotes()
        except json.JSONDecodeError:
            logging.error(f"Error parsing quotes file {self.quotes_file}")
            return self.get_default_quotes()
    
    def get_default_quotes(self):
        """Return default quotes if file loading fails"""
        return {
            "mental_health": [
                {"text": "You are not alone in this. Even when it feels like the world is against you, there are people who care.", "author": "Unknown"},
                {"text": "Healing isn't about erasing your past; it's about making peace with it.", "author": "Unknown"},
                {"text": "Your mental health is just as important as your physical health. Take care of both.", "author": "Unknown"},
                {"text": "It's okay to not be okay. What matters is that you're trying.", "author": "Unknown"},
                {"text": "You have survived 100% of your worst days. You're doing better than you think.", "author": "Unknown"}
            ],
            "motivation": [
                {"text": "The greatest revolution of our generation is the discovery that human beings can alter their lives by altering their attitudes.", "author": "William James"},
                {"text": "You don't have to be positive all the time. It's perfectly okay to feel sad, angry, annoyed, frustrated, scared, or anxious. Having feelings doesn't make you a negative person.", "author": "Lori Deschene"},
                {"text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson"},
                {"text": "The only person you are destined to become is the person you decide to be.", "author": "Ralph Waldo Emerson"},
                {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"}
            ],
            "self_care": [
                {"text": "Self-care is not selfish. You cannot serve from an empty vessel.", "author": "Eleanor Brown"},
                {"text": "Rest when you're weary. Refresh and renew yourself, your body, your mind, your spirit.", "author": "Ralph Marston"},
                {"text": "Taking care of yourself doesn't mean me first, it means me too.", "author": "L.R. Knost"},
                {"text": "You can't pour from an empty cup. Take care of yourself first.", "author": "Unknown"},
                {"text": "Be patient with yourself. Self-growth is tender; it's holy ground.", "author": "Unknown"}
            ]
        }
    
    def initialize_favorites(self):
        """Initialize favorites in session state"""
        if 'favorite_quotes' not in st.session_state:
            st.session_state.favorite_quotes = []
    
    def get_daily_quote(self):
        """Get quote of the day based on current date"""
        # Use date as seed for consistent daily quote
        today = date.today()
        random.seed(today.toordinal())
        
        # Get all quotes from all categories
        all_quotes = []
        for category in self.quotes.values():
            all_quotes.extend(category)
        
        if all_quotes:
            daily_quote = random.choice(all_quotes)
            # Reset random seed
            random.seed()
            return daily_quote
        
        return {"text": "Every day is a new opportunity to grow and heal.", "author": "MindMate"}
    
    def get_random_quote(self, category=None):
        """Get a random quote, optionally from specific category"""
        if category and category in self.quotes:
            quotes_pool = self.quotes[category]
        else:
            # Get all quotes from all categories
            quotes_pool = []
            for category_quotes in self.quotes.values():
                quotes_pool.extend(category_quotes)
        
        if quotes_pool:
            return random.choice(quotes_pool)
        
        return {"text": "You are stronger than you think and more capable than you imagine.", "author": "MindMate"}
    
    def add_to_favorites(self, quote):
        """Add quote to favorites"""
        if quote not in st.session_state.favorite_quotes:
            st.session_state.favorite_quotes.append(quote)
            return True
        return False
    
    def remove_from_favorites(self, quote):
        """Remove quote from favorites"""
        if quote in st.session_state.favorite_quotes:
            st.session_state.favorite_quotes.remove(quote)
            return True
        return False
    
    def get_favorites(self):
        """Get all favorite quotes"""
        return st.session_state.favorite_quotes
    
    def is_favorite(self, quote):
        """Check if quote is in favorites"""
        return quote in st.session_state.favorite_quotes
    
    def get_quote_categories(self):
        """Get all available quote categories"""
        return list(self.quotes.keys())
    
    def search_quotes(self, search_term):
        """Search quotes by text or author"""
        search_term = search_term.lower()
        results = []
        
        for category, quotes in self.quotes.items():
            for quote in quotes:
                if (search_term in quote['text'].lower() or 
                    search_term in quote['author'].lower()):
                    quote_with_category = quote.copy()
                    quote_with_category['category'] = category
                    results.append(quote_with_category)
        
        return results
