#!/usr/bin/env python3
"""
Emergency Notification Service for ThalaNet Emergency Blood Management Platform
Detects emergency requests and sends instant alerts with location-based matching
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import asyncio
import logging
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmergencyAlert:
    """Data class for emergency alerts"""
    alert_id: str
    request_id: str
    blood_type_needed: str
    urgency_level: str
    location: str
    latitude: float
    longitude: float
    units_required: int
    hospital_name: str
    contact_person: str
    contact_number: str
    timestamp: datetime
    status: str = 'active'
    matched_donors: List[Dict] = None
    notification_sent: bool = False

class EmergencyNotificationService:
    def __init__(self, config: Dict = None):
        """
        Initialize the emergency notification service
        
        Args:
            config: Configuration dictionary with notification settings
        """
        self.config = config or self._get_default_config()
        self.active_alerts = {}
        self.alert_history = []
        self.notification_queue = []
        
        # Load ML models and matching system
        self.donor_prediction_model = None
        self.matching_system = None
        
        # Initialize notification channels
        self.notification_channels = {
            'email': self._send_email_notification,
            'sms': self._send_sms_notification,
            'whatsapp': self._send_whatsapp_notification,
            'push': self._send_push_notification
        }
        
        logger.info("Emergency Notification Service initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'check_interval_seconds': 30,
            'max_alerts_per_hour': 50,
            'notification_channels': ['email', 'sms'],
            'max_distance_km': 100,
            'min_matching_score': 50,
            'alert_expiry_hours': 24,
            'batch_notification_size': 10
        }
    
    def detect_emergency_requests(self, emergency_requests_df: pd.DataFrame) -> List[EmergencyAlert]:
        """
        Detect new emergency requests that need immediate attention
        
        Args:
            emergency_requests_df: DataFrame of emergency requests
            
        Returns:
            List of new emergency alerts
        """
        new_alerts = []
        current_time = datetime.now()
        
        for _, request in emergency_requests_df.iterrows():
            request_id = request['request_id']
            
            # Skip if already processed
            if request_id in self.active_alerts:
                continue
            
            # Check if request is recent and urgent
            request_time = pd.to_datetime(request['timestamp'])
            time_diff = current_time - request_time
            
            # Only process recent requests (within last hour)
            if time_diff.total_seconds() > 3600:
                continue
            
            # Check urgency level
            urgency = request.get('urgency_level', 'MEDIUM')
            if urgency in ['HIGH', 'CRITICAL']:
                # Create emergency alert
                alert = EmergencyAlert(
                    alert_id=f"ALERT_{len(self.active_alerts) + 1:06d}",
                    request_id=request_id,
                    blood_type_needed=request['blood_type_needed'],
                    urgency_level=urgency,
                    location=request['location'],
                    latitude=request.get('latitude', 0),
                    longitude=request.get('longitude', 0),
                    units_required=request.get('units_required', 1),
                    hospital_name=request.get('hospital_name', 'Unknown'),
                    contact_person=request.get('contact_person', 'Unknown'),
                    contact_number=request.get('contact_number', 'Unknown'),
                    timestamp=request_time
                )
                
                new_alerts.append(alert)
                self.active_alerts[request_id] = alert
                
                logger.info(f"New emergency alert created: {alert.alert_id} for {urgency} urgency")
        
        return new_alerts
    
    def find_matching_donors_for_alert(self, alert: EmergencyAlert, donors_df: pd.DataFrame) -> List[Dict]:
        """
        Find matching donors for an emergency alert
        
        Args:
            alert: Emergency alert object
            donors_df: DataFrame of available donors
            
        Returns:
            List of matching donors with scores
        """
        if self.matching_system is None:
            # Simple matching if ML system not available
            return self._simple_donor_matching(alert, donors_df)
        
        # Use ML-based matching system
        try:
            matches = self.matching_system.find_emergency_matches({
                'blood_type_needed': alert.blood_type_needed,
                'urgency_level': alert.urgency_level,
                'latitude': alert.latitude,
                'longitude': alert.longitude,
                'location': alert.location
            }, donors_df)
            
            return matches.get('immediate_contact', []) + matches.get('high_priority', [])
        
        except Exception as e:
            logger.error(f"Error in ML matching: {e}")
            return self._simple_donor_matching(alert, donors_df)
    
    def _simple_donor_matching(self, alert: EmergencyAlert, donors_df: pd.DataFrame) -> List[Dict]:
        """Simple donor matching when ML system is not available"""
        matches = []
        
        # Filter compatible donors
        compatible_donors = donors_df[
            (donors_df['blood_type'] == alert.blood_type_needed) &
            (donors_df['availability_status'] == 'Available') &
            (donors_df['health_conditions'] == 'None')
        ].copy()
        
        if len(compatible_donors) == 0:
            return matches
        
        # Calculate distance and score for each donor
        for _, donor in compatible_donors.iterrows():
            distance = self._calculate_distance(
                alert.latitude, alert.longitude,
                donor.get('latitude', 0), donor.get('longitude', 0)
            )
            
            if distance <= self.config['max_distance_km']:
                # Simple scoring
                score = 100 - (distance / self.config['max_distance_km']) * 50
                
                match = {
                    'donor_id': donor['donor_id'],
                    'donor_name': donor['name'],
                    'blood_type': donor['blood_type'],
                    'location': donor['location'],
                    'distance_km': round(distance, 2),
                    'matching_score': round(score, 2),
                    'contact_number': donor.get('contact_number', 'Unknown'),
                    'responsiveness_score': donor.get('responsiveness_score', 0.5)
                }
                matches.append(match)
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x['matching_score'], reverse=True)
        return matches[:10]
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates"""
        try:
            from geopy.distance import geodesic
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers
        except ImportError:
            # Simple distance calculation
            return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
    
    def generate_alert_message(self, alert: EmergencyAlert, matched_donors: List[Dict]) -> str:
        """
        Generate notification message for emergency alert
        
        Args:
            alert: Emergency alert object
            matched_donors: List of matched donors
            
        Returns:
            Formatted notification message
        """
        message = f"""
🚨 EMERGENCY BLOOD REQUEST 🚨

Blood Type: {alert.blood_type_needed}
Urgency: {alert.urgency_level}
Location: {alert.location}
Hospital: {alert.hospital_name}
Units Required: {alert.units_required}
Contact: {alert.contact_person} - {alert.contact_number}

⏰ URGENT: Required within {self._get_urgency_timeframe(alert.urgency_level)}

🔍 MATCHING DONORS FOUND: {len(matched_donors)}

Top Matches:
"""
        
        for i, donor in enumerate(matched_donors[:5], 1):
            message += f"{i}. {donor['donor_name']} - {donor['distance_km']} km away\n"
            message += f"   Score: {donor['matching_score']} | Contact: {donor['contact_number']}\n\n"
        
        message += f"""
📱 Alert ID: {alert.alert_id}
🕐 Generated: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Please contact the hospital immediately if you can donate!
        """
        
        return message.strip()
    
    def _get_urgency_timeframe(self, urgency_level: str) -> str:
        """Get timeframe description for urgency level"""
        timeframes = {
            'LOW': '7-30 days',
            'MEDIUM': '3-7 days',
            'HIGH': '1-3 days',
            'CRITICAL': '1-24 hours'
        }
        return timeframes.get(urgency_level, 'Unknown')
    
    async def send_emergency_notifications(self, alert: EmergencyAlert, matched_donors: List[Dict]):
        """
        Send emergency notifications through configured channels
        
        Args:
            alert: Emergency alert object
            matched_donors: List of matched donors
        """
        if not matched_donors:
            logger.warning(f"No matched donors for alert {alert.alert_id}")
            return
        
        # Generate message
        message = self.generate_alert_message(alert, matched_donors)
        
        # Send notifications through configured channels
        notification_tasks = []
        
        for channel in self.config['notification_channels']:
            if channel in self.notification_channels:
                task = asyncio.create_task(
                    self._send_notification_async(channel, message, alert, matched_donors)
                )
                notification_tasks.append(task)
        
        # Wait for all notifications to complete
        if notification_tasks:
            await asyncio.gather(*notification_tasks, return_exceptions=True)
        
        # Mark alert as notified
        alert.notification_sent = True
        alert.matched_donors = matched_donors
        
        logger.info(f"Emergency notifications sent for alert {alert.alert_id}")
    
    async def _send_notification_async(self, channel: str, message: str, alert: EmergencyAlert, matched_donors: List[Dict]):
        """Send notification asynchronously"""
        try:
            result = await self.notification_channels[channel](message, alert, matched_donors)
            logger.info(f"Notification sent via {channel}: {result}")
        except Exception as e:
            logger.error(f"Error sending notification via {channel}: {e}")
    
    def _send_email_notification(self, message: str, alert: EmergencyAlert, matched_donors: List[Dict]) -> bool:
        """Send email notification"""
        try:
            # This would integrate with your email service (SendGrid, AWS SES, etc.)
            # For now, just log the email
            logger.info(f"EMAIL NOTIFICATION SENT:\n{message}")
            return True
        except Exception as e:
            logger.error(f"Email notification failed: {e}")
            return False
    
    def _send_sms_notification(self, message: str, alert: EmergencyAlert, matched_donors: List[Dict]) -> bool:
        """Send SMS notification"""
        try:
            # This would integrate with SMS service (Twilio, AWS SNS, etc.)
            # For now, just log the SMS
            logger.info(f"SMS NOTIFICATION SENT:\n{message}")
            return True
        except Exception as e:
            logger.error(f"SMS notification failed: {e}")
            return False
    
    def _send_whatsapp_notification(self, message: str, alert: EmergencyAlert, matched_donors: List[Dict]) -> bool:
        """Send WhatsApp notification"""
        try:
            # This would integrate with WhatsApp Business API
            # For now, just log the WhatsApp message
            logger.info(f"WHATSAPP NOTIFICATION SENT:\n{message}")
            return True
        except Exception as e:
            logger.error(f"WhatsApp notification failed: {e}")
            return False
    
    def _send_push_notification(self, message: str, alert: EmergencyAlert, matched_donors: List[Dict]) -> bool:
        """Send push notification"""
        try:
            # This would integrate with push notification service (Firebase, etc.)
            # For now, just log the push notification
            logger.info(f"PUSH NOTIFICATION SENT:\n{message}")
            return True
        except Exception as e:
            logger.error(f"Push notification failed: {e}")
            return False
    
    def process_emergency_requests(self, emergency_requests_df: pd.DataFrame, donors_df: pd.DataFrame):
        """
        Main method to process emergency requests and send notifications
        
        Args:
            emergency_requests_df: DataFrame of emergency requests
            donors_df: DataFrame of available donors
        """
        logger.info("Processing emergency requests...")
        
        # Detect new emergency requests
        new_alerts = self.detect_emergency_requests(emergency_requests_df)
        
        if not new_alerts:
            logger.info("No new emergency requests detected")
            return
        
        logger.info(f"Detected {len(new_alerts)} new emergency requests")
        
        # Process each alert
        for alert in new_alerts:
            try:
                # Find matching donors
                matched_donors = self.find_matching_donors_for_alert(alert, donors_df)
                
                if matched_donors:
                    # Send notifications asynchronously
                    asyncio.run(self.send_emergency_notifications(alert, matched_donors))
                else:
                    logger.warning(f"No matching donors found for alert {alert.alert_id}")
                
                # Add to history
                self.alert_history.append({
                    'alert_id': alert.alert_id,
                    'timestamp': alert.timestamp.isoformat(),
                    'status': 'processed',
                    'matched_donors_count': len(matched_donors) if matched_donors else 0
                })
                
            except Exception as e:
                logger.error(f"Error processing alert {alert.alert_id}: {e}")
                alert.status = 'error'
        
        # Clean up expired alerts
        self._cleanup_expired_alerts()
    
    def _cleanup_expired_alerts(self):
        """Remove expired alerts from active alerts"""
        current_time = datetime.now()
        expired_alerts = []
        
        for request_id, alert in self.active_alerts.items():
            if (current_time - alert.timestamp).total_seconds() > (self.config['alert_expiry_hours'] * 3600):
                expired_alerts.append(request_id)
        
        for request_id in expired_alerts:
            del self.active_alerts[request_id]
            logger.info(f"Expired alert removed: {request_id}")
    
    def get_alert_statistics(self) -> Dict:
        """Get statistics about emergency alerts"""
        current_time = datetime.now()
        
        # Active alerts by urgency
        urgency_counts = {}
        for alert in self.active_alerts.values():
            urgency = alert.urgency_level
            urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
        
        # Recent alerts (last 24 hours)
        recent_alerts = [
            alert for alert in self.alert_history
            if (current_time - datetime.fromisoformat(alert['timestamp'])).total_seconds() <= 86400
        ]
        
        return {
            'active_alerts_count': len(self.active_alerts),
            'urgency_distribution': urgency_counts,
            'recent_alerts_count': len(recent_alerts),
            'total_alerts_processed': len(self.alert_history),
            'last_processed': self.alert_history[-1]['timestamp'] if self.alert_history else None
        }
    
    def save_alert_data(self, output_file: str = "emergency_alerts.json"):
        """Save alert data to JSON file"""
        data = {
            'active_alerts': {
                req_id: {
                    'alert_id': alert.alert_id,
                    'blood_type_needed': alert.blood_type_needed,
                    'urgency_level': alert.urgency_level,
                    'location': alert.location,
                    'timestamp': alert.timestamp.isoformat(),
                    'status': alert.status,
                    'matched_donors_count': len(alert.matched_donors) if alert.matched_donors else 0
                }
                for req_id, alert in self.active_alerts.items()
            },
            'alert_history': self.alert_history,
            'statistics': self.get_alert_statistics()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Alert data saved to {output_file}")

def main():
    """Example usage of the emergency notification service"""
    print("Emergency Notification Service")
    print("=" * 50)
    
    try:
        # Load datasets
        emergency_requests_df = pd.read_csv("data/emergency_requests.csv")
        donors_df = pd.read_csv("data/donors.csv")
        
        # Initialize service
        service = EmergencyNotificationService()
        
        # Process emergency requests
        service.process_emergency_requests(emergency_requests_df, donors_df)
        
        # Get statistics
        stats = service.get_alert_statistics()
        print(f"\nAlert Statistics:")
        print(f"Active Alerts: {stats['active_alerts_count']}")
        print(f"Urgency Distribution: {stats['urgency_distribution']}")
        print(f"Recent Alerts: {stats['recent_alerts_count']}")
        
        # Save data
        service.save_alert_data()
        
    except FileNotFoundError:
        print("Data files not found. Please run the synthetic data generator first.")
        print("Run: python src/utils/syntheticDataGenerator.py")

if __name__ == "__main__":
    main()

