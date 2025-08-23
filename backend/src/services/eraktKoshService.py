#!/usr/bin/env python3
"""
E-RaktKosh API Integration Service for ThalaNet Emergency Blood Management Platform
Mock implementation that can be replaced with real government blood bank API endpoints
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import requests
import logging
from dataclasses import dataclass
import time
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BloodBankInfo:
    """Data class for blood bank information"""
    bank_id: str
    name: str
    location: str
    latitude: float
    longitude: float
    contact_number: str
    email: str
    blood_inventory: Dict[str, int]  # blood_type -> units_available
    last_updated: datetime
    status: str = 'active'  # active, inactive, maintenance

@dataclass
class BloodRequest:
    """Data class for blood requests"""
    request_id: str
    blood_type: str
    units_required: int
    urgency_level: str
    patient_name: str
    hospital_name: str
    contact_number: str
    location: str
    latitude: float
    longitude: float
    timestamp: datetime
    status: str = 'pending'  # pending, fulfilled, expired, cancelled

class ERaktKoshService:
    def __init__(self, config: Dict = None):
        """
        Initialize the E-RaktKosh API integration service
        
        Args:
            config: Configuration dictionary with API settings
        """
        self.config = config or self._get_default_config()
        self.api_base_url = self.config['api_base_url']
        self.api_key = self.config['api_key']
        self.session = requests.Session()
        
        # Mock data for development/testing
        self.mock_blood_banks = self._generate_mock_blood_banks()
        self.mock_requests = self._generate_mock_requests()
        
        # API rate limiting
        self.last_api_call = 0
        self.api_call_count = 0
        
        logger.info("E-RaktKosh Service initialized")
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'api_base_url': 'https://api.eraktkosh.in/v1',
            'api_key': 'mock_api_key_for_development',
            'timeout_seconds': 30,
            'max_retries': 3,
            'rate_limit_per_minute': 60,
            'enable_mock_mode': True,  # Set to False for production
            'mock_data_size': 100
        }
    
    def _generate_mock_blood_banks(self) -> List[BloodBankInfo]:
        """Generate mock blood bank data for development"""
        blood_banks = []
        
        # Major cities in India
        cities = [
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
            {'name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025},
            {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
            {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707},
            {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867},
            {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
            {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567},
            {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714}
        ]
        
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        
        for i, city in enumerate(cities):
            # Generate 3-5 blood banks per city
            num_banks = np.random.randint(3, 6)
            
            for j in range(num_banks):
                bank_id = f"BB_{city['name'][:3].upper()}_{i+1:02d}_{j+1:02d}"
                
                # Generate blood inventory
                inventory = {}
                for blood_type in blood_types:
                    # Random inventory levels (0-50 units)
                    inventory[blood_type] = np.random.randint(0, 51)
                
                blood_bank = BloodBankInfo(
                    bank_id=bank_id,
                    name=f"{city['name']} Blood Bank {j+1}",
                    location=f"{city['name']}, India",
                    latitude=city['lat'] + np.random.normal(0, 0.01),
                    longitude=city['lon'] + np.random.normal(0, 0.01),
                    contact_number=f"+91-{np.random.randint(7000000000, 9999999999)}",
                    email=f"bloodbank{j+1}@{city['name'].lower()}.gov.in",
                    blood_inventory=inventory,
                    last_updated=datetime.now() - timedelta(hours=np.random.randint(1, 24)),
                    status=np.random.choice(['active', 'active', 'active', 'maintenance'], p=[0.8, 0.1, 0.05, 0.05])
                )
                
                blood_banks.append(blood_bank)
        
        return blood_banks
    
    def _generate_mock_requests(self) -> List[BloodRequest]:
        """Generate mock blood request data for development"""
        requests = []
        
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        urgency_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        hospitals = [
            'Apollo Hospital', 'Fortis Hospital', 'Max Hospital', 'Manipal Hospital',
            'KIMS Hospital', 'Narayana Health', 'Medanta Hospital', 'BLK Hospital'
        ]
        
        for i in range(self.config['mock_data_size']):
            blood_type = np.random.choice(blood_types)
            urgency = np.random.choice(urgency_levels, p=[0.3, 0.4, 0.2, 0.1])
            
            # Generate random location
            city_idx = np.random.randint(0, len(self.mock_blood_banks))
            city = self.mock_blood_banks[city_idx]
            
            request = BloodRequest(
                request_id=f"REQ_{i+1:06d}",
                blood_type=blood_type,
                units_required=np.random.randint(1, 6),
                urgency_level=urgency,
                patient_name=f"Patient_{i+1}",
                hospital_name=np.random.choice(hospitals),
                contact_number=f"+91-{np.random.randint(7000000000, 9999999999)}",
                location=city.location,
                latitude=city.latitude + np.random.normal(0, 0.01),
                longitude=city.longitude + np.random.normal(0, 0.01),
                timestamp=datetime.now() - timedelta(hours=np.random.randint(1, 168)),
                status=np.random.choice(['pending', 'fulfilled', 'expired'], p=[0.6, 0.3, 0.1])
            )
            
            requests.append(request)
        
        return requests
    
    def _rate_limit_check(self):
        """Check and enforce API rate limiting"""
        current_time = time.time()
        
        # Reset counter if a minute has passed
        if current_time - self.last_api_call >= 60:
            self.api_call_count = 0
            self.last_api_call = current_time
        
        # Check if we're over the limit
        if self.api_call_count >= self.config['rate_limit_per_minute']:
            wait_time = 60 - (current_time - self.last_api_call)
            logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            self.api_call_count = 0
            self.last_api_call = time.time()
        
        self.api_call_count += 1
    
    def _make_api_call(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """
        Make API call to E-RaktKosh with rate limiting and error handling
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data for POST/PUT
            
        Returns:
            API response data
        """
        if self.config['enable_mock_mode']:
            # Return mock data for development
            return self._get_mock_response(endpoint, method, data)
        
        # Real API call
        self._rate_limit_check()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'ThalaNet/1.0'
            }
            
            url = f"{self.api_base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=self.config['timeout_seconds'])
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data, timeout=self.config['timeout_seconds'])
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=headers, json=data, timeout=self.config['timeout_seconds'])
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            return {'error': str(e), 'status': 'failed'}
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    def _get_mock_response(self, endpoint: str, method: str, data: Dict = None) -> Dict:
        """Get mock response for development/testing"""
        if 'blood-banks' in endpoint:
            return {
                'status': 'success',
                'data': [self._blood_bank_to_dict(bank) for bank in self.mock_blood_banks],
                'count': len(self.mock_blood_banks),
                'timestamp': datetime.now().isoformat()
            }
        elif 'blood-inventory' in endpoint:
            return {
                'status': 'success',
                'data': self._get_blood_inventory_summary(),
                'timestamp': datetime.now().isoformat()
            }
        elif 'requests' in endpoint:
            return {
                'status': 'success',
                'data': [self._blood_request_to_dict(req) for req in self.mock_requests],
                'count': len(self.mock_requests),
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'success',
                'data': {'message': 'Mock response for development'},
                'timestamp': datetime.now().isoformat()
            }
    
    def _blood_bank_to_dict(self, bank: BloodBankInfo) -> Dict:
        """Convert BloodBankInfo to dictionary"""
        return {
            'bank_id': bank.bank_id,
            'name': bank.name,
            'location': bank.location,
            'latitude': bank.latitude,
            'longitude': bank.longitude,
            'contact_number': bank.contact_number,
            'email': bank.email,
            'blood_inventory': bank.blood_inventory,
            'last_updated': bank.last_updated.isoformat(),
            'status': bank.status
        }
    
    def _blood_request_to_dict(self, request: BloodRequest) -> Dict:
        """Convert BloodRequest to dictionary"""
        return {
            'request_id': request.request_id,
            'blood_type': request.blood_type,
            'units_required': request.units_required,
            'urgency_level': request.urgency_level,
            'patient_name': request.patient_name,
            'hospital_name': request.hospital_name,
            'contact_number': request.contact_number,
            'location': request.location,
            'latitude': request.latitude,
            'longitude': request.longitude,
            'timestamp': request.timestamp.isoformat(),
            'status': request.status
        }
    
    def get_blood_banks(self, location: str = None, radius_km: float = 50) -> Dict:
        """
        Get list of blood banks from E-RaktKosh
        
        Args:
            location: Location to search around
            radius_km: Search radius in kilometers
            
        Returns:
            Dictionary with blood bank data
        """
        endpoint = '/blood-banks'
        if location:
            endpoint += f'?location={location}&radius={radius_km}'
        
        return self._make_api_call(endpoint, 'GET')
    
    def get_blood_inventory(self, bank_id: str = None, blood_type: str = None) -> Dict:
        """
        Get blood inventory information
        
        Args:
            bank_id: Specific blood bank ID
            blood_type: Specific blood type
            
        Returns:
            Dictionary with inventory data
        """
        if bank_id:
            endpoint = f'/blood-banks/{bank_id}/inventory'
        else:
            endpoint = '/blood-inventory'
            if blood_type:
                endpoint += f'?blood_type={blood_type}'
        
        return self._make_api_call(endpoint, 'GET')
    
    def get_blood_requests(self, status: str = None, urgency: str = None) -> Dict:
        """
        Get blood requests from E-RaktKosh
        
        Args:
            status: Filter by request status
            urgency: Filter by urgency level
            
        Returns:
            Dictionary with request data
        """
        endpoint = '/blood-requests'
        params = []
        
        if status:
            params.append(f'status={status}')
        if urgency:
            params.append(f'urgency={urgency}')
        
        if params:
            endpoint += '?' + '&'.join(params)
        
        return self._make_api_call(endpoint, 'GET')
    
    def create_blood_request(self, request_data: Dict) -> Dict:
        """
        Create a new blood request in E-RaktKosh
        
        Args:
            request_data: Blood request data
            
        Returns:
            Dictionary with created request info
        """
        # Validate required fields
        required_fields = ['blood_type', 'units_required', 'urgency_level', 'patient_name', 'hospital_name', 'contact_number', 'location']
        
        for field in required_fields:
            if field not in request_data:
                return {'error': f'Missing required field: {field}', 'status': 'failed'}
        
        # Add timestamp and generate request ID
        request_data['timestamp'] = datetime.now().isoformat()
        request_data['request_id'] = f"REQ_{int(time.time())}"
        request_data['status'] = 'pending'
        
        # Make API call
        return self._make_api_call('/blood-requests', 'POST', request_data)
    
    def update_blood_request(self, request_id: str, update_data: Dict) -> Dict:
        """
        Update an existing blood request
        
        Args:
            request_id: Request ID to update
            update_data: Data to update
            
        Returns:
            Dictionary with updated request info
        """
        return self._make_api_call(f'/blood-requests/{request_id}', 'PUT', update_data)
    
    def search_blood_banks(self, blood_type: str, location: str, radius_km: float = 50) -> Dict:
        """
        Search for blood banks with specific blood type availability
        
        Args:
            blood_type: Required blood type
            location: Search location
            radius_km: Search radius
            
        Returns:
            Dictionary with matching blood banks
        """
        endpoint = f'/search/blood-banks?blood_type={blood_type}&location={location}&radius={radius_km}'
        return self._make_api_call(endpoint, 'GET')
    
    def get_blood_availability_summary(self) -> Dict:
        """
        Get overall blood availability summary across all blood banks
        
        Returns:
            Dictionary with availability summary
        """
        return self._make_api_call('/blood-availability/summary', 'GET')
    
    def _get_blood_inventory_summary(self) -> Dict:
        """Get mock blood inventory summary"""
        summary = {}
        blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        
        for blood_type in blood_types:
            total_units = 0
            available_banks = 0
            
            for bank in self.mock_blood_banks:
                if bank.status == 'active':
                    units = bank.blood_inventory.get(blood_type, 0)
                    total_units += units
                    if units > 0:
                        available_banks += 1
            
            summary[blood_type] = {
                'total_units': total_units,
                'available_banks': available_banks,
                'average_per_bank': total_units / max(available_banks, 1)
            }
        
        return summary
    
    def get_emergency_blood_requests(self, location: str = None) -> Dict:
        """
        Get emergency blood requests for quick response
        
        Args:
            location: Location to filter by
            
        Returns:
            Dictionary with emergency requests
        """
        # Filter for high/critical urgency requests
        emergency_requests = [
            req for req in self.mock_requests
            if req.urgency_level in ['HIGH', 'CRITICAL'] and req.status == 'pending'
        ]
        
        if location:
            # Simple location filtering (in real implementation, use proper geospatial queries)
            emergency_requests = [
                req for req in emergency_requests
                if location.lower() in req.location.lower()
            ]
        
        return {
            'status': 'success',
            'data': [self._blood_request_to_dict(req) for req in emergency_requests],
            'count': len(emergency_requests),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_blood_bank_statistics(self) -> Dict:
        """
        Get statistics about blood banks and inventory
        
        Returns:
            Dictionary with statistics
        """
        total_banks = len(self.mock_blood_banks)
        active_banks = len([b for b in self.mock_blood_banks if b.status == 'active'])
        
        total_requests = len(self.mock_requests)
        pending_requests = len([r for r in self.mock_requests if r.status == 'pending'])
        
        # Calculate total blood units across all banks
        total_blood_units = 0
        for bank in self.mock_blood_banks:
            if bank.status == 'active':
                total_blood_units += sum(bank.blood_inventory.values())
        
        return {
            'status': 'success',
            'data': {
                'total_blood_banks': total_banks,
                'active_blood_banks': active_banks,
                'total_blood_units': total_blood_units,
                'total_requests': total_requests,
                'pending_requests': pending_requests,
                'fulfillment_rate': ((total_requests - pending_requests) / total_requests * 100) if total_requests > 0 else 0
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def export_data(self, data_type: str, format: str = 'json') -> Dict:
        """
        Export data from E-RaktKosh in various formats
        
        Args:
            data_type: Type of data to export
            format: Export format (json, csv, excel)
            
        Returns:
            Dictionary with export data
        """
        if data_type == 'blood_banks':
            data = [self._blood_bank_to_dict(bank) for bank in self.mock_blood_banks]
        elif data_type == 'blood_requests':
            data = [self._blood_request_to_dict(req) for req in self.mock_requests]
        elif data_type == 'inventory':
            data = self._get_blood_inventory_summary()
        else:
            return {'error': f'Unknown data type: {data_type}', 'status': 'failed'}
        
        if format.lower() == 'csv':
            # Convert to CSV format
            if isinstance(data, list) and data:
                csv_data = []
                headers = list(data[0].keys())
                csv_data.append(','.join(headers))
                
                for item in data:
                    row = [str(item.get(header, '')) for header in headers]
                    csv_data.append(','.join(row))
                
                return {
                    'status': 'success',
                    'format': 'csv',
                    'data': '\n'.join(csv_data),
                    'filename': f'eraktkosh_{data_type}_{datetime.now().strftime("%Y%m%d")}.csv'
                }
        
        return {
            'status': 'success',
            'format': 'json',
            'data': data,
            'filename': f'eraktkosh_{data_type}_{datetime.now().strftime("%Y%m%d")}.json'
        }
    
    def get_api_status(self) -> Dict:
        """
        Check E-RaktKosh API status and connectivity
        
        Returns:
            Dictionary with API status information
        """
        try:
            # Try to make a simple API call
            response = self._make_api_call('/health', 'GET')
            
            return {
                'status': 'success',
                'api_status': 'connected' if response.get('status') == 'success' else 'error',
                'response_time': time.time() - self.last_api_call,
                'rate_limit_remaining': self.config['rate_limit_per_minute'] - self.api_call_count,
                'mock_mode': self.config['enable_mock_mode'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'api_status': 'disconnected',
                'error': str(e),
                'mock_mode': self.config['enable_mock_mode'],
                'timestamp': datetime.now().isoformat()
            }

def main():
    """Example usage of the E-RaktKosh service"""
    print("E-RaktKosh API Integration Service")
    print("=" * 50)
    
    # Initialize service
    service = ERaktKoshService()
    
    # Test various API endpoints
    print("\n1. Getting blood banks...")
    blood_banks = service.get_blood_banks()
    print(f"Found {blood_banks.get('count', 0)} blood banks")
    
    print("\n2. Getting blood inventory...")
    inventory = service.get_blood_inventory()
    print(f"Inventory summary: {len(inventory.get('data', {}))} blood types")
    
    print("\n3. Getting blood requests...")
    requests = service.get_blood_requests()
    print(f"Found {requests.get('count', 0)} blood requests")
    
    print("\n4. Creating a new blood request...")
    new_request = service.create_blood_request({
        'blood_type': 'A+',
        'units_required': 2,
        'urgency_level': 'HIGH',
        'patient_name': 'Test Patient',
        'hospital_name': 'Test Hospital',
        'contact_number': '+91-9876543210',
        'location': 'Mumbai, India'
    })
    print(f"Request created: {new_request.get('status')}")
    
    print("\n5. Getting emergency requests...")
    emergency = service.get_emergency_blood_requests()
    print(f"Emergency requests: {emergency.get('count', 0)}")
    
    print("\n6. Getting statistics...")
    stats = service.get_blood_bank_statistics()
    print(f"Statistics: {stats.get('data', {})}")
    
    print("\n7. Checking API status...")
    api_status = service.get_api_status()
    print(f"API Status: {api_status.get('api_status')}")
    
    print("\nService testing completed!")

if __name__ == "__main__":
    main()

