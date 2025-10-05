# 🤖 Retell Custom LLM - Developer Guide

## 📖 Overview

This is a **Retell Custom LLM Integration** that allows you to plug your own Large Language Model into the Retell voice AI platform. It acts as a bridge between Retell's voice processing and your custom LLM, enabling fully customizable voice AI agents.

## 🏗️ Architecture

```
┌─────────────────┐    WebSocket     ┌──────────────────┐    API Calls    ┌─────────────────┐
│   Retell Server │ ←──────────────→ │  Your Server     │ ←─────────────→ │  Your LLM       │
│ (Voice Processing)│                 │ (Custom LLM)     │                 │ (OpenAI, etc.)  │
└─────────────────┘                 └──────────────────┘                 └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API Key
- Retell API Key
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/tindevelopers/retell-custom-llm-demo.git
cd retell-custom-llm-python-demo
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Locally
```bash
python -m uvicorn app.server:app --reload --port=8080
```

### 4. Deploy to Cloud
```bash
# Railway
railway up

# Google Cloud Run
gcloud run deploy --source .

# Docker
docker build -t retell-llm .
docker run -p 8080:8080 retell-llm
```

## 🔧 Configuration

### Environment Variables
```env
RETELL_API_KEY=your_retell_api_key
OPENAI_API_KEY=your_openai_api_key
OPENAI_ORGANIZATION_ID=your_org_id  # Optional
```

### Agent Customization
Edit `app/llm.py` to customize your agent:

```python
# Change the agent's role and personality
agent_prompt = """
You are a [YOUR_ROLE] with the following responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

Conversational Style: [Your style guidelines]
Personality: [Your personality traits]
"""

# Change the opening message
begin_sentence = "Hello! How can I help you today?"
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns service status and configuration.

### WebSocket Connection
```http
WS /llm-websocket/{call_id}
```
Real-time communication with Retell for voice conversations.

### Webhook (Optional)
```http
POST /webhook
```
Receives call events from Retell (call_started, call_ended, call_analyzed).

## 🎯 Supported Use Cases

### 1. Customer Service Agent
```python
agent_prompt = """
You are a customer service representative for TechCorp.
Your responsibilities:
- Help customers with technical issues
- Provide product information
- Escalate complex problems
- Maintain a friendly, professional tone

Keep responses under 15 words and always end with a helpful question.
"""
```

### 2. Sales Agent
```python
agent_prompt = """
You are a sales representative for SolarPanels Inc.
Your goals:
- Identify customer needs for solar solutions
- Explain benefits and savings
- Schedule consultations
- Close deals

Be enthusiastic, knowledgeable, and persuasive while being helpful.
"""
```

### 3. Personal Assistant
```python
agent_prompt = """
You are a personal assistant helping with daily tasks.
You can:
- Schedule appointments
- Set reminders
- Answer questions
- Provide information

Be proactive, organized, and always helpful.
"""
```

### 4. Healthcare Support
```python
agent_prompt = """
You are a healthcare support specialist.
Your responsibilities:
- Provide general health information
- Schedule appointments
- Answer insurance questions
- Direct patients to appropriate resources

Always maintain HIPAA compliance and direct serious medical concerns to professionals.
"""
```

### 5. Technical Support
```python
agent_prompt = """
You are a technical support engineer for CloudTech.
Your expertise includes:
- Troubleshooting software issues
- Explaining technical concepts
- Providing step-by-step solutions
- Escalating complex problems

Be patient, clear, and methodical in your explanations.
"""
```

### 6. Educational Tutor
```python
agent_prompt = """
You are an educational tutor specializing in [SUBJECT].
Your approach:
- Break down complex topics
- Provide examples and analogies
- Ask questions to check understanding
- Encourage learning

Adapt your explanations to the student's level and learning style.
"""
```

### 7. Real Estate Agent
```python
agent_prompt = """
You are a real estate agent helping clients find their perfect home.
Your services include:
- Understanding client needs and budget
- Explaining market conditions
- Scheduling property viewings
- Guiding through the buying process

Be knowledgeable about local markets and patient with first-time buyers.
"""
```

### 8. Financial Advisor
```python
agent_prompt = """
You are a financial advisor helping clients with their finances.
Your expertise covers:
- Investment strategies
- Retirement planning
- Budget management
- Insurance needs

Always recommend consulting with licensed professionals for major financial decisions.
"""
```

## 🔄 Integration with Retell

### 1. Connect to Retell Dashboard
1. Go to [Retell Dashboard](https://beta.retellai.com/dashboard)
2. Create a new agent
3. Set Custom LLM URL to: `wss://your-domain.com/llm-websocket`
4. Configure voice settings
5. Test the integration

### 2. WebSocket Protocol
The server communicates with Retell using a specific protocol:

#### Request Types:
- `call_details` - Call metadata
- `ping_pong` - Keep-alive
- `update_only` - Transcript updates
- `response_required` - User needs response
- `reminder_required` - User timeout

#### Response Types:
- `config` - Server configuration
- `response` - Agent response
- `ping_pong` - Keep-alive response

## 🛠️ Development

### Project Structure
```
retell-custom-llm-python-demo/
├── app/
│   ├── server.py          # Main FastAPI server
│   ├── llm.py            # LLM integration (current)
│   ├── llm_with_func_calling.py  # Alternative with functions
│   ├── custom_types.py   # Data models
│   └── claude_with_func_calling.py  # Claude integration
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── railway.json         # Railway deployment config
└── README.md           # This file
```

### Adding New Features

#### 1. Custom LLM Integration
Create a new LLM client in `app/`:

```python
class CustomLlmClient:
    def __init__(self):
        # Initialize your LLM client
        
    async def draft_response(self, request):
        # Implement response generation
        pass
```

#### 2. Function Calling
Use `llm_with_func_calling.py` as a template:

```python
def prepare_functions(self):
    functions = [
        {
            "type": "function",
            "function": {
                "name": "your_function",
                "description": "Function description",
                "parameters": {
                    # Define parameters
                }
            }
        }
    ]
    return functions
```

#### 3. Database Integration
Add database support for call history:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add to server.py
engine = create_engine("sqlite:///calls.db")
SessionLocal = sessionmaker(bind=engine)
```

### Testing

#### 1. Local Testing
```bash
# Test WebSocket connection
python test_websocket.py

# Test health endpoint
curl http://localhost:8080/health
```

#### 2. Integration Testing
```bash
# Test with Retell dashboard
# 1. Deploy to staging environment
# 2. Configure Retell with staging URL
# 3. Make test calls
# 4. Verify responses
```

## 🚀 Deployment Options

### 1. Railway (Recommended for beginners)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### 2. Google Cloud Run (Recommended for production)
```bash
# Install Google Cloud SDK
gcloud run deploy --source .
```

### 3. Docker
```bash
# Build image
docker build -t retell-llm .

# Run container
docker run -p 8080:8080 -e RETELL_API_KEY=your_key retell-llm
```

### 4. AWS Lambda (Serverless)
```bash
# Use Mangum adapter
pip install mangum
# Configure for Lambda deployment
```

## 📊 Monitoring and Debugging

### Health Monitoring
```bash
# Check service health
curl https://your-domain.com/health

# Response format:
{
    "status": "healthy",
    "retell_key_set": true,
    "openai_key_set": true,
    "openai_org_set": true
}
```

### Logging
```python
import logging

# Add to server.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use in your code
logger.info(f"Call started: {call_id}")
```

### Error Handling
```python
try:
    # Your code here
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    # Handle error gracefully
```

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit API keys to version control
- Use `.env` files for local development
- Use cloud provider secret management for production

### 2. Webhook Verification
```python
# Verify Retell webhook signatures
valid_signature = retell.verify(
    json.dumps(post_data),
    api_key=os.environ["RETELL_API_KEY"],
    signature=request.headers.get("X-Retell-Signature")
)
```

### 3. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/webhook")
@limiter.limit("10/minute")
async def handle_webhook(request: Request):
    # Your webhook handler
```

## 📈 Performance Optimization

### 1. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_llm_response(prompt_hash):
    # Cache frequent responses
    pass
```

### 2. Connection Pooling
```python
import asyncio
from aiohttp import ClientSession

# Reuse HTTP connections
async def make_request():
    async with ClientSession() as session:
        # Make requests
        pass
```

### 3. Response Streaming
```python
# Already implemented in llm.py
async for chunk in stream:
    yield ResponseResponse(
        response_id=request.response_id,
        content=chunk.choices[0].delta.content,
        content_complete=False
    )
```

## 🆘 Troubleshooting

### Common Issues

#### 1. "uvicorn: command not found"
```bash
# Solution: Use python -m uvicorn
python -m uvicorn app.server:app --reload --port=8080
```

#### 2. Environment variables not loading
```bash
# Check .env file exists and has correct format
# Ensure no spaces around = sign
RETELL_API_KEY=your_key_here
```

#### 3. WebSocket connection fails
```bash
# Check firewall settings
# Verify WebSocket URL format: wss://domain.com/llm-websocket
# Check server logs for errors
```

#### 4. OpenAI API errors
```bash
# Verify API key is valid
# Check API usage limits
# Ensure organization ID is correct
```

### Debug Mode
```bash
# Run with debug logging
PYTHONPATH=. python -m uvicorn app.server:app --reload --log-level debug
```

## 📚 Additional Resources

- [Retell Documentation](https://docs.retellai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket Protocol Guide](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the Retell documentation
- Contact the development team

---

**Happy coding! 🚀**
