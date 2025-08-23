#!/usr/bin/env python3
"""
Patient-Donor Matching Algorithm for ThalaNet Emergency Blood Management Platform
Implements intelligent matching based on blood type compatibility, location, urgency, and ML predictions
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import json
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

class PatientDonorMatching:
    def __init__(self):
        """Initialize the patient-donor matching system"""
        
        # Blood type compatibility matrix
        self.blood_compatibility = {
            'O-': ['O-'],
            'O+': ['O+', 'O-'],
            'A-': ['A-', 'O-'],
            'A+': ['A+', 'A-', 'O+', 'O-'],
            'B-': ['B-', 'O-'],
            'B+': ['B+', 'B-', 'O+', 'O-'],
            'AB-': ['AB-', 'A-', 'B-', 'O-'],
            'AB+': ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']
        }
        
        # Urgency weights for scoring
        self.urgency_weights = {
            'LOW': 1.0,
            'MEDIUM': 1.5,
            'HIGH': 2.0,
            'CRITICAL': 3.0
        }
        
        # Location proximity weights
        self.distance_weights = {
            'same_city': 1.0,
            'nearby_city': 0.8,
            'far_city': 0.6
        }
        
        # Maximum acceptable distance (km)
        self.max_distance = 100
        
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using geodesic distance
        
        Args:
            lat1, lon1: First coordinate pair
            lat2, lon2: Second coordinate pair
            
        Returns:
            Distance in kilometers
        """
        try:
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers
        except:
            # Fallback to simple calculation if geopy fails
            return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111  # Rough conversion
            
    def get_location_proximity(self, distance: float) -> str:
        """
        Categorize location proximity based on distance
        
        Args:
            distance: Distance in kilometers
            
        Returns:
            Proximity category
        """
        if distance <= 10:
            return 'same_city'
        elif distance <= 50:
            return 'nearby_city'
        else:
            return 'far_city'
    
    def check_blood_compatibility(self, patient_blood_type: str, donor_blood_type: str) -> bool:
        """
        Check if donor blood type is compatible with patient
        
        Args:
            patient_blood_type: Patient's required blood type
            donor_blood_type: Donor's blood type
            
        Returns:
            True if compatible, False otherwise
        """
        return donor_blood_type in self.blood_compatibility.get(patient_blood_type, [])
    
    def calculate_matching_score(self, 
                               patient: Dict, 
                               donor: Dict, 
                               distance: float,
                               predicted_availability: float = 0.5) -> float:
        """
        Calculate matching score between patient and donor
        
        Args:
            patient: Patient data dictionary
            donor: Donor data dictionary
            distance: Distance between patient and donor
            predicted_availability: ML-predicted availability score (0-1)
            
        Returns:
            Matching score (higher is better)
        """
        score = 0.0
        
        # Blood type compatibility (mandatory)
        if not self.check_blood_compatibility(patient['blood_type_required'], donor['blood_type']):
            return 0.0
        
        # Base compatibility score
        score += 100
        
        # Urgency factor
        urgency = patient.get('urgency_level', 'MEDIUM')
        urgency_multiplier = self.urgency_weights.get(urgency, 1.0)
        score *= urgency_multiplier
        
        # Distance factor
        proximity = self.get_location_proximity(distance)
        distance_weight = self.distance_weights.get(proximity, 0.5)
        score *= distance_weight
        
        # Availability factor
        availability_score = donor.get('predicted_availability_score', predicted_availability)
        score *= (0.5 + 0.5 * availability_score)
        
        # Health condition factor
        if donor.get('health_conditions') == 'None':
            score *= 1.2
        else:
            score *= 0.8
        
        # Responsiveness factor
        responsiveness = donor.get('responsiveness_score', 0.5)
        score *= (0.8 + 0.4 * responsiveness)
        
        # Age factor (18-45 preferred)
        donor_age = donor.get('age', 35)
        if 18 <= donor_age <= 45:
            score *= 1.1
        elif donor_age > 65:
            score *= 0.9
        
        # Recent donation factor
        last_donation = donor.get('last_donation_date')
        if last_donation:
            try:
                last_donation_date = pd.to_datetime(last_donation)
                days_since = (datetime.now() - last_donation_date).days
                if days_since >= 56:  # 8 weeks minimum
                    score *= 1.2
                elif days_since < 30:
                    score *= 0.3  # Too recent
            except:
                pass
        
        return max(0.0, score)
    
    def find_matches(self, 
                    patient: Dict, 
                    donors_df: pd.DataFrame,
                    max_matches: int = 10,
                    min_score: float = 50.0) -> List[Dict]:
        """
        Find best matching donors for a patient
        
        Args:
            patient: Patient data dictionary
            donors_df: DataFrame of available donors
            max_matches: Maximum number of matches to return
            min_score: Minimum matching score threshold
            
        Returns:
            List of matching donors with scores and details
        """
        matches = []
        
        # Filter donors by basic criteria
        available_donors = donors_df[
            (donors_df['availability_status'] == 'Available') &
            (donors_df['health_conditions'] != 'HIV/AIDS') &
            (donors_df['health_conditions'] != 'Hepatitis')
        ].copy()
        
        if len(available_donors) == 0:
            return matches
        
        # Calculate matching scores for all compatible donors
        for _, donor in available_donors.iterrows():
            # Calculate distance
            distance = self.calculate_distance(
                patient.get('latitude', 0),
                patient.get('longitude', 0),
                donor.get('latitude', 0),
                donor.get('longitude', 0)
            )
            
            # Skip if too far
            if distance > self.max_distance:
                continue
            
            # Calculate matching score
            score = self.calculate_matching_score(
                patient, 
                donor.to_dict(), 
                distance,
                donor.get('predicted_availability_score', 0.5)
            )
            
            if score >= min_score:
                match = {
                    'donor_id': donor['donor_id'],
                    'donor_name': donor['name'],
                    'blood_type': donor['blood_type'],
                    'age': donor['age'],
                    'gender': donor['gender'],
                    'location': donor['location'],
                    'distance_km': round(distance, 2),
                    'matching_score': round(score, 2),
                    'predicted_availability': donor.get('predicted_availability_score', 0.5),
                    'responsiveness_score': donor.get('responsiveness_score', 0.5),
                    'last_donation_date': donor.get('last_donation_date'),
                    'health_conditions': donor.get('health_conditions'),
                    'contact_number': donor.get('contact_number'),
                    'urgency_level': patient.get('urgency_level', 'MEDIUM')
                }
                matches.append(match)
        
        # Sort by matching score (highest first)
        matches.sort(key=lambda x: x['matching_score'], reverse=True)
        
        # Return top matches
        return matches[:max_matches]
    
    def find_emergency_matches(self, 
                              emergency_request: Dict, 
                              donors_df: pd.DataFrame,
                              max_matches: int = 20) -> Dict:
        """
        Find emergency matches for urgent blood requests
        
        Args:
            emergency_request: Emergency request data
            donors_df: DataFrame of available donors
            
        Returns:
            Dictionary with matching results and recommendations
        """
        # Create patient object from emergency request
        patient = {
            'blood_type_required': emergency_request['blood_type_needed'],
            'urgency_level': emergency_request['urgency_level'],
            'latitude': emergency_request.get('latitude', 0),
            'longitude': emergency_request.get('longitude', 0),
            'location': emergency_request['location']
        }
        
        # Find matches
        matches = self.find_matches(patient, donors_df, max_matches, min_score=30.0)
        
        # Categorize matches by urgency and distance
        critical_matches = [m for m in matches if m['urgency_level'] == 'CRITICAL' and m['distance_km'] <= 25]
        high_priority_matches = [m for m in matches if m['matching_score'] >= 150 and m['distance_km'] <= 50]
        standard_matches = [m for m in matches if m['matching_score'] >= 100]
        
        # Generate recommendations
        recommendations = {
            'immediate_contact': critical_matches[:3],
            'high_priority': high_priority_matches[:5],
            'backup_options': standard_matches[:10],
            'total_matches': len(matches),
            'blood_type_needed': emergency_request['blood_type_needed'],
            'urgency_level': emergency_request['urgency_level'],
            'location': emergency_request['location'],
            'timestamp': datetime.now().isoformat()
        }
        
        return recommendations
    
    def batch_match_patients(self, 
                           patients_df: pd.DataFrame, 
                           donors_df: pd.DataFrame,
                           max_matches_per_patient: int = 5) -> Dict:
        """
        Perform batch matching for multiple patients
        
        Args:
            patients_df: DataFrame of patients
            donors_df: DataFrame of donors
            max_matches_per_patient: Maximum matches per patient
            
        Returns:
            Dictionary with matching results for all patients
        """
        print(f"Performing batch matching for {len(patients_df)} patients...")
        
        all_matches = {}
        total_matches = 0
        
        for _, patient in patients_df.iterrows():
            patient_dict = patient.to_dict()
            
            # Find matches for this patient
            matches = self.find_matches(
                patient_dict, 
                donors_df, 
                max_matches=max_matches_per_patient,
                min_score=40.0
            )
            
            all_matches[patient['patient_id']] = {
                'patient_info': {
                    'name': patient['name'],
                    'blood_type_required': patient['blood_type_required'],
                    'urgency_level': patient['urgency_level'],
                    'location': patient['location']
                },
                'matches': matches,
                'match_count': len(matches)
            }
            
            total_matches += len(matches)
        
        print(f"Batch matching completed. Total matches found: {total_matches}")
        
        return all_matches
    
    def generate_matching_report(self, matches: Dict) -> str:
        """
        Generate a human-readable matching report
        
        Args:
            matches: Matching results dictionary
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("PATIENT-DONOR MATCHING REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total patients: {len(matches)}")
        report.append("")
        
        for patient_id, patient_data in matches.items():
            patient_info = patient_data['patient_info']
            matches_list = patient_data['matches']
            
            report.append(f"Patient: {patient_info['name']} ({patient_id})")
            report.append(f"Blood Type Required: {patient_info['blood_type_required']}")
            report.append(f"Urgency Level: {patient_info['urgency_level']}")
            report.append(f"Location: {patient_info['location']}")
            report.append(f"Matches Found: {len(matches_list)}")
            report.append("")
            
            if matches_list:
                report.append("Top Matches:")
                for i, match in enumerate(matches_list[:3], 1):
                    report.append(f"  {i}. {match['donor_name']} ({match['donor_id']})")
                    report.append(f"     Score: {match['matching_score']}")
                    report.append(f"     Distance: {match['distance_km']} km")
                    report.append(f"     Availability: {match['predicted_availability']:.2f}")
                    report.append("")
            else:
                report.append("  No suitable matches found")
                report.append("")
            
            report.append("-" * 40)
            report.append("")
        
        return "\n".join(report)
    
    def save_matching_results(self, matches: Dict, output_file: str = "matching_results.json"):
        """Save matching results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(matches, f, indent=2, default=str)
        print(f"Matching results saved to {output_file}")

def main():
    """Example usage of the matching system"""
    print("Patient-Donor Matching System")
    print("=" * 50)
    
    try:
        # Load datasets
        donors_df = pd.read_csv("data/donors.csv")
        patients_df = pd.read_csv("data/patients.csv")
        emergency_requests_df = pd.read_csv("data/emergency_requests.csv")
        
        # Initialize matching system
        matcher = PatientDonorMatching()
        
        # Example 1: Find matches for a specific patient
        print("\n1. Finding matches for a specific patient...")
        sample_patient = patients_df.iloc[0].to_dict()
        matches = matcher.find_matches(sample_patient, donors_df, max_matches=5)
        
        print(f"Found {len(matches)} matches for {sample_patient['name']}")
        for i, match in enumerate(matches[:3], 1):
            print(f"  {i}. {match['donor_name']} - Score: {match['matching_score']}, Distance: {match['distance_km']} km")
        
        # Example 2: Emergency matching
        print("\n2. Emergency matching...")
        sample_emergency = emergency_requests_df.iloc[0].to_dict()
        emergency_matches = matcher.find_emergency_matches(sample_emergency, donors_df)
        
        print(f"Emergency matches: {emergency_matches['total_matches']} total")
        print(f"Immediate contact: {len(emergency_matches['immediate_contact'])}")
        print(f"High priority: {len(emergency_matches['high_priority'])}")
        
        # Example 3: Batch matching
        print("\n3. Batch matching for all patients...")
        batch_matches = matcher.batch_match_patients(patients_df.head(10), donors_df)
        
        # Generate and save report
        report = matcher.generate_matching_report(batch_matches)
        with open("matching_report.txt", "w") as f:
            f.write(report)
        
        print("Matching report saved to matching_report.txt")
        
        # Save results
        matcher.save_matching_results(batch_matches)
        
    except FileNotFoundError:
        print("Data files not found. Please run the synthetic data generator first.")
        print("Run: python src/utils/syntheticDataGenerator.py")

if __name__ == "__main__":
    main()

