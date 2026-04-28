# AgriGPT Farmer Agent

A FastAPI-based AI assistant for farmers that provides information about crop pests, diseases, and government schemes using Google Gemini AI.

## Features

- **Intelligent Tool Routing**: Automatically detects whether questions are about pests/diseases or government schemes
- **Pest & Disease Database**: Comprehensive information for rice, wheat, tomato, cotton, and maize crops
- **Government Schemes**: Complete database of Indian farmer welfare schemes (PM-KISAN, PMFBY, KCC, etc.)
- **Google Gemini Integration**: Uses Google's Gemini Pro model for natural language responses
- **RESTful API**: Clean FastAPI endpoints for easy integration

## API Endpoints

### POST /chat
Main chat endpoint that intelligently routes questions to appropriate tools.

**Request Body:**
```json
{
  "chatId": "string",
  "phone_number": "string",
  "message": "string",
  "api_key": "string"
}
```

**Response:**
```json
{
  "response": "string",
  "sources": ["simulate_pests"] | ["government_schemes"] | []
}
```

### POST /pests
Direct access to pest and disease information.

**Request Body:**
```json
{
  "query": "What pests affect rice crops?"
}
```

**Response:**
```json
{
  "pest": "Stem Borer (Scirpophaga incertulas)",
  "details": "Symptoms: Causes 'dead heart'... Control measures: carbofuran 3G..."
}
```

### POST /schemes
Direct access to government scheme information.

**Request Body:**
```json
{
  "query": "What is PM-KISAN scheme?"
}
```

**Response:**
```json
{
  "scheme": "PM-KISAN",
  "details": "Benefit: Rs 6,000 per year... Eligibility: All small and marginal..."
}
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get Google Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

3. **Run locally:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

**For Render deployment, use start command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Deployment on Render

1. **Push to GitHub:**
```bash
git add .
git commit -m "Implement AgriGPT FastAPI application"
git push origin main
```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Choose "Web Service"
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `./start.sh` or `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Deploy!

3. **Verify Deployment:**
   - Visit `https://your-app-name.onrender.com/docs` to see Swagger UI
   - Test the `/chat` endpoint with sample requests

## Example Usage

### Pest Question:
```bash
curl -X POST "https://your-app.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "test123",
    "phone_number": "9876543210",
    "message": "What pests affect rice crops?",
    "api_key": "YOUR_GEMINI_API_KEY"
  }'
```

Response:
```json
{
  "response": "Rice crops are commonly affected by several pests including stem borers, brown planthoppers, and gall midges...",
  "sources": ["simulate_pests"]
}
```

### Government Scheme Question:
```bash
curl -X POST "https://your-app.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "test123",
    "phone_number": "9876543210",
    "message": "Tell me about PM-KISAN scheme",
    "api_key": "YOUR_GEMINI_API_KEY"
  }'
```

Response:
```json
{
  "response": "PM-KISAN provides Rs 6,000 per year to eligible farmer families...",
  "sources": ["government_schemes"]
}
```

## Knowledge Bases

### Pests & Diseases
- **Rice**: Stem borer, brown planthopper, gall midge, leaf folder, blast, bacterial blight, sheath blight, brown spot
- **Wheat**: Aphids, termites, yellow rust, brown rust, loose smut, karnal bunt
- **Tomato**: Fruit borer, whitefly, leaf miner, early blight, late blight, leaf curl virus, fusarium wilt
- **Cotton**: Pink bollworm, American bollworm, sucking pests, mealy bug, leaf curl disease, bacterial blight
- **Maize**: Fall armyworm, stem borer, turcicum leaf blight, maydis leaf blight

### Government Schemes
- PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)
- PMFBY (PM Fasal Bima Yojana)
- KCC (Kisan Credit Card)
- Soil Health Card Scheme
- PM Kisan Maan Dhan Yojana
- NMSA (National Mission for Sustainable Agriculture)
- Per Drop More Crop (Micro Irrigation)
- eNAM (National Agriculture Market)
- RKVY (Rashtriya Krishi Vikas Yojana)
- Agri Infrastructure Fund

## Architecture

- **FastAPI**: Modern Python web framework
- **Google Gemini**: AI model for natural language processing
- **Pydantic**: Data validation and serialization
- **Knowledge Bases**: Structured data for pests and government schemes
- **Tool Routing**: Intelligent detection of question intent

## Testing

The application includes comprehensive knowledge bases and handles various farmer questions. Test with different crops and schemes to ensure proper routing and responses.
