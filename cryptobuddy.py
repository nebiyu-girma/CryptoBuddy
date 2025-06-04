"""
CryptoBuddy - AI-Powered Cryptocurrency Advisor Chatbot
=======================================================
A rule-based chatbot that provides investment advice based on profitability and sustainability.

Author: Nebiyu Girma
Version: 1.0
"""

import re
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any


class CryptoBuddy:
    """
    A rule-based cryptocurrency advisor chatbot that analyzes crypto data
    and provides investment advice based on profitability and sustainability.
    """
    
    def __init__(self):
        self.name = "CryptoBuddy"
        self.version = "1.0"
        self.crypto_db = self._initialize_crypto_database()
        self.conversation_history = []
        self.greeting_responses = [
            "Hey there! 🚀 Ready to explore the crypto universe?",
            "Welcome to CryptoBuddy! Let's find you some profitable and sustainable crypto gems! 💎",
            "Hi! I'm your crypto sidekick - ask me about trends, sustainability, or investment advice! 🌟"
        ]
        
    def _initialize_crypto_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize the cryptocurrency database with sample data."""
        return {
            "Bitcoin": {
                "symbol": "BTC",
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3,
                "max_score": 10,
                "current_price": 67500.00,
                "market_cap_usd": 1300000000000,
                "description": "The original cryptocurrency and digital gold standard"
            },
            "Ethereum": {
                "symbol": "ETH",
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6,
                "max_score": 10,
                "current_price": 3800.00,
                "market_cap_usd": 456000000000,
                "description": "Smart contract platform powering DeFi and NFTs"
            },
            "Cardano": {
                "symbol": "ADA",
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8,
                "max_score": 10,
                "current_price": 0.65,
                "market_cap_usd": 23000000000,
                "description": "Proof-of-stake blockchain focused on sustainability and academic research"
            },
            "Solana": {
                "symbol": "SOL",
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 7,
                "max_score": 10,
                "current_price": 145.00,
                "market_cap_usd": 68000000000,
                "description": "High-performance blockchain for decentralized apps and DeFi"
            },
            "Polygon": {
                "symbol": "MATIC",
                "price_trend": "stable",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 9,
                "max_score": 10,
                "current_price": 0.85,
                "market_cap_usd": 8500000000,
                "description": "Ethereum scaling solution with carbon-negative commitment"
            }
        }
    
    def greet(self) -> str:
        """Return a friendly greeting message."""
        return random.choice(self.greeting_responses)
    
    def _normalize_query(self, query: str) -> str:
        """Normalize user query for better matching."""
        return query.lower().strip()
    
    def _extract_crypto_mentions(self, query: str) -> List[str]:
        """Extract cryptocurrency names mentioned in the query."""
        mentioned_cryptos = []
        normalized_query = self._normalize_query(query)
        
        for crypto_name in self.crypto_db.keys():
            if crypto_name.lower() in normalized_query:
                mentioned_cryptos.append(crypto_name)
        
        # Also check for symbols
        for crypto_name, data in self.crypto_db.items():
            if data["symbol"].lower() in normalized_query:
                mentioned_cryptos.append(crypto_name)
                
        return list(set(mentioned_cryptos))  # Remove duplicates
    
    def get_most_profitable(self) -> Tuple[str, Dict]:
        """Find the most profitable cryptocurrency based on trends and market cap."""
        profitable_cryptos = []
        
        for name, data in self.crypto_db.items():
            score = 0
            # Rising trend gets higher score
            if data["price_trend"] == "rising":
                score += 3
            elif data["price_trend"] == "stable":
                score += 1
            
            # High market cap gets higher score (more established)
            if data["market_cap"] == "high":
                score += 2
            elif data["market_cap"] == "medium":
                score += 1
                
            profitable_cryptos.append((name, data, score))
        
        # Sort by score (descending)
        profitable_cryptos.sort(key=lambda x: x[2], reverse=True)
        return profitable_cryptos[0][0], profitable_cryptos[0][1]
    
    def get_most_sustainable(self) -> Tuple[str, Dict]:
        """Find the most sustainable cryptocurrency."""
        best_crypto = max(
            self.crypto_db.items(),
            key=lambda x: x[1]["sustainability_score"]
        )
        return best_crypto[0], best_crypto[1]
    
    def get_balanced_recommendation(self) -> Tuple[str, Dict]:
        """Get a balanced recommendation considering both profitability and sustainability."""
        balanced_scores = []
        
        for name, data in self.crypto_db.items():
            # Calculate profitability score
            profit_score = 0
            if data["price_trend"] == "rising":
                profit_score += 3
            elif data["price_trend"] == "stable":
                profit_score += 1
            
            if data["market_cap"] == "high":
                profit_score += 2
            elif data["market_cap"] == "medium":
                profit_score += 1
            
            # Normalize sustainability score (0-10 to 0-5 scale)
            sustainability_normalized = (data["sustainability_score"] / data["max_score"]) * 5
            
            # Combined score (equal weight)
            total_score = (profit_score + sustainability_normalized) / 2
            balanced_scores.append((name, data, total_score))
        
        balanced_scores.sort(key=lambda x: x[2], reverse=True)
        return balanced_scores[0][0], balanced_scores[0][1]
    
    def get_crypto_info(self, crypto_name: str) -> str:
        """Get detailed information about a specific cryptocurrency."""
        if crypto_name not in self.crypto_db:
            return f"Sorry, I don't have information about {crypto_name} in my database."
        
        data = self.crypto_db[crypto_name]
        sustainability_percentage = (data["sustainability_score"] / data["max_score"]) * 100
        
        return f"""
🪙 **{crypto_name} ({data['symbol']})** 
💰 Current Price: ${data['current_price']:,.2f}
📈 Price Trend: {data['price_trend'].title()}
🏛️ Market Cap: {data['market_cap'].title()} (${data['market_cap_usd']:,.0f})
🌱 Sustainability Score: {data['sustainability_score']}/10 ({sustainability_percentage:.0f}%)
⚡ Energy Use: {data['energy_use'].title()}
📝 Description: {data['description']}
        """.strip()
    
    def analyze_query(self, user_query: str) -> str:
        """Analyze user query and provide appropriate response."""
        normalized_query = self._normalize_query(user_query)
        mentioned_cryptos = self._extract_crypto_mentions(user_query)
        
        # Store conversation
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user_query": user_query,
            "mentioned_cryptos": mentioned_cryptos
        })
        
        # Handle specific crypto information requests
        if mentioned_cryptos and any(word in normalized_query for word in ["info", "about", "tell me", "details"]):
            return self.get_crypto_info(mentioned_cryptos[0])
        
        # Handle sustainability queries
        if any(word in normalized_query for word in ["sustainable", "green", "eco", "environment", "energy"]):
            crypto_name, data = self.get_most_sustainable()
            sustainability_percentage = (data["sustainability_score"] / data["max_score"]) * 100
            return f"""
🌱 **Most Sustainable Choice: {crypto_name} ({data['symbol']})**

{crypto_name} leads in sustainability with a {data['sustainability_score']}/10 score ({sustainability_percentage:.0f}%)! 
It uses {data['energy_use']} energy and is currently {data['price_trend']}. 

Perfect for eco-conscious investors! 🌍✨
            """.strip()
        
        # Handle profitability queries
        if any(word in normalized_query for word in ["profitable", "profit", "money", "gains", "rising", "trending"]):
            crypto_name, data = self.get_most_profitable()
            return f"""
🚀 **Most Profitable Choice: {crypto_name} ({data['symbol']})**

{crypto_name} is trending {data['price_trend']} with a {data['market_cap']} market cap! 
Current price: ${data['current_price']:,.2f}

Great for profit-focused investors! 💰📈
            """.strip()
        
        # Handle balanced/general investment advice
        if any(word in normalized_query for word in ["invest", "buy", "recommend", "advice", "best", "should"]):
            crypto_name, data = self.get_balanced_recommendation()
            sustainability_percentage = (data["sustainability_score"] / data["max_score"]) * 100
            return f"""
⭐ **Balanced Recommendation: {crypto_name} ({data['symbol']})**

{crypto_name} offers the best balance of profitability and sustainability!

📊 **Quick Stats:**
• Price: ${data['current_price']:,.2f} ({data['price_trend']} trend)
• Sustainability: {data['sustainability_score']}/10 ({sustainability_percentage:.0f}%)
• Market Position: {data['market_cap'].title()} cap

{data['description']} 

⚠️ **Disclaimer**: Crypto investments are risky—always do your own research!
            """.strip()
        
        # Handle comparison queries
        if "compare" in normalized_query or "vs" in normalized_query:
            return self._compare_cryptos()
        
        # Handle listing queries
        if any(word in normalized_query for word in ["list", "all", "show me", "available"]):
            return self._list_all_cryptos()
        
        # Default response for unclear queries
        return """
🤔 I didn't quite understand that! Here's what I can help you with:

💡 **Try asking:**
• "What's the most profitable crypto?"
• "Which crypto is most sustainable?"
• "What should I invest in?"
• "Tell me about Bitcoin"
• "Compare all cryptos"
• "List all available cryptos"

I'm here to help you make informed crypto decisions! 🚀
        """.strip()
    
    def _compare_cryptos(self) -> str:
        """Compare all cryptocurrencies in the database."""
        comparison = "📊 **Crypto Comparison Overview**\n\n"
        
        for name, data in self.crypto_db.items():
            sustainability_percentage = (data["sustainability_score"] / data["max_score"]) * 100
            trend_emoji = "📈" if data["price_trend"] == "rising" else "📊"
            
            comparison += f"""
{trend_emoji} **{name} ({data['symbol']})**
Price: ${data['current_price']:,.2f} | Trend: {data['price_trend'].title()}
Sustainability: {sustainability_percentage:.0f}% | Energy: {data['energy_use'].title()}
            """.strip() + "\n\n"
        
        comparison += "💡 **Need specific advice?** Ask me for profitability, sustainability, or investment recommendations!"
        return comparison
    
    def _list_all_cryptos(self) -> str:
        """List all available cryptocurrencies."""
        crypto_list = "🪙 **Available Cryptocurrencies:**\n\n"
        
        for name, data in self.crypto_db.items():
            crypto_list += f"• {name} ({data['symbol']}) - ${data['current_price']:,.2f}\n"
        
        crypto_list += "\n💬 Ask me about any of these cryptos for detailed analysis!"
        return crypto_list
    
    def get_disclaimer(self) -> str:
        """Return investment disclaimer."""
        return """
⚠️ **Investment Disclaimer**
This chatbot provides educational information only. Cryptocurrency investments carry significant risks including total loss of capital. Past performance doesn't guarantee future results. Always conduct thorough research and consider consulting with financial advisors before making investment decisions.
        """.strip()
    
    def chat(self):
        """Main chat interface for interactive conversation."""
        print("=" * 60)
        print(f"🤖 Welcome to {self.name} v{self.version}")
        print("=" * 60)
        print(self.greet())
        print("\n💡 Type 'help' for commands, 'disclaimer' for legal info, or 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.name}: Thanks for chatting! Happy investing! 🚀💰")
                    break
                
                if user_input.lower() == 'help':
                    print(f"\n{self.name}: {self.analyze_query('help')}\n")
                    continue
                
                if user_input.lower() == 'disclaimer':
                    print(f"\n{self.name}: {self.get_disclaimer()}\n")
                    continue
                
                response = self.analyze_query(user_input)
                print(f"\n{self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n{self.name}: Oops! Something went wrong: {str(e)}")
                print("Let's try again! 🔄\n")


def main():
    """Main function to run the CryptoBuddy chatbot."""
    bot = CryptoBuddy()
    
    
    bot.chat()
    
    # Test mode - demonstrate functionality
    print("🧪 **CryptoBuddy Demo Mode**\n")
    
    test_queries = [
        "Hello!",
        "What's the most sustainable crypto?",
        "Which crypto is most profitable?",
        "What should I invest in?",
        "Tell me about Bitcoin",
        "Compare all cryptos",
        "List available cryptos"
    ]
    
    bot_instance = CryptoBuddy()
    print(bot_instance.greet())
    print("\n" + "=" * 50)
    
    for query in test_queries:
        print(f"\n🗣️ **User**: {query}")
        print(f"🤖 **CryptoBuddy**: {bot_instance.analyze_query(query)}")
        print("\n" + "-" * 30)
    
    print(f"\n{bot_instance.get_disclaimer()}")
    
    print("\n" + "=" * 50)
    print("🚀 **To run interactive mode, uncomment bot.chat() in main() function**")


if __name__ == "__main__":
    main()