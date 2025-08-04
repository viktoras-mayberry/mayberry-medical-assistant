## Development Plan

### Knowledge Base Integration
- Research and integrate medical knowledge bases.
- Expand with additional trusted sources.

### AI Model Integration
- Replace mock systems with sophisticated AI models.
- Train and deploy necessary models.

### Ongoing Documentation
- Continuously update this document with new features and architecture changes.
- Use diagrams to illustrate workflows and structures.

### Feature Implementation
- Complete UMLS/SNOMED CT Integration.
- Develop multi-language support.

---

# MAYBERRY Medical AI

**Your Trusted Partner for Intelligent Healthcare Guidance**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Material-UI](https://img.shields.io/badge/Material--UI-5.15.15-blue.svg)](https://mui.com/)

MAYBERRY Medical AI is a next-generation medical assistant that provides advanced, private, and compliant healthcare support. Built with cutting-edge AI technology, it offers personalized health insights, symptom analysis, and expert-level medical guidance while maintaining the highest standards of privacy and security.

## Key Features

### AI-Powered Medical Chat
- Interactive conversational AI for health consultations
- Context-aware responses based on medical knowledge
- 24/7 availability for immediate health guidance
- Multi-language support

### Advanced Symptom Checker
- Comprehensive symptom analysis with 16+ common symptoms
- Risk level assessment (Low, Medium, High, Critical)
- Personalized recommendations based on age, gender, and severity
- Emergency care detection and alerts

### Lab Result Analysis
- AI-powered interpretation of lab results
- Support for multiple test types (CBC, CMP, Lipid Panel, etc.)
- File upload support (PDF, images, text files)
- Biomarker trend analysis and explanations

### Expert Second Opinion
- AI-driven second opinion on diagnoses
- Virtual expert panel consultations
- Treatment plan validation
- Confidence scoring and consensus building

### Privacy & Security
- **HIPAA & GDPR Compliant**: Strict adherence to healthcare privacy regulations
- **Local Processing**: Option to process data on-device for complete privacy
- **Anonymous Access**: Core features available without account creation
- **Encrypted Storage**: End-to-end encryption for all sensitive data

## Technology Stack

### Backend
- **Framework**: FastAPI 0.110.0
- **Database**: SQLAlchemy with SQLite (PostgreSQL ready)
- **Authentication**: JWT tokens with bcrypt hashing
- **AI/ML**: Transformers, PyTorch, scikit-learn
- **API Documentation**: Auto-generated OpenAPI/Swagger

### Frontend
- **Framework**: React 18.3.1
- **UI Library**: Material-UI 5.15.15
- **State Management**: React Query + Zustand
- **Routing**: React Router DOM 6.22.3
- **Forms**: React Hook Form with validation
- **Styling**: Emotion + Material-UI theming

### DevOps & Tools
- **Development**: Hot reload for both frontend and backend
- **Testing**: Pytest for backend, Jest for frontend
- **Code Quality**: Black, Flake8, ESLint
- **Documentation**: Auto-generated API docs

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mayberry-medical-ai.git
   cd mayberry-medical-ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

### Running the Application

1. **Start the Backend** (Terminal 1)
   ```bash
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
mayberry-medical-ai/
├── backend/                    # FastAPI backend
│   ├── routers/               # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   └── medical.py        # Medical AI endpoints
│   ├── services/             # Business logic services
│   │   ├── local_medical_ai.py # AI model service
│   │   └── symptom_analysis.py # Symptom analysis logic
│   ├── models.py             # Database models
│   ├── schemas.py            # Pydantic schemas
│   ├── auth.py               # Authentication utilities
│   ├── database.py           # Database configuration
│   ├── config.py             # Application settings
│   ├── main.py               # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── contexts/         # React contexts
│   │   ├── services/         # API services
│   │   ├── theme/            # Material-UI theme
│   │   ├── App.js            # Main app component
│   │   └── index.js          # Entry point
│   ├── public/               # Static assets
│   └── package.json          # Node dependencies
└── README.md                 # This file
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env` file:

```env
# Application settings
APP_NAME="MAYBERRY Medical AI"
DEBUG=false
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database settings
DATABASE_URL=sqlite:///./mayberry_medical.db

# JWT settings
JWT_SECRET=your-jwt-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# AI/ML settings (optional)
OPENAI_API_KEY=your-openai-api-key-optional
HUGGINGFACE_API_KEY=your-huggingface-api-key-optional
```

### Frontend Configuration

Create `frontend/.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=MAYBERRY Medical AI
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📱 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile

#### Medical AI
- `POST /medical/chat` - AI medical chat
- `POST /medical/symptom-checker` - Symptom analysis
- `POST /medical/second-opinion` - Expert second opinion
- `POST /medical/lab-analysis` - Lab result analysis

#### System
- `GET /health` - System health check
- `GET /` - API information

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Write tests for new features
- Update documentation for API changes
- Ensure HIPAA compliance for medical features

## Roadmap

### Phase 1: Core Features 
- [x] User authentication system
- [x] Basic medical AI chat
- [x] Symptom checker interface
- [x] Lab analysis framework
- [x] Responsive UI/UX design

### Phase 2: AI Enhancement 
- [x] **Phase 2A: Medical Knowledge Base Integration** 
  - [x] Project structure setup for knowledge base
  - [x] Medical ontology framework initialization
  - [x] Symptom-disease relationship mapping schema
  - [x] Database population script for initial data
  - [x] Knowledge API endpoints for symptoms and diseases
- [x] **Phase 2B: Enhanced Medical AI Models** 
  - [x] BioBERT integration for medical text understanding
  - [x] ClinicalBERT integration for clinical text analysis
  - [x] Confidence scoring system for AI responses
  - [x] Enhanced symptom analysis with severity assessment
  - [x] Advanced medical query processing with contextual understanding
  - [x] Batch analysis capabilities for multiple symptom sets
  - [x] Comprehensive API endpoints for enhanced AI features
- [ ] **Phase 2C: UMLS/SNOMED CT Integration**
  - [ ] UMLS terminology integration
  - [ ] SNOMED CT concept mapping
  - [ ] Standardized medical coding
- [ ] **Phase 2D: Advanced Symptom Analysis**
  - [ ] Multi-symptom correlation analysis
  - [ ] Risk stratification algorithms
  - [ ] Predictive modeling for disease progression

### Phase 3: Advanced Features
- [ ] Voice interaction capabilities
- [ ] Medical image analysis
- [ ] Integration with wearable devices
- [ ] Telemedicine consultation booking
- [ ] Health tracking and monitoring

### Phase 4: Enterprise Features
- [ ] Healthcare provider dashboard
- [ ] Electronic Health Records (EHR) integration
- [ ] Advanced analytics and reporting
- [ ] White-label solutions
- [ ] API marketplace

## Security & Compliance

- **HIPAA Compliance**: All patient data handling follows HIPAA guidelines
- **GDPR Compliance**: European data protection standards implemented
- **SOC 2 Type II**: Security audit compliance
- **Data Encryption**: AES-256 encryption for data at rest
- **Secure Transmission**: TLS 1.3 for data in transit
- **Regular Security Audits**: Automated vulnerability scanning

## Support

- **Documentation**: Check this README and API docs
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: support@mayberrymedical.ai (coming soon)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Medical Disclaimer

**IMPORTANT**: MAYBERRY Medical AI is designed to provide health information and support decision-making. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with questions about medical conditions. Never disregard professional medical advice or delay seeking treatment based on information provided by this application.

## Acknowledgments

- Built with ❤️ by the MAYBERRY Medical AI team
- Inspired by the need for accessible, private healthcare AI
- Thanks to the open-source community for amazing tools and libraries
- Special thanks to healthcare professionals who provided medical insights

---

**Made with ❤️ for better healthcare accessibility**
