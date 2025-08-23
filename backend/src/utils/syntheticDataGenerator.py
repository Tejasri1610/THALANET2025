#!/usr/bin/env python3
"""
Synthetic Dataset Generator for ThalaNet Emergency Blood Management Platform
Generates realistic datasets for donors, patients, emergency requests, and historical donations
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

class SyntheticDataGenerator:
    def __init__(self, seed: int = 42):
        """Initialize the synthetic data generator with a seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        self.seed = seed
        
        # Blood type distribution (realistic Indian population)
        self.blood_type_distribution = {
            'O+': 0.38, 'B+': 0.32, 'A+': 0.22, 'AB+': 0.08,
            'O-': 0.07, 'B-': 0.06, 'A-': 0.04, 'AB-': 0.01
        }
        
        # Indian cities with coordinates
        self.cities = [
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'weight': 0.25},
            {'name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025, 'weight': 0.22},
            {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'weight': 0.18},
            {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'weight': 0.15},
            {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'weight': 0.12},
            {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'weight': 0.08}
        ]
        
        # Health conditions that affect donation
        self.health_conditions = [
            'None', 'Diabetes', 'Hypertension', 'Anemia', 'HIV/AIDS', 
            'Hepatitis', 'Malaria', 'Tuberculosis', 'Cancer', 'Heart Disease'
        ]
        
        # Urgency levels
        self.urgency_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        
    def generate_donors(self, count: int = 1000) -> pd.DataFrame:
        """Generate synthetic donor data"""
        print(f"Generating {count} donor records...")
        donors = []

        # Normalize blood type probabilities
        blood_types = list(self.blood_type_distribution.keys())
        blood_probs = np.array(list(self.blood_type_distribution.values()))
        blood_probs = blood_probs / blood_probs.sum()

        # Normalize city weights
        city_weights = np.array([c['weight'] for c in self.cities])
        city_weights = city_weights / city_weights.sum()
        
        for i in range(count):
            age = max(18, min(65, int(np.random.normal(35, 12))))
            gender = np.random.choice(['Male', 'Female'], p=[0.6, 0.4])
            blood_type = np.random.choice(blood_types, p=blood_probs)
            city = np.random.choice(self.cities, p=city_weights)
            location = f"{city['name']}, India"
            
            last_donation_days = np.random.exponential(180)
            last_donation_date = datetime.now() - timedelta(days=int(last_donation_days))
            days_since_donation = (datetime.now() - last_donation_date).days
            base_availability = 1.0 if days_since_donation >= 56 else 0.0
            
            health_condition = np.random.choice(
                self.health_conditions,
                p=[0.7, 0.08, 0.07, 0.05, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01]
            )
            if health_condition != 'None':
                base_availability *= 0.3
            
            donation_frequency = np.random.poisson(2)
            responsiveness = np.random.beta(2, 2)
            contact_number = f"+91-{random.randint(7000000000, 9999999999)}"
            
            donor = {
                'donor_id': f"DON_{i+1:06d}",
                'name': f"Donor_{i+1}",
                'age': age,
                'gender': gender,
                'blood_type': blood_type,
                'location': location,
                'latitude': city['lat'] + np.random.normal(0, 0.01),
                'longitude': city['lon'] + np.random.normal(0, 0.01),
                'last_donation_date': last_donation_date.strftime('%Y-%m-%d'),
                'availability_status': 'Available' if base_availability > 0.5 else 'Unavailable',
                'health_conditions': health_condition,
                'contact_number': contact_number,
                'donation_frequency': donation_frequency,
                'responsiveness_score': responsiveness,
                'base_availability_score': base_availability
            }
            donors.append(donor)
        
        df = pd.DataFrame(donors)
        print(f"Generated {len(df)} donor records")
        return df

    def generate_patients(self, count: int = 500) -> pd.DataFrame:
        """Generate synthetic patient data"""
        print(f"Generating {count} patient records...")
        patients = []

        blood_types = list(self.blood_type_distribution.keys())
        blood_probs = np.array(list(self.blood_type_distribution.values()))
        blood_probs = blood_probs / blood_probs.sum()
        city_weights = np.array([c['weight'] for c in self.cities])
        city_weights = city_weights / city_weights.sum()
        
        for i in range(count):
            age = max(1, min(85, int(np.random.normal(45, 20))))
            gender = np.random.choice(['Male', 'Female'], p=[0.52, 0.48])
            blood_type_required = np.random.choice(blood_types, p=blood_probs)
            city = np.random.choice(self.cities, p=city_weights)
            location = f"{city['name']}, India"
            urgency_level = np.random.choice(self.urgency_levels, p=[0.3, 0.4, 0.2, 0.1])
            
            urgency_days = {
                'LOW': np.random.randint(7, 30),
                'MEDIUM': np.random.randint(3, 7),
                'HIGH': np.random.randint(1, 3),
                'CRITICAL': np.random.randint(1, 2)/24  # fraction of a day
            }
            
            required_by_date = datetime.now() + timedelta(days=urgency_days[urgency_level])
            
            patient = {
                'patient_id': f"PAT_{i+1:06d}",
                'name': f"Patient_{i+1}",
                'age': age,
                'gender': gender,
                'blood_type_required': blood_type_required,
                'location': location,
                'latitude': city['lat'] + np.random.normal(0, 0.01),
                'longitude': city['lon'] + np.random.normal(0, 0.01),
                'urgency_level': urgency_level,
                'required_by_date': required_by_date.strftime('%Y-%m-%d %H:%M:%S'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            patients.append(patient)
        
        df = pd.DataFrame(patients)
        print(f"Generated {len(df)} patient records")
        return df

    def generate_emergency_requests(self, count: int = 200) -> pd.DataFrame:
        """Generate synthetic emergency request data"""
        print(f"Generating {count} emergency request records...")
        requests = []

        blood_types = list(self.blood_type_distribution.keys())
        blood_probs = np.array(list(self.blood_type_distribution.values()))
        blood_probs = blood_probs / blood_probs.sum()
        city_weights = np.array([c['weight'] for c in self.cities])
        city_weights = city_weights / city_weights.sum()
        
        for i in range(count):
            blood_type_needed = np.random.choice(blood_types, p=blood_probs)
            city = np.random.choice(self.cities, p=city_weights)
            location = f"{city['name']}, India"
            urgency_level = np.random.choice(self.urgency_levels, p=[0.1, 0.2, 0.4, 0.3])
            
            urgency_hours = {
                'LOW': np.random.randint(24, 168),
                'MEDIUM': np.random.randint(6, 24),
                'HIGH': np.random.randint(1, 6),
                'CRITICAL': np.random.randint(0, 1)
            }
            timestamp = datetime.now() - timedelta(hours=urgency_hours[urgency_level])
            
            request = {
                'request_id': f"REQ_{i+1:06d}",
                'blood_type_needed': blood_type_needed,
                'location': location,
                'latitude': city['lat'] + np.random.normal(0, 0.01),
                'longitude': city['lon'] + np.random.normal(0, 0.01),
                'urgency_level': urgency_level,
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status': np.random.choice(['Active', 'Fulfilled', 'Expired'], p=[0.6, 0.3, 0.1]),
                'units_required': np.random.randint(1, 5),
                'hospital_name': f"Hospital_{random.randint(1, 20)}",
                'contact_person': f"Dr. {random.choice(['Sharma', 'Patel', 'Singh', 'Kumar', 'Verma'])}",
                'contact_number': f"+91-{random.randint(7000000000, 9999999999)}"
            }
            requests.append(request)
        
        return pd.DataFrame(requests)

    def generate_historical_donations(self, donors_df: pd.DataFrame, max_records: int = 10) -> pd.DataFrame:
        """Generate historical donation records for donors"""
        print("Generating historical donation records...")
        records = []
        for _, donor in donors_df.iterrows():
            num_donations = np.random.randint(1, max_records + 1)
            for _ in range(num_donations):
                donation_date = datetime.now() - timedelta(days=int(np.random.exponential(180)))
                records.append({
                    'donor_id': donor['donor_id'],
                    'donation_date': donation_date.strftime('%Y-%m-%d'),
                    'blood_type': donor['blood_type'],
                    'location': donor['location']
                })
        return pd.DataFrame(records)

    def save_datasets(self, output_dir: str = "./data"):
        """Generate and save all datasets as CSVs"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        print("Starting synthetic dataset generation...")

        donors_df = self.generate_donors(1000)
        donors_df.to_csv(output_path / "donors.csv", index=False)
        
        patients_df = self.generate_patients(500)
        patients_df.to_csv(output_path / "patients.csv", index=False)
        
        requests_df = self.generate_emergency_requests(200)
        requests_df.to_csv(output_path / "emergency_requests.csv", index=False)
        
        historical_df = self.generate_historical_donations(donors_df)
        historical_df.to_csv(output_path / "historical_donations.csv", index=False)

        print(f"Datasets saved to {output_path.resolve()}")


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    generator.save_datasets()
