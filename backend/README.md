# ThalaNet Emergency Blood Management Platform - Backend

A comprehensive backend system for emergency blood management with ML-powered donor prediction, intelligent patient-donor matching, and real-time emergency notifications.

## 🚀 Features

### Core Functionality
- **Synthetic Dataset Generation**: Realistic blood donation data for development and testing
- **ML-Powered Donor Prediction**: Predicts donor availability using Random Forest, Gradient Boosting, and Logistic Regression
- **Intelligent Patient-Donor Matching**: Location-based matching with urgency prioritization
- **Emergency Notification System**: Real-time alerts for critical blood requests
- **AI WhatsApp Chatbot**: Intelligent responses with patient matching and donation history
- **E-RaktKosh API Integration**: Government blood bank data integration (mock implementation)
- **Data Privacy & Security**: Encryption, data masking, and security audit logging

### Technical Features
- **Modular Architecture**: Clean separation of concerns with easy dataset replacement
- **Python ML Backend**: Scikit-learn and TensorFlow integration
- **Node.js API Server**: Express.js with security middleware
- **Real-time Processing**: Async notification system with rate limiting
- **Comprehensive Testing**: Full pipeline testing and validation
- **Production Ready**: Security headers, CORS, compression, and logging

## 🏗️ Architecture

```
backend/
├── src/
│   ├── utils/           # Data generation utilities
│   ├── ml/             # Machine learning models
│   ├── services/       # Business logic services
│   ├── security/       # Privacy and security modules
│   ├── routes/         # API route handlers
│   └── index.js        # Main server entry point
├── data/               # Generated datasets
├── models/             # Trained ML models
├── results/            # Training and testing results
├── package.json        # Node.js dependencies
└── requirements.txt    # Python dependencies
```

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control
- **8GB+ RAM** for ML model training
- **2GB+ free disk space**

### Python Dependencies
- scikit-learn, pandas, numpy
- TensorFlow (optional)
- geopy for geospatial calculations
- cryptography for security features

### Node.js Dependencies
- Express.js for web server
- Security middleware (helmet, cors, rate-limit)
- Logging and monitoring tools

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### 2. Generate Synthetic Data
```bash
# Generate realistic datasets for development
python src/utils/syntheticDataGenerator.py

# This creates:
# - data/donors.csv (1000 donor records)
# - data/patients.csv (500 patient records)
# - data/emergency_requests.csv (200 emergency requests)
# - data/historical_donations.csv (5000 donation records)
```

### 3. Train ML Models
```bash
# Train all ML models and test the complete system
python src/ml/trainModels.py

# This will:
# - Train donor prediction models
# - Test patient-donor matching
# - Validate emergency notification system
# - Test chatbot and security modules
# - Generate comprehensive reports
```

### 4. Start Backend Server
```bash
# Start the Node.js API server
npm run dev

# Server runs on http://localhost:5000
# Health check: http://localhost:5000/health
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Security Settings
JWT_SECRET=your_jwt_secret_here
ENCRYPTION_KEY=your_encryption_key_here

# Database Configuration (for production)
MONGODB_URI=mongodb://localhost:27017/thalanet
REDIS_URL=redis://localhost:6379

# External APIs
ERAKTKOSH_API_KEY=your_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

### Python Configuration
Modify configuration in individual modules or create a `config.py` file:

```python
# Example configuration
ML_CONFIG = {
    'model_types': ['random_forest', 'gradient_boosting', 'logistic'],
    'cross_validation_folds': 5,
    'test_size': 0.2,
    'random_state': 42
}

SECURITY_CONFIG = {
    'encryption_algorithm': 'AES-256',
    'key_derivation_rounds': 100000,
    'enable_audit_logging': True,
    'data_retention_days': 365
}
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

### Donors
- `GET /api/donors` - List all donors
- `GET /api/donors/:id` - Get donor details
- `POST /api/donors` - Create new donor
- `PUT /api/donors/:id` - Update donor
- `DELETE /api/donors/:id` - Delete donor

### Patients
- `GET /api/patients` - List all patients
- `GET /api/patients/:id` - Get patient details
- `POST /api/patients` - Create new patient
- `PUT /api/patients/:id` - Update patient

### Emergency Requests
- `GET /api/emergency-requests` - List emergency requests
- `POST /api/emergency-requests` - Create emergency request
- `PUT /api/emergency-requests/:id/status` - Update request status
- `GET /api/emergency-requests/urgent` - Get urgent requests

### Matching System
- `POST /api/matching/find-donors` - Find matching donors for patient
- `GET /api/matching/statistics` - Get matching statistics
- `POST /api/matching/emergency-match` - Emergency donor matching

### Notifications
- `POST /api/notifications/send` - Send notification
- `GET /api/notifications/history` - Get notification history
- `POST /api/notifications/subscribe` - Subscribe to notifications

### Chatbot
- `POST /api/chatbot/process` - Process WhatsApp message
- `GET /api/chatbot/conversations` - Get conversation history
- `POST /api/chatbot/emergency` - Handle emergency chatbot requests

### Analytics
- `GET /api/analytics/dashboard` - Dashboard statistics
- `GET /api/analytics/blood-availability` - Blood availability trends
- `GET /api/analytics/donor-predictions` - ML model predictions

## 🤖 Machine Learning Models

### Donor Prediction Model
The system trains multiple ML models to predict donor availability:

```python
from ml.donorPredictionModel import DonorPredictionModel

# Initialize model
model = DonorPredictionModel(model_type='random_forest')

# Train model
results = model.train(training_data)

# Make predictions
predictions = model.predict(donor_features)
```

**Features Used:**
- Age, gender, blood type
- Last donation date
- Health conditions
- Historical donation frequency
- Responsiveness score
- Location data

**Model Types:**
- **Random Forest**: Best overall performance, handles non-linear relationships
- **Gradient Boosting**: High accuracy, good for complex patterns
- **Logistic Regression**: Fast, interpretable, baseline model

### Patient-Donor Matching
Intelligent matching algorithm considering:

```python
from ml.patientDonorMatching import PatientDonorMatching

# Initialize matching system
matcher = PatientDonorMatching()

# Find matches for patient
matches = matcher.find_matches(patient_data, donors_data)

# Emergency matching
emergency_matches = matcher.find_emergency_matches(emergency_request, donors_data)
```

**Matching Criteria:**
- Blood type compatibility
- Location proximity (geodesic distance)
- Urgency level prioritization
- ML-predicted availability score
- Health condition filtering
- Historical responsiveness

## 🔒 Security Features

### Data Encryption
- AES-256 encryption for sensitive data
- Secure key derivation using PBKDF2
- Encrypted storage of PII fields

### Data Masking
- Phone numbers: +91-987***3210
- Email addresses: jo***@example.com
- Names: J*** Doe
- Addresses: Partial masking for privacy

### Security Audit
- Comprehensive event logging
- Login attempts tracking
- Password change monitoring
- API access logging

### Input Validation
- SQL injection prevention
- XSS protection
- Input sanitization
- Rate limiting

## 📈 Performance Optimization

### ML Model Optimization
- Feature engineering for better predictions
- Cross-validation for model selection
- Hyperparameter tuning capabilities
- Model persistence and caching

### API Performance
- Response compression
- Database query optimization
- Caching strategies
- Async processing for notifications

### Scalability
- Modular architecture for easy scaling
- Stateless API design
- Horizontal scaling support
- Load balancing ready

## 🧪 Testing

### Automated Testing
```bash
# Run Python tests
python -m pytest tests/

# Run Node.js tests
npm test

# Run complete system test
python src/ml/trainModels.py
```

### Manual Testing
```bash
# Test individual components
python src/utils/syntheticDataGenerator.py
python src/ml/donorPredictionModel.py
python src/services/emergencyNotificationService.py

# Test API endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/donors
```

## 📊 Monitoring and Logging

### Log Files
- `training.log` - ML model training logs
- `server.log` - API server logs
- `security.log` - Security audit logs
- `error.log` - Error tracking

### Metrics
- API response times
- ML model accuracy scores
- Emergency response times
- System uptime and health

## 🚀 Deployment

### Development
```bash
npm run dev          # Start development server
python -m flask run  # Start Python services
```

### Production
```bash
npm start            # Start production server
pm2 start ecosystem.config.js  # Process management
```

### Docker (Optional)
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

## 🔄 Data Pipeline

### 1. Data Generation
```python
# Generate synthetic data
generator = SyntheticDataGenerator(seed=42)
datasets = generator.save_datasets("data/")
```

### 2. Model Training
```python
# Train ML models
trainer = ThalaNetModelTrainer()
results = trainer.run_complete_training()
```

### 3. Real-time Processing
```python
# Process emergency requests
emergency_service = EmergencyNotificationService()
emergency_service.process_emergency_requests(requests, donors)
```

### 4. API Integration
```javascript
// Handle API requests
app.post('/api/emergency-requests', async (req, res) => {
  const result = await emergencyService.createRequest(req.body);
  res.json(result);
});
```

## 🔧 Customization

### Adding New ML Models
```python
# Extend the base model class
class CustomMLModel(DonorPredictionModel):
    def __init__(self):
        super().__init__('custom')
    
    def train(self, data):
        # Custom training logic
        pass
```

### Custom Matching Algorithms
```python
# Extend matching system
class CustomMatching(PatientDonorMatching):
    def calculate_matching_score(self, patient, donor, distance):
        # Custom scoring logic
        return custom_score
```

### New Notification Channels
```python
# Add new notification method
def send_telegram_notification(self, message, alert, matched_donors):
    # Telegram integration logic
    pass
```

## 📚 API Documentation

### Request/Response Examples

**Create Emergency Request:**
```json
POST /api/emergency-requests
{
  "blood_type_needed": "A+",
  "urgency_level": "CRITICAL",
  "units_required": 2,
  "patient_name": "John Doe",
  "hospital_name": "City Hospital",
  "contact_number": "+91-9876543210",
  "location": "Mumbai, India"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "request_id": "REQ_000001",
    "status": "active",
    "matched_donors": 5,
    "estimated_response_time": "2 hours"
  }
}
```

## 🆘 Troubleshooting

### Common Issues

**Python Import Errors:**
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/backend/src"
```

**ML Model Training Failures:**
```bash
# Check data quality
python -c "import pandas as pd; df = pd.read_csv('data/donors.csv'); print(df.info())"

# Verify dependencies
pip list | grep -E "(scikit-learn|pandas|numpy)"
```

**API Server Issues:**
```bash
# Check logs
tail -f logs/server.log

# Verify environment
echo $NODE_ENV
echo $PORT
```

### Performance Issues
- Increase Node.js memory limit: `node --max-old-space-size=4096`
- Optimize ML model parameters
- Use database indexing for large datasets
- Implement caching strategies

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Code Standards
- Python: PEP 8 compliance
- JavaScript: ESLint configuration
- Documentation: Comprehensive docstrings
- Testing: 90%+ code coverage

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Blood donation organizations worldwide
- Open source ML community
- Healthcare technology innovators
- Emergency response professionals

## 📞 Support

### Documentation
- [API Reference](docs/api.md)
- [ML Model Guide](docs/ml-models.md)
- [Deployment Guide](docs/deployment.md)

### Community
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discussions](https://github.com/your-repo/discussions)
- [Wiki](https://github.com/your-repo/wiki)

### Contact
- **Email**: support@thalanet.org
- **GitHub**: [@thalanet-team](https://github.com/thalanet-team)
- **Documentation**: [docs.thalanet.org](https://docs.thalanet.org)

---

**Built with ❤️ for saving lives through better blood management**

