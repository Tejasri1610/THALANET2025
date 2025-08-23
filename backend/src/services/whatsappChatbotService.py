#!/usr/bin/env python3
"""
AI WhatsApp Chatbot Service for ThalaNet Emergency Blood Management Platform
Provides intelligent responses with patient matching, donation history, and donor suggestions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import re
import logging
from dataclasses import dataclass
import asyncio
import requests
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Data class for chat messages"""
    message_id: str
    sender_phone: str
    message_text: str
    timestamp: datetime
    message_type: str = 'text'  # text, image, location, etc.
    context: Dict = None

@dataclass
class ChatResponse:
    """Data class for chat responses"""
    response_id: str
    message_id: str
    response_text: str
    response_type: str = 'text'
    attachments: List[Dict] = None
    quick_replies: List[str] = None
    timestamp: datetime = None

class WhatsAppChatbotService:
    def __init__(self, config: Dict = None):
        """
        Initialize the WhatsApp chatbot service
        
        Args:
            config: Configuration dictionary with chatbot settings
        """
        self.config = config or self._get_default_config()
        self.conversation_history = {}
        self.user_profiles = {}
        self.response_templates = self._load_response_templates()
        
        # Load ML models and matching system
        self.donor_prediction_model = None
        self.matching_system = None
        
        # Initialize WhatsApp Business API client (mock for now)
        self.whatsapp_client = None
        
        logger.info("WhatsApp Chatbot Service initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'max_conversation_history': 50,
            'response_timeout_seconds': 30,
            'max_quick_replies': 4,
            'enable_ai_responses': True,
            'enable_patient_matching': True,
            'enable_donation_history': True,
            'enable_smart_suggestions': True,
            'language': 'en',
            'timezone': 'Asia/Kolkata'
        }
    
    def _load_response_templates(self) -> Dict:
        """Load response templates for different scenarios"""
        return {
            'greeting': [
                "Hello! Welcome to ThalaNet Blood Donation Service. How can I help you today?",
                "Hi there! I'm your ThalaNet blood donation assistant. What would you like to know?",
                "Welcome to ThalaNet! I'm here to help with blood donation queries and emergency requests."
            ],
            'donation_info': [
                "Blood donation is a safe and simple process that takes about 10-15 minutes. You can donate every 56 days.",
                "To donate blood, you must be 18-65 years old, weigh at least 50kg, and be in good health.",
                "Blood donation helps save up to 3 lives. The process is completely safe and sterile."
            ],
            'eligibility': [
                "You can donate if you're 18-65 years old, weigh at least 50kg, and haven't donated in the last 56 days.",
                "Temporary deferrals apply if you have cold/flu, recent surgery, or certain medications.",
                "Permanent deferrals apply for HIV/AIDS, Hepatitis B/C, or certain chronic conditions."
            ],
            'emergency_request': [
                "🚨 EMERGENCY BLOOD REQUEST DETECTED! 🚨\n\nI'll help you find the best matches immediately.",
                "URGENT: Blood request detected. Let me search for compatible donors in your area.",
                "⚠️ Emergency situation detected. I'm finding the closest compatible donors now."
            ],
            'no_matches': [
                "I couldn't find immediate matches in your area, but I'm expanding the search radius.",
                "No local matches found, but I'm checking nearby cities for compatible donors.",
                "Let me search a wider area to find suitable donors for this request."
            ],
            'donation_reminder': [
                "Friendly reminder: You're eligible to donate blood again! It's been over 56 days since your last donation.",
                "Great news! You can donate blood again. Would you like to schedule an appointment?",
                "You're due for another blood donation. Ready to save more lives?"
            ],
            'help': [
                "I can help you with:\n• Blood donation information\n• Emergency requests\n• Donation history\n• Finding donors\n• Scheduling appointments",
                "Available commands:\n• 'Donate blood' - Get donation info\n• 'Emergency' - Report urgent need\n• 'My history' - View donations\n• 'Find donor' - Search for matches",
                "Here's what I can do:\n• Answer donation questions\n• Process emergency requests\n• Show your donation history\n• Help find compatible donors"
            ],
            'error': [
                "I'm sorry, I couldn't process that request. Please try again or contact our support team.",
                "Something went wrong. Let me try to help you in a different way.",
                "I encountered an error. Please rephrase your request or contact support."
            ]
        }
    
    def process_message(self, message: ChatMessage, 
                       donors_df: pd.DataFrame = None,
                       patients_df: pd.DataFrame = None,
                       emergency_requests_df: pd.DataFrame = None) -> ChatResponse:
        """
        Process incoming WhatsApp message and generate appropriate response
        
        Args:
            message: Incoming chat message
            donors_df: DataFrame of donors (for matching)
            patients_df: DataFrame of patients (for matching)
            emergency_requests_df: DataFrame of emergency requests
            
        Returns:
            Chat response object
        """
        try:
            # Update conversation history
            self._update_conversation_history(message)
            
            # Analyze message intent
            intent = self._analyze_message_intent(message.message_text)
            
            # Generate response based on intent
            if intent == 'greeting':
                response = self._generate_greeting_response(message)
            elif intent == 'donation_info':
                response = self._generate_donation_info_response(message)
            elif intent == 'eligibility':
                response = self._generate_eligibility_response(message)
            elif intent == 'emergency_request':
                response = self._generate_emergency_response(message, donors_df, emergency_requests_df)
            elif intent == 'donation_history':
                response = self._generate_history_response(message, donors_df)
            elif intent == 'find_donor':
                response = self._generate_donor_search_response(message, donors_df, patients_df)
            elif intent == 'help':
                response = self._generate_help_response(message)
            else:
                response = self._generate_generic_response(message)
            
            # Add quick replies if appropriate
            response.quick_replies = self._generate_quick_replies(intent)
            
            # Update timestamp
            response.timestamp = datetime.now()
            
            # Store response in conversation history
            self._store_response(message.sender_phone, response)
            
            logger.info(f"Generated response for message {message.message_id}: {intent}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")
            return self._generate_error_response(message)
    
    def _analyze_message_intent(self, message_text: str) -> str:
        """
        Analyze message text to determine user intent
        
        Args:
            message_text: Text content of the message
            
        Returns:
            Intent category string
        """
        message_lower = message_text.lower().strip()
        
        # Greeting patterns
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return 'greeting'
        
        # Donation information patterns
        if any(word in message_lower for word in ['donate', 'donation', 'blood donation', 'how to donate', 'process']):
            return 'donation_info'
        
        # Eligibility patterns
        if any(word in message_lower for word in ['eligible', 'can i donate', 'requirements', 'age', 'weight', 'health']):
            return 'eligibility'
        
        # Emergency request patterns
        if any(word in message_lower for word in ['emergency', 'urgent', 'need blood', 'critical', 'help', 'sos']):
            return 'emergency_request'
        
        # Donation history patterns
        if any(word in message_lower for word in ['history', 'my donations', 'last donation', 'when can i donate again']):
            return 'donation_history'
        
        # Donor search patterns
        if any(word in message_lower for word in ['find donor', 'search', 'match', 'compatible', 'need donor']):
            return 'find_donor'
        
        # Help patterns
        if any(word in message_lower for word in ['help', 'what can you do', 'commands', 'options']):
            return 'help'
        
        return 'unknown'
    
    def _generate_greeting_response(self, message: ChatMessage) -> ChatResponse:
        """Generate greeting response"""
        greeting = np.random.choice(self.response_templates['greeting'])
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=greeting
        )
    
    def _generate_donation_info_response(self, message: ChatMessage) -> ChatResponse:
        """Generate donation information response"""
        info = np.random.choice(self.response_templates['donation_info'])
        
        response_text = f"{info}\n\nWould you like to know about eligibility requirements or schedule a donation?"
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_eligibility_response(self, message: ChatMessage) -> ChatResponse:
        """Generate eligibility information response"""
        eligibility = np.random.choice(self.response_templates['eligibility'])
        
        response_text = f"{eligibility}\n\nWould you like me to check if you're eligible based on your profile?"
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_emergency_response(self, message: ChatMessage, 
                                   donors_df: pd.DataFrame,
                                   emergency_requests_df: pd.DataFrame) -> ChatResponse:
        """Generate emergency response with donor matching"""
        emergency_msg = np.random.choice(self.response_templates['emergency_request'])
        
        # Check for recent emergency requests
        recent_emergencies = self._find_recent_emergencies(message.sender_phone, emergency_requests_df)
        
        if recent_emergencies:
            response_text = f"{emergency_msg}\n\nI found {len(recent_emergencies)} recent emergency requests in your area."
            
            # Add emergency details
            for i, emergency in enumerate(recent_emergencies[:3], 1):
                response_text += f"\n\n{i}. {emergency['blood_type_needed']} blood needed at {emergency['hospital_name']}"
                response_text += f"\n   Urgency: {emergency['urgency_level']}"
                response_text += f"\n   Contact: {emergency['contact_person']} - {emergency['contact_number']}"
        else:
            response_text = f"{emergency_msg}\n\nI don't see any recent emergency requests from your number. Would you like to report a new emergency?"
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_history_response(self, message: ChatMessage, donors_df: pd.DataFrame) -> ChatResponse:
        """Generate donation history response"""
        # Find donor profile
        donor_profile = self._find_donor_profile(message.sender_phone, donors_df)
        
        if donor_profile:
            last_donation = donor_profile.get('last_donation_date', 'Unknown')
            total_donations = donor_profile.get('donation_frequency', 0)
            
            response_text = f"📊 Your Donation History:\n\n"
            response_text += f"Last Donation: {last_donation}\n"
            response_text += f"Total Donations: {total_donations}\n"
            response_text += f"Blood Type: {donor_profile.get('blood_type', 'Unknown')}\n"
            response_text += f"Status: {donor_profile.get('availability_status', 'Unknown')}"
            
            # Check if eligible to donate again
            if last_donation != 'Unknown':
                try:
                    last_date = pd.to_datetime(last_donation)
                    days_since = (datetime.now() - last_date).days
                    
                    if days_since >= 56:
                        response_text += f"\n\n✅ You're eligible to donate again!"
                    else:
                        days_remaining = 56 - days_since
                        response_text += f"\n\n⏳ You can donate again in {days_remaining} days"
                except:
                    pass
        else:
            response_text = "I couldn't find your donation history. Are you a registered donor? You can register by providing your details."
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_donor_search_response(self, message: ChatMessage, 
                                      donors_df: pd.DataFrame,
                                      patients_df: pd.DataFrame) -> ChatResponse:
        """Generate donor search response with smart suggestions"""
        response_text = "🔍 Donor Search Results:\n\n"
        
        # Extract blood type from message if mentioned
        blood_type = self._extract_blood_type(message.message_text)
        
        if blood_type:
            # Find compatible donors
            compatible_donors = self._find_compatible_donors(blood_type, donors_df)
            
            if compatible_donors:
                response_text += f"Found {len(compatible_donors)} compatible {blood_type} donors:\n\n"
                
                for i, donor in enumerate(compatible_donors[:5], 1):
                    response_text += f"{i}. {donor['name']} - {donor['location']}\n"
                    response_text += f"   Availability: {donor['availability_status']}\n"
                    response_text += f"   Last Donation: {donor['last_donation_date']}\n\n"
            else:
                response_text += f"No available {blood_type} donors found in your area.\n\n"
                response_text += "I'll expand the search to nearby cities."
        else:
            response_text += "Please specify the blood type you're looking for (e.g., 'Find A+ donor' or 'Need O- blood')."
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_help_response(self, message: ChatMessage) -> ChatResponse:
        """Generate help response"""
        help_text = np.random.choice(self.response_templates['help'])
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=help_text
        )
    
    def _generate_generic_response(self, message: ChatMessage) -> ChatResponse:
        """Generate generic response for unknown intent"""
        response_text = "I'm here to help with blood donation queries and emergency requests. "
        response_text += "You can ask me about:\n• Donation process\n• Eligibility\n• Emergency requests\n• Your donation history\n• Finding donors"
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=response_text
        )
    
    def _generate_error_response(self, message: ChatMessage) -> ChatResponse:
        """Generate error response"""
        error_msg = np.random.choice(self.response_templates['error'])
        
        return ChatResponse(
            response_id=f"RESP_{len(self.conversation_history.get(message.sender_phone, [])) + 1:06d}",
            message_id=message.message_id,
            response_text=error_msg
        )
    
    def _generate_quick_replies(self, intent: str) -> List[str]:
        """Generate quick reply options based on intent"""
        quick_replies = {
            'greeting': ['Donate Blood', 'Emergency Help', 'My History', 'Find Donor'],
            'donation_info': ['Eligibility', 'Schedule Donation', 'Donation Centers', 'Back to Menu'],
            'eligibility': ['Check My Status', 'Requirements', 'Schedule Donation', 'Back to Menu'],
            'emergency_request': ['Report Emergency', 'Find Donors', 'Contact Hospital', 'Back to Menu'],
            'donation_history': ['Schedule Next Donation', 'Update Profile', 'Find Centers', 'Back to Menu'],
            'find_donor': ['Search by Blood Type', 'Search by Location', 'Emergency Search', 'Back to Menu'],
            'help': ['Donation Info', 'Emergency Help', 'My Profile', 'Contact Support']
        }
        
        return quick_replies.get(intent, ['Help', 'Emergency', 'Donate', 'Back to Menu'])[:self.config['max_quick_replies']]
    
    def _update_conversation_history(self, message: ChatMessage):
        """Update conversation history for a user"""
        if message.sender_phone not in self.conversation_history:
            self.conversation_history[message.sender_phone] = []
        
        # Add message to history
        self.conversation_history[message.sender_phone].append({
            'message_id': message.message_id,
            'text': message.message_text,
            'timestamp': message.timestamp.isoformat(),
            'type': 'user'
        })
        
        # Limit history size
        if len(self.conversation_history[message.sender_phone]) > self.config['max_conversation_history']:
            self.conversation_history[message.sender_phone] = self.conversation_history[message.sender_phone][-self.config['max_conversation_history']:]
    
    def _store_response(self, sender_phone: str, response: ChatResponse):
        """Store bot response in conversation history"""
        if sender_phone in self.conversation_history:
            self.conversation_history[sender_phone].append({
                'response_id': response.response_id,
                'text': response.response_text,
                'timestamp': response.timestamp.isoformat(),
                'type': 'bot',
                'quick_replies': response.quick_replies
            })
    
    def _find_recent_emergencies(self, phone: str, emergency_requests_df: pd.DataFrame) -> List[Dict]:
        """Find recent emergency requests"""
        if emergency_requests_df is None:
            return []
        
        # Look for emergencies in the last 24 hours
        current_time = datetime.now()
        recent_emergencies = []
        
        for _, emergency in emergency_requests_df.iterrows():
            try:
                emergency_time = pd.to_datetime(emergency['timestamp'])
                if (current_time - emergency_time).total_seconds() <= 86400:  # 24 hours
                    recent_emergencies.append(emergency.to_dict())
            except:
                continue
        
        return recent_emergencies
    
    def _find_donor_profile(self, phone: str, donors_df: pd.DataFrame) -> Optional[Dict]:
        """Find donor profile by phone number"""
        if donors_df is None:
            return None
        
        # Clean phone number for matching
        clean_phone = self._clean_phone_number(phone)
        
        for _, donor in donors_df.iterrows():
            donor_phone = self._clean_phone_number(donor.get('contact_number', ''))
            if clean_phone in donor_phone or donor_phone in clean_phone:
                return donor.to_dict()
        
        return None
    
    def _find_compatible_donors(self, blood_type: str, donors_df: pd.DataFrame) -> List[Dict]:
        """Find compatible donors for a blood type"""
        if donors_df is None:
            return []
        
        # Blood type compatibility matrix
        compatibility = {
            'O-': ['O-'],
            'O+': ['O+', 'O-'],
            'A-': ['A-', 'O-'],
            'A+': ['A+', 'A-', 'O+', 'O-'],
            'B-': ['B-', 'O-'],
            'B+': ['B+', 'B-', 'O+', 'O-'],
            'AB-': ['AB-', 'A-', 'B-', 'O-'],
            'AB+': ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']
        }
        
        compatible_types = compatibility.get(blood_type, [])
        compatible_donors = []
        
        for _, donor in donors_df.iterrows():
            if (donor['blood_type'] in compatible_types and 
                donor['availability_status'] == 'Available' and
                donor['health_conditions'] == 'None'):
                compatible_donors.append(donor.to_dict())
        
        # Sort by last donation date (most recent first)
        compatible_donors.sort(key=lambda x: x.get('last_donation_date', ''), reverse=True)
        
        return compatible_donors[:10]
    
    def _extract_blood_type(self, message: str) -> Optional[str]:
        """Extract blood type from message text"""
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        
        for blood_type in blood_types:
            if blood_type.lower() in message.lower():
                return blood_type
        
        return None
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean phone number for matching"""
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', phone)
        
        # Remove country code if present
        if cleaned.startswith('91') and len(cleaned) > 10:
            cleaned = cleaned[2:]
        
        return cleaned
    
    def get_conversation_summary(self, phone: str) -> Dict:
        """Get conversation summary for a user"""
        if phone not in self.conversation_history:
            return {'message_count': 0, 'last_message': None, 'topics': []}
        
        history = self.conversation_history[phone]
        
        # Analyze topics
        topics = []
        for item in history:
            if item['type'] == 'user':
                intent = self._analyze_message_intent(item['text'])
                topics.append(intent)
        
        return {
            'message_count': len(history),
            'last_message': history[-1]['timestamp'] if history else None,
            'topics': topics[-5:],  # Last 5 topics
            'user_messages': len([h for h in history if h['type'] == 'user']),
            'bot_responses': len([h for h in history if h['type'] == 'bot'])
        }
    
    def save_conversation_data(self, output_file: str = "whatsapp_conversations.json"):
        """Save conversation data to JSON file"""
        data = {
            'conversations': self.conversation_history,
            'user_profiles': self.user_profiles,
            'statistics': {
                'total_users': len(self.conversation_history),
                'total_messages': sum(len(conv) for conv in self.conversation_history.values()),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Conversation data saved to {output_file}")

def main():
    """Example usage of the WhatsApp chatbot service"""
    print("WhatsApp Chatbot Service")
    print("=" * 50)
    
    try:
        # Load datasets
        donors_df = pd.read_csv("data/donors.csv")
        patients_df = pd.read_csv("data/patients.csv")
        emergency_requests_df = pd.read_csv("data/emergency_requests.csv")
        
        # Initialize chatbot service
        chatbot = WhatsAppChatbotService()
        
        # Example conversation
        test_messages = [
            ChatMessage("MSG_001", "+91-9876543210", "Hello", datetime.now()),
            ChatMessage("MSG_002", "+91-9876543210", "I want to donate blood", datetime.now()),
            ChatMessage("MSG_003", "+91-9876543210", "Emergency! Need A+ blood", datetime.now()),
            ChatMessage("MSG_004", "+91-9876543210", "Show my donation history", datetime.now())
        ]
        
        print("Processing test messages...")
        
        for message in test_messages:
            print(f"\nUser: {message.message_text}")
            
            response = chatbot.process_message(
                message, donors_df, patients_df, emergency_requests_df
            )
            
            print(f"Bot: {response.response_text}")
            if response.quick_replies:
                print(f"Quick Replies: {', '.join(response.quick_replies)}")
        
        # Get conversation summary
        summary = chatbot.get_conversation_summary("+91-9876543210")
        print(f"\nConversation Summary: {summary}")
        
        # Save data
        chatbot.save_conversation_data()
        
    except FileNotFoundError:
        print("Data files not found. Please run the synthetic data generator first.")
        print("Run: python src/utils/syntheticDataGenerator.py")

if __name__ == "__main__":
    main()

