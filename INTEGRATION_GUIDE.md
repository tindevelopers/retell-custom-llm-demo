# 🔌 Integration Guide - Connecting to Retell Custom LLM

## 🎯 Quick Integration Checklist

### ✅ Prerequisites
- [ ] Retell API Key
- [ ] OpenAI API Key (or your preferred LLM)
- [ ] WebSocket-capable server
- [ ] Domain with SSL certificate

### ✅ Deployment Options
- [ ] **Railway** (Easiest) - `railway up`
- [ ] **Google Cloud Run** (Recommended) - `gcloud run deploy`
- [ ] **AWS Lambda** (Serverless) - Requires Mangum adapter
- [ ] **Docker** (Any platform) - `docker run`
- [ ] **Heroku** - Standard deployment
- [ ] **Vercel** - Serverless functions

## 🚀 Step-by-Step Integration

### Step 1: Deploy Your Custom LLM Server

#### Option A: Railway (5 minutes)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway up

# 3. Set environment variables
railway variables set RETELL_API_KEY=your_key
railway variables set OPENAI_API_KEY=your_key
```

#### Option B: Google Cloud Run (10 minutes)
```bash
# 1. Install Google Cloud SDK
gcloud auth login
gcloud config set project your-project

# 2. Deploy
gcloud run deploy retell-llm --source . --allow-unauthenticated

# 3. Set environment variables
gcloud run services update retell-llm --set-env-vars="RETELL_API_KEY=your_key,OPENAI_API_KEY=your_key"
```

#### Option C: Docker (Anywhere)
```bash
# 1. Build image
docker build -t retell-llm .

# 2. Run container
docker run -p 8080:8080 \
  -e RETELL_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  retell-llm
```

### Step 2: Get Your WebSocket URL

After deployment, your WebSocket URL will be:
- **Railway**: `wss://your-app-name.up.railway.app/llm-websocket`
- **Google Cloud Run**: `wss://your-service-hash.region.run.app/llm-websocket`
- **Custom Domain**: `wss://yourdomain.com/llm-websocket`

### Step 3: Configure Retell Dashboard

1. Go to [Retell Dashboard](https://beta.retellai.com/dashboard)
2. Click "Create Agent"
3. Select "Custom LLM"
4. Enter your WebSocket URL: `wss://your-domain.com/llm-websocket`
5. Configure voice settings
6. Test the connection

### Step 4: Test Your Integration

```bash
# Test health endpoint
curl https://your-domain.com/health

# Expected response:
{
    "status": "healthy",
    "retell_key_set": true,
    "openai_key_set": true,
    "openai_org_set": true
}
```

## 🎨 Customizing Your Agent

### Basic Customization

Edit `app/llm.py` to customize your agent:

```python
# Change the agent's role
agent_prompt = """
You are a [YOUR_ROLE] with these responsibilities:
- Handle customer inquiries
- Provide accurate information
- Escalate complex issues
- Maintain professional tone

Keep responses under 20 words and always be helpful.
"""

# Change the opening message
begin_sentence = "Hello! I'm your [ROLE], how can I help you today?"
```

### Advanced Customization

#### 1. Function Calling
Use `app/llm_with_func_calling.py` for advanced capabilities:

```python
def prepare_functions(self):
    functions = [
        {
            "type": "function",
            "function": {
                "name": "check_inventory",
                "description": "Check product availability",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"}
                    }
                }
            }
        }
    ]
    return functions
```

#### 2. Custom LLM Integration
Replace OpenAI with your preferred LLM:

```python
class CustomLlmClient:
    def __init__(self):
        # Initialize your LLM client
        self.client = YourLlmClient(api_key="your_key")
    
    async def draft_response(self, request):
        # Implement your LLM logic
        response = await self.client.generate(
            prompt=self.prepare_prompt(request)
        )
        return response
```

#### 3. Database Integration
Add persistent storage:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add to server.py
engine = create_engine("postgresql://user:pass@host/db")
SessionLocal = sessionmaker(bind=engine)

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Store call data
    db = SessionLocal()
    # Save call information
    db.commit()
```

## 🔧 Platform-Specific Configurations

### Railway Configuration
Create `railway.json`:
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

### Google Cloud Run Configuration
Create `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/retell-llm', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/retell-llm']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'retell-llm', '--image', 'gcr.io/$PROJECT_ID/retell-llm', '--region', 'us-central1']
```

### AWS Lambda Configuration
Create `lambda_handler.py`:
```python
from mangum import Mangum
from app.server import app

handler = Mangum(app, lifespan="off")
```

### Heroku Configuration
Create `Procfile`:
```
web: uvicorn app.server:app --host 0.0.0.0 --port $PORT
```

## 📊 Monitoring and Analytics

### Health Monitoring
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": get_uptime(),
        "calls_processed": get_call_count()
    }
```

### Call Analytics
```python
@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    
    if data["event"] == "call_ended":
        # Analyze call performance
        duration = data["call_duration"]
        satisfaction = data.get("satisfaction_score")
        
        # Store analytics
        store_call_analytics(data)
```

### Error Tracking
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)

# Automatic error tracking
```

## 🔒 Security Considerations

### 1. API Key Management
```python
import os
from cryptography.fernet import Fernet

# Encrypt sensitive data
def encrypt_api_key(key: str) -> str:
    fernet = Fernet(os.environ["ENCRYPTION_KEY"])
    return fernet.encrypt(key.encode()).decode()
```

### 2. Webhook Verification
```python
import hmac
import hashlib

def verify_retell_signature(payload: str, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### 3. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.websocket("/llm-websocket/{call_id}")
@limiter.limit("10/minute")
async def websocket_endpoint(websocket: WebSocket, call_id: str):
    # Your WebSocket handler
```

## 🚀 Performance Optimization

### 1. Connection Pooling
```python
import asyncio
from aiohttp import ClientSession

# Reuse HTTP connections
async def make_llm_request(session: ClientSession, prompt: str):
    async with session.post('/v1/chat/completions', json={
        'model': 'gpt-4',
        'messages': [{'role': 'user', 'content': prompt}]
    }) as response:
        return await response.json()
```

### 2. Caching
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def get_cached_response(prompt_hash: str):
    # Cache frequent responses
    return generate_response(prompt_hash)

def hash_prompt(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()
```

### 3. Streaming Responses
```python
async def stream_response(request: ResponseRequiredRequest):
    async for chunk in llm_stream:
        yield ResponseResponse(
            response_id=request.response_id,
            content=chunk.choices[0].delta.content,
            content_complete=False
        )
    
    # Final response
    yield ResponseResponse(
        response_id=request.response_id,
        content="",
        content_complete=True
    )
```

## 🧪 Testing Your Integration

### 1. Unit Tests
```python
import pytest
from app.llm import LlmClient

@pytest.mark.asyncio
async def test_llm_response():
    client = LlmClient()
    request = ResponseRequiredRequest(
        response_id=1,
        transcript="Hello, how are you?",
        call_id="test-call"
    )
    
    response = await client.draft_response(request)
    assert response.response_type == "response"
    assert len(response.content) > 0
```

### 2. Integration Tests
```python
import asyncio
import websockets

async def test_websocket_connection():
    uri = "wss://localhost:8080/llm-websocket/test-call"
    
    async with websockets.connect(uri) as websocket:
        # Send test message
        await websocket.send(json.dumps({
            "response_type": "response_required",
            "response_id": 1,
            "transcript": "Hello"
        }))
        
        # Receive response
        response = await websocket.recv()
        assert "response" in response
```

### 3. Load Testing
```python
import asyncio
import aiohttp

async def load_test():
    tasks = []
    for i in range(100):
        task = asyncio.create_task(test_call())
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    print(f"Completed {len(results)} calls")
```

## 🆘 Troubleshooting

### Common Issues and Solutions

#### 1. WebSocket Connection Fails
**Problem**: `WebSocket connection failed`
**Solutions**:
- Check firewall settings
- Verify SSL certificate
- Ensure WebSocket URL format: `wss://domain.com/llm-websocket`
- Check server logs for errors

#### 2. Environment Variables Not Loading
**Problem**: `Environment variables not found`
**Solutions**:
- Verify `.env` file exists
- Check variable names (case-sensitive)
- Ensure no spaces around `=` sign
- Restart server after changes

#### 3. OpenAI API Errors
**Problem**: `OpenAI API error`
**Solutions**:
- Verify API key is valid
- Check API usage limits
- Ensure organization ID is correct
- Check network connectivity

#### 4. Slow Response Times
**Problem**: `Response time > 5 seconds`
**Solutions**:
- Enable response streaming
- Implement caching
- Use faster LLM models
- Optimize prompt length

### Debug Mode
```bash
# Enable debug logging
export DEBUG=1
python -m uvicorn app.server:app --reload --log-level debug

# Check logs
tail -f logs/app.log
```

## 📈 Scaling Your Integration

### Horizontal Scaling
```python
# Load balancer configuration
upstream retell_backend {
    server app1.example.com:8080;
    server app2.example.com:8080;
    server app3.example.com:8080;
}
```

### Vertical Scaling
```python
# Increase resources
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### Auto-scaling
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: retell-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: retell-llm
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 📚 Additional Resources

- [Retell Documentation](https://docs.retellai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FastAPI WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)
- [WebSocket Protocol RFC](https://tools.ietf.org/html/rfc6455)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Ready to build amazing voice AI experiences! 🚀**
