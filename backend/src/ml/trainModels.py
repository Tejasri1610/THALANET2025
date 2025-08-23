#!/usr/bin/env python3
"""
Main Training Script for ThalaNet Emergency Blood Management Platform
Orchestrates the training of all ML models and generates the complete system
"""

import os
import sys
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.syntheticDataGenerator import SyntheticDataGenerator
from ml.donorPredictionModel import DonorPredictionModel, train_and_evaluate_models
from ml.patientDonorMatching import PatientDonorMatching
from services.emergencyNotificationService import EmergencyNotificationService
from services.whatsappChatbotService import WhatsAppChatbotService
from services.eraktKoshService import ERaktKoshService
from security.dataPrivacySecurity import DataPrivacySecurity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ThalaNetModelTrainer:
    def __init__(self, config: Dict = None):
        """
        Initialize the ThalaNet model trainer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._get_default_config()
        self.output_dir = Path(self.config['output_dir'])
        self.data_dir = self.output_dir / 'data'
        self.models_dir = self.output_dir / 'models'
        self.results_dir = self.output_dir / 'results'
        
        # Create output directories
        self._create_directories()
        
        # Initialize components
        self.data_generator = None
        self.donor_prediction_model = None
        self.matching_system = None
        self.emergency_service = None
        self.chatbot_service = None
        self.eraktkosh_service = None
        self.security_module = None
        
        logger.info("ThalaNet Model Trainer initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'output_dir': 'output',
            'generate_synthetic_data': True,
            'train_ml_models': True,
            'test_matching_system': True,
            'test_emergency_service': True,
            'test_chatbot_service': True,
            'test_eraktkosh_service': True,
            'test_security_module': True,
            'data_sizes': {
                'donors': 1000,
                'patients': 500,
                'emergency_requests': 200,
                'historical_donations': 5000
            },
            'ml_models': ['random_forest', 'gradient_boosting', 'logistic'],
            'enable_cross_validation': True,
            'save_intermediate_results': True
        }
    
    def _create_directories(self):
        """Create necessary output directories"""
        try:
            self.output_dir.mkdir(exist_ok=True)
            self.data_dir.mkdir(exist_ok=True)
            self.models_dir.mkdir(exist_ok=True)
            self.results_dir.mkdir(exist_ok=True)
            
            logger.info(f"Created output directories in {self.output_dir}")
        
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
            raise
    
    def generate_synthetic_data(self) -> Dict:
        """
        Generate synthetic datasets for training and testing
        
        Returns:
            Dictionary with generated datasets
        """
        logger.info("Starting synthetic data generation...")
        
        try:
            # Initialize data generator
            self.data_generator = SyntheticDataGenerator(seed=42)
            
            # Generate datasets
            datasets = self.data_generator.save_datasets(str(self.data_dir))
            
            # Save metadata
            metadata = {
                'generation_timestamp': datetime.now().isoformat(),
                'data_sizes': {name: len(df) for name, df in datasets.items()},
                'config': self.config['data_sizes']
            }
            
            with open(self.data_dir / 'generation_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info("Synthetic data generation completed successfully")
            return datasets
        
        except Exception as e:
            logger.error(f"Error generating synthetic data: {e}")
            raise
    
    def train_ml_models(self, datasets: Dict) -> Dict:
        """
        Train machine learning models for donor prediction
        
        Args:
            datasets: Dictionary with training datasets
            
        Returns:
            Dictionary with training results
        """
        logger.info("Starting ML model training...")
        
        try:
            # Prepare data
            donors_df = datasets['donors']
            donations_df = datasets['historical_donations']
            
            # Train and evaluate models
            training_results = train_and_evaluate_models(donors_df, donations_df)
            
            # Save training results
            results_file = self.results_dir / 'ml_training_results.json'
            with open(results_file, 'w') as f:
                json.dump(training_results, f, indent=2, default=str)
            
            logger.info(f"ML model training completed. Results saved to {results_file}")
            return training_results
        
        except Exception as e:
            logger.error(f"Error training ML models: {e}")
            raise
    
    def test_matching_system(self, datasets: Dict) -> Dict:
        """
        Test the patient-donor matching system
        
        Args:
            datasets: Dictionary with test datasets
            
        Returns:
            Dictionary with matching results
        """
        logger.info("Testing patient-donor matching system...")
        
        try:
            # Initialize matching system
            self.matching_system = PatientDonorMatching()
            
            # Test matching for a sample of patients
            test_patients = datasets['patients'].head(10)
            donors_df = datasets['donors']
            
            # Perform batch matching
            matching_results = self.matching_system.batch_match_patients(
                test_patients, donors_df, max_matches_per_patient=5
            )
            
            # Generate matching report
            report = self.matching_system.generate_matching_report(matching_results)
            
            # Save results
            report_file = self.results_dir / 'matching_report.txt'
            with open(report_file, 'w') as f:
                f.write(report)
            
            # Save matching results
            results_file = self.results_dir / 'matching_results.json'
            self.matching_system.save_matching_results(matching_results, str(results_file))
            
            logger.info(f"Matching system testing completed. Report saved to {report_file}")
            
            return {
                'matching_results': matching_results,
                'report_file': str(report_file),
                'results_file': str(results_file)
            }
        
        except Exception as e:
            logger.error(f"Error testing matching system: {e}")
            raise
    
    def test_emergency_service(self, datasets: Dict) -> Dict:
        """
        Test the emergency notification service
        
        Args:
            datasets: Dictionary with test datasets
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing emergency notification service...")
        
        try:
            # Initialize emergency service
            self.emergency_service = EmergencyNotificationService()
            
            # Test with emergency requests and donors
            emergency_requests_df = datasets['emergency_requests']
            donors_df = datasets['donors']
            
            # Process emergency requests
            self.emergency_service.process_emergency_requests(emergency_requests_df, donors_df)
            
            # Get statistics
            stats = self.emergency_service.get_alert_statistics()
            
            # Save alert data
            alerts_file = self.results_dir / 'emergency_alerts.json'
            self.emergency_service.save_alert_data(str(alerts_file))
            
            logger.info(f"Emergency service testing completed. Alerts saved to {alerts_file}")
            
            return {
                'statistics': stats,
                'alerts_file': str(alerts_file)
            }
        
        except Exception as e:
            logger.error(f"Error testing emergency service: {e}")
            raise
    
    def test_chatbot_service(self, datasets: Dict) -> Dict:
        """
        Test the WhatsApp chatbot service
        
        Args:
            datasets: Dictionary with test datasets
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing WhatsApp chatbot service...")
        
        try:
            # Initialize chatbot service
            self.chatbot_service = WhatsAppChatbotService()
            
            # Test with sample messages
            from services.whatsappChatbotService import ChatMessage
            
            test_messages = [
                ChatMessage("MSG_001", "+91-9876543210", "Hello", datetime.now()),
                ChatMessage("MSG_002", "+91-9876543210", "I want to donate blood", datetime.now()),
                ChatMessage("MSG_003", "+91-9876543210", "Emergency! Need A+ blood", datetime.now()),
                ChatMessage("MSG_004", "+91-9876543210", "Show my donation history", datetime.now())
            ]
            
            # Process messages
            responses = []
            for message in test_messages:
                response = self.chatbot_service.process_message(
                    message, datasets['donors'], datasets['patients'], datasets['emergency_requests']
                )
                responses.append({
                    'message': message.message_text,
                    'response': response.response_text,
                    'quick_replies': response.quick_replies
                })
            
            # Save conversation data
            conversations_file = self.results_dir / 'whatsapp_conversations.json'
            self.chatbot_service.save_conversation_data(str(conversations_file))
            
            # Get conversation summary
            summary = self.chatbot_service.get_conversation_summary("+91-9876543210")
            
            logger.info(f"Chatbot service testing completed. Conversations saved to {conversations_file}")
            
            return {
                'responses': responses,
                'summary': summary,
                'conversations_file': str(conversations_file)
            }
        
        except Exception as e:
            logger.error(f"Error testing chatbot service: {e}")
            raise
    
    def test_eraktkosh_service(self, datasets: Dict) -> Dict:
        """
        Test the E-RaktKosh API integration service
        
        Args:
            datasets: Dictionary with test datasets
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing E-RaktKosh API integration service...")
        
        try:
            # Initialize E-RaktKosh service
            self.eraktkosh_service = ERaktKoshService()
            
            # Test various API endpoints
            test_results = {}
            
            # Test blood banks
            blood_banks = self.eraktkosh_service.get_blood_banks()
            test_results['blood_banks'] = blood_banks
            
            # Test blood inventory
            inventory = self.eraktkosh_service.get_blood_inventory()
            test_results['inventory'] = inventory
            
            # Test blood requests
            requests = self.eraktkosh_service.get_blood_requests()
            test_results['requests'] = requests
            
            # Test emergency requests
            emergency = self.eraktkosh_service.get_emergency_blood_requests()
            test_results['emergency'] = emergency
            
            # Test statistics
            stats = self.eraktkosh_service.get_blood_bank_statistics()
            test_results['statistics'] = stats
            
            # Test API status
            api_status = self.eraktkosh_service.get_api_status()
            test_results['api_status'] = api_status
            
            # Save test results
            results_file = self.results_dir / 'eraktkosh_test_results.json'
            with open(results_file, 'w') as f:
                json.dump(test_results, f, indent=2, default=str)
            
            logger.info(f"E-RaktKosh service testing completed. Results saved to {results_file}")
            
            return {
                'test_results': test_results,
                'results_file': str(results_file)
            }
        
        except Exception as e:
            logger.error(f"Error testing E-RaktKosh service: {e}")
            raise
    
    def test_security_module(self) -> Dict:
        """
        Test the data privacy and security module
        
        Returns:
            Dictionary with test results
        """
        logger.info("Testing data privacy and security module...")
        
        try:
            # Initialize security module
            self.security_module = DataPrivacySecurity()
            
            # Test various security features
            test_results = {}
            
            # Test encryption/decryption
            test_data = "sensitive_patient_information"
            encrypted = self.security_module.encrypt_sensitive_data(test_data)
            decrypted = self.security_module.decrypt_sensitive_data(encrypted)
            test_results['encryption'] = {
                'original': test_data,
                'encrypted': encrypted,
                'decrypted': decrypted,
                'match': test_data == decrypted
            }
            
            # Test password hashing
            password = "MySecurePassword123!"
            hashed, salt = self.security_module.hash_password(password)
            is_valid = self.security_module.verify_password(password, hashed, salt)
            test_results['password_hashing'] = {
                'password': password,
                'hashed': hashed,
                'salt': salt,
                'verification': is_valid
            }
            
            # Test password strength validation
            weak_password = "123"
            strong_password = "MySecurePassword123!"
            
            weak_validation = self.security_module.validate_password_strength(weak_password)
            strong_validation = self.security_module.validate_password_strength(strong_password)
            
            test_results['password_validation'] = {
                'weak_password': weak_validation,
                'strong_password': strong_validation
            }
            
            # Test data masking
            test_phone = "+91-9876543210"
            test_email = "john.doe@example.com"
            test_name = "John Doe"
            
            masked_phone = self.security_module.mask_pii_data(test_phone, 'phone_number')
            masked_email = self.security_module.mask_pii_data(test_email, 'email')
            masked_name = self.security_module.mask_pii_data(test_name, 'name')
            
            test_results['data_masking'] = {
                'phone': {'original': test_phone, 'masked': masked_phone},
                'email': {'original': test_email, 'masked': masked_email},
                'name': {'original': test_name, 'masked': masked_name}
            }
            
            # Test secure token generation
            token = self.security_module.generate_secure_token(32)
            test_results['secure_token'] = token
            
            # Test input sanitization
            malicious_input = "<script>alert('xss')</script>Hello World"
            sanitized = self.security_module.sanitize_input(malicious_input)
            test_results['input_sanitization'] = {
                'malicious_input': malicious_input,
                'sanitized': sanitized
            }
            
            # Test security logging
            self.security_module.log_security_event('login_attempt', 'user123', {'ip': '192.168.1.1'})
            self.security_module.log_security_event('password_change', 'user123', {'method': 'web'})
            self.security_module.log_security_event('failed_login', 'user456', {'reason': 'invalid_password'})
            
            # Get security statistics
            stats = self.security_module.get_security_statistics()
            test_results['security_statistics'] = stats
            
            # Save test results
            results_file = self.results_dir / 'security_test_results.json'
            with open(results_file, 'w') as f:
                json.dump(test_results, f, indent=2, default=str)
            
            logger.info(f"Security module testing completed. Results saved to {results_file}")
            
            return {
                'test_results': test_results,
                'results_file': str(results_file)
            }
        
        except Exception as e:
            logger.error(f"Error testing security module: {e}")
            raise
    
    def run_complete_training(self) -> Dict:
        """
        Run the complete training and testing pipeline
        
        Returns:
            Dictionary with all results
        """
        logger.info("Starting complete ThalaNet training pipeline...")
        
        start_time = datetime.now()
        all_results = {}
        
        try:
            # Step 1: Generate synthetic data
            if self.config['generate_synthetic_data']:
                logger.info("Step 1: Generating synthetic data...")
                datasets = self.generate_synthetic_data()
                all_results['synthetic_data'] = {
                    'status': 'success',
                    'datasets': list(datasets.keys()),
                    'data_sizes': {name: len(df) for name, df in datasets.items()}
                }
            else:
                logger.info("Step 1: Skipping synthetic data generation...")
                # Load existing data
                datasets = {}
                for file_path in self.data_dir.glob('*.csv'):
                    dataset_name = file_path.stem
                    datasets[dataset_name] = pd.read_csv(file_path)
            
            # Step 2: Train ML models
            if self.config['train_ml_models']:
                logger.info("Step 2: Training ML models...")
                ml_results = self.train_ml_models(datasets)
                all_results['ml_training'] = ml_results
            
            # Step 3: Test matching system
            if self.config['test_matching_system']:
                logger.info("Step 3: Testing matching system...")
                matching_results = self.test_matching_system(datasets)
                all_results['matching_system'] = matching_results
            
            # Step 4: Test emergency service
            if self.config['test_emergency_service']:
                logger.info("Step 4: Testing emergency service...")
                emergency_results = self.test_emergency_service(datasets)
                all_results['emergency_service'] = emergency_results
            
            # Step 5: Test chatbot service
            if self.config['test_chatbot_service']:
                logger.info("Step 5: Testing chatbot service...")
                chatbot_results = self.test_chatbot_service(datasets)
                all_results['chatbot_service'] = chatbot_results
            
            # Step 6: Test E-RaktKosh service
            if self.config['test_eraktkosh_service']:
                logger.info("Step 6: Testing E-RaktKosh service...")
                eraktkosh_results = self.test_eraktkosh_service(datasets)
                all_results['eraktkosh_service'] = eraktkosh_results
            
            # Step 7: Test security module
            if self.config['test_security_module']:
                logger.info("Step 7: Testing security module...")
                security_results = self.test_security_module()
                all_results['security_module'] = security_results
            
            # Calculate total execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Add summary information
            all_results['summary'] = {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'execution_time_seconds': execution_time,
                'status': 'completed',
                'output_directory': str(self.output_dir)
            }
            
            # Save complete results
            complete_results_file = self.results_dir / 'complete_training_results.json'
            with open(complete_results_file, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)
            
            logger.info(f"Complete training pipeline finished in {execution_time:.2f} seconds")
            logger.info(f"All results saved to {complete_results_file}")
            
            return all_results
        
        except Exception as e:
            logger.error(f"Error in complete training pipeline: {e}")
            
            # Save error information
            error_results = {
                'summary': {
                    'start_time': start_time.isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'status': 'failed',
                    'error': str(e),
                    'output_directory': str(self.output_dir)
                },
                'partial_results': all_results
            }
            
            error_file = self.results_dir / 'training_error_results.json'
            with open(error_file, 'w') as f:
                json.dump(error_results, f, indent=2, default=str)
            
            raise
    
    def generate_system_summary(self) -> str:
        """
        Generate a human-readable summary of the complete system
        
        Returns:
            Formatted summary string
        """
        try:
            summary = []
            summary.append("=" * 80)
            summary.append("THALANET EMERGENCY BLOOD MANAGEMENT PLATFORM - SYSTEM SUMMARY")
            summary.append("=" * 80)
            summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            summary.append("")
            
            # Check what components are available
            summary.append("SYSTEM COMPONENTS:")
            summary.append("-" * 40)
            
            if self.data_generator:
                summary.append("✅ Synthetic Data Generator - Ready")
            else:
                summary.append("❌ Synthetic Data Generator - Not initialized")
            
            if self.donor_prediction_model:
                summary.append("✅ Donor Prediction ML Models - Ready")
            else:
                summary.append("❌ Donor Prediction ML Models - Not initialized")
            
            if self.matching_system:
                summary.append("✅ Patient-Donor Matching System - Ready")
            else:
                summary.append("❌ Patient-Donor Matching System - Not initialized")
            
            if self.emergency_service:
                summary.append("✅ Emergency Notification Service - Ready")
            else:
                summary.append("❌ Emergency Notification Service - Not initialized")
            
            if self.chatbot_service:
                summary.append("✅ WhatsApp Chatbot Service - Ready")
            else:
                summary.append("❌ WhatsApp Chatbot Service - Not initialized")
            
            if self.eraktkosh_service:
                summary.append("✅ E-RaktKosh API Integration - Ready")
            else:
                summary.append("❌ E-RaktKosh API Integration - Not initialized")
            
            if self.security_module:
                summary.append("✅ Data Privacy & Security Module - Ready")
            else:
                summary.append("❌ Data Privacy & Security Module - Not initialized")
            
            summary.append("")
            summary.append("OUTPUT FILES:")
            summary.append("-" * 40)
            
            # List output files
            for file_path in self.output_dir.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.output_dir)
                    summary.append(f"📁 {relative_path}")
            
            summary.append("")
            summary.append("NEXT STEPS:")
            summary.append("-" * 40)
            summary.append("1. Review generated datasets in the 'data' directory")
            summary.append("2. Examine ML model performance in 'results/ml_training_results.json'")
            summary.append("3. Check matching system results in 'results/matching_results.json'")
            summary.append("4. Review emergency service alerts in 'results/emergency_alerts.json'")
            summary.append("5. Test chatbot conversations in 'results/whatsapp_conversations.json'")
            summary.append("6. Verify E-RaktKosh integration in 'results/eraktkosh_test_results.json'")
            summary.append("7. Check security module results in 'results/security_test_results.json'")
            summary.append("")
            summary.append("8. Replace synthetic data with real datasets when available")
            summary.append("9. Update API endpoints in services for production use")
            summary.append("10. Configure security settings for production environment")
            summary.append("")
            summary.append("=" * 80)
            
            return "\n".join(summary)
        
        except Exception as e:
            logger.error(f"Error generating system summary: {e}")
            return f"Error generating summary: {e}"

def main():
    """Main function to run the complete training pipeline"""
    print("ThalaNet Emergency Blood Management Platform")
    print("Complete Training and Testing Pipeline")
    print("=" * 60)
    
    try:
        # Initialize trainer
        trainer = ThalaNetModelTrainer()
        
        # Run complete training
        results = trainer.run_complete_training()
        
        # Generate system summary
        summary = trainer.generate_system_summary()
        
        # Save summary
        summary_file = trainer.results_dir / 'system_summary.txt'
        with open(summary_file, 'w') as f:
            f.write(summary)
        
        # Print summary
        print("\n" + summary)
        print(f"\nSystem summary saved to: {summary_file}")
        
        print("\n🎉 Training pipeline completed successfully!")
        print(f"📁 All outputs saved to: {trainer.output_dir}")
        
    except Exception as e:
        print(f"\n❌ Training pipeline failed: {e}")
        print("Check the logs for detailed error information.")
        sys.exit(1)

if __name__ == "__main__":
    main()

