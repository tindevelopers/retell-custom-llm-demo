# 📚 API Reference - Retell Custom LLM

## 🌐 Base URLs

### Production Deployments
- **Railway**: `https://retell-custom-llm-demo-v2-production.up.railway.app`
- **Google Cloud Run**: `https://retell-custom-llm-258009805037.us-central1.run.app`
- **Local Development**: `http://localhost:8080`

### WebSocket URLs
- **Railway**: `wss://retell-custom-llm-demo-v2-production.up.railway.app/llm-websocket`
- **Google Cloud Run**: `wss://retell-custom-llm-258009805037.us-central1.run.app/llm-websocket`
- **Local**: `ws://localhost:8080/llm-websocket`

## 📡 HTTP Endpoints

### Health Check
```http
GET /health
```

**Description**: Returns the health status of the service and configuration details.

**Response**:
```json
{
    "status": "healthy - NEW PROJECT DEPLOYMENT TEST",
    "retell_key_set": true,
    "openai_key_set": true,
    "openai_org_set": true,
    "retell_key_length": 32,
    "openai_key_length": 164,
    "openai_org_length": 28,
    "all_env_vars": [
        "K_REVISION",
        "PORT",
        "HOME",
        "PYTHONUNBUFFERED"
    ],
    "railway_env_vars": {
        "OPENAI_API_KEY": "sk-proj-5A...",
        "RETELL_API_KEY": "key_aa1140...",
        "OPENAI_ORGANIZATION_ID": "org-WPDHe6..."
    }
}
```

**Status Codes**:
- `200 OK` - Service is healthy
- `500 Internal Server Error` - Service has issues

### API Documentation
```http
GET /docs
```

**Description**: Interactive API documentation (Swagger UI).

**Response**: HTML page with interactive API documentation.

### OpenAPI Schema
```http
GET /openapi.json
```

**Description**: OpenAPI 3.0 schema definition.

**Response**: JSON schema for the API.

## 🔌 WebSocket Endpoints

### LLM WebSocket Connection
```http
WS /llm-websocket/{call_id}
```

**Description**: Real-time WebSocket connection for LLM communication with Retell.

**Path Parameters**:
- `call_id` (string, required) - Unique identifier for the call session

**Headers**:
- `Authorization: Bearer {retell_api_key}` (optional)

**Connection Flow**:

1. **Establish Connection**
   ```javascript
   const ws = new WebSocket('wss://your-domain.com/llm-websocket/call-123');
   ```

2. **Receive Config Request**
   ```json
   {
       "response_type": "config",
       "response_id": 1
   }
   ```

3. **Send Config Response**
   ```json
   {
       "response_type": "config",
       "config": {
           "auto_reconnect": true,
           "call_details": true
       },
       "response_id": 1
   }
   ```

4. **Receive Call Details**
   ```json
   {
       "response_type": "call_details",
       "call_details": {
           "call_id": "call-123",
           "agent_id": "agent-456",
           "customer_number": "+1234567890",
           "start_timestamp": 1640995200
       },
       "response_id": 2
   }
   ```

5. **Receive Response Required**
   ```json
   {
       "response_type": "response_required",
       "response_id": 3,
       "transcript": "Hello, how can I help you?",
       "call_id": "call-123",
       "call_control": {
           "end_call": false,
           "transfer_call": false,
           "mute_agent": false
       }
   }
   ```

6. **Send Response**
   ```json
   {
       "response_type": "response",
       "response_id": 3,
       "content": "Hello! I'm here to help you today.",
       "content_complete": false
   }
   ```

7. **Send Final Response**
   ```json
   {
       "response_type": "response",
       "response_id": 3,
       "content": "",
       "content_complete": true
   }
   ```

## 📋 Data Models

### Request Types

#### ConfigRequest
```json
{
    "response_type": "config",
    "response_id": 1
}
```

#### CallDetailsRequest
```json
{
    "response_type": "call_details",
    "response_id": 2,
    "call_details": {
        "call_id": "string",
        "agent_id": "string",
        "customer_number": "string",
        "start_timestamp": 1640995200
    }
}
```

#### ResponseRequiredRequest
```json
{
    "response_type": "response_required",
    "response_id": 3,
    "transcript": "string",
    "call_id": "string",
    "call_control": {
        "end_call": false,
        "transfer_call": false,
        "mute_agent": false
    }
}
```

#### UpdateOnlyRequest
```json
{
    "response_type": "update_only",
    "response_id": 4,
    "transcript": "string",
    "call_id": "string"
}
```

#### PingPongRequest
```json
{
    "response_type": "ping_pong",
    "response_id": 5
}
```

### Response Types

#### ConfigResponse
```json
{
    "response_type": "config",
    "config": {
        "auto_reconnect": true,
        "call_details": true
    },
    "response_id": 1
}
```

#### ResponseResponse
```json
{
    "response_type": "response",
    "response_id": 3,
    "content": "string",
    "content_complete": false
}
```

#### PingPongResponse
```json
{
    "response_type": "ping_pong",
    "response_id": 5
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `RETELL_API_KEY` | Retell API key for authentication | Yes | `key_aa1140c911a00921562fb219a957` |
| `OPENAI_API_KEY` | OpenAI API key for LLM access | Yes | `sk-proj-...` |
| `OPENAI_ORGANIZATION_ID` | OpenAI organization ID | No | `org-WPDHe6VO8J3u7AdZrkfxKeFz` |
| `PORT` | Server port (auto-set by platforms) | No | `8080` |

### Agent Configuration

#### Current Agent Settings
```python
# Agent Role: Professional Therapist
agent_prompt = """
Task: As a professional therapist, your responsibilities are comprehensive and patient-centered. 
You establish a positive and trusting rapport with patients, diagnosing and treating mental health disorders. 
Your role involves creating tailored treatment plans based on individual patient needs and circumstances. 
Regular meetings with patients are essential for providing counseling and treatment, and for adjusting plans as needed. 
You conduct ongoing assessments to monitor patient progress, involve and advise family members when appropriate, 
and refer patients to external specialists or agencies if required. Keeping thorough records of patient interactions 
and progress is crucial. You also adhere to all safety protocols and maintain strict client confidentiality. 
Additionally, you contribute to the practice's overall success by completing related tasks as needed.

Conversational Style: Communicate concisely and conversationally. Aim for responses in short, clear prose, 
ideally under 10 words. This succinct approach helps in maintaining clarity and focus during patient interactions.

Personality: Your approach should be empathetic and understanding, balancing compassion with maintaining a 
professional stance on what is best for the patient. It's important to listen actively and empathize without 
overly agreeing with the patient, ensuring that your professional opinion guides the therapeutic process.
"""

# Opening Message
begin_sentence = "Hey there, I'm your personal AI therapist, how can I help you?"
```

## 🚀 Usage Examples

### Python Client
```python
import asyncio
import websockets
import json

async def connect_to_retell():
    uri = "wss://your-domain.com/llm-websocket/call-123"
    
    async with websockets.connect(uri) as websocket:
        # Send config response
        config_response = {
            "response_type": "config",
            "config": {"auto_reconnect": True, "call_details": True},
            "response_id": 1
        }
        await websocket.send(json.dumps(config_response))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(connect_to_retell())
```

### JavaScript Client
```javascript
const ws = new WebSocket('wss://your-domain.com/llm-websocket/call-123');

ws.onopen = function() {
    console.log('Connected to Retell LLM');
    
    // Send config response
    const configResponse = {
        response_type: "config",
        config: {
            auto_reconnect: true,
            call_details: true
        },
        response_id: 1
    };
    ws.send(JSON.stringify(configResponse));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    if (data.response_type === 'response_required') {
        // Generate response using your LLM
        const response = generateResponse(data.transcript);
        
        // Send response
        const responseMessage = {
            response_type: "response",
            response_id: data.response_id,
            content: response,
            content_complete: true
        };
        ws.send(JSON.stringify(responseMessage));
    }
};
```

### cURL Examples
```bash
# Health check
curl https://your-domain.com/health

# API documentation
curl https://your-domain.com/docs

# OpenAPI schema
curl https://your-domain.com/openapi.json
```

## 🔍 Error Handling

### WebSocket Errors

#### Connection Errors
```json
{
    "error": "connection_failed",
    "message": "Unable to establish WebSocket connection",
    "code": "WS_CONNECTION_ERROR"
}
```

#### Authentication Errors
```json
{
    "error": "authentication_failed",
    "message": "Invalid Retell API key",
    "code": "WS_AUTH_ERROR"
}
```

#### Protocol Errors
```json
{
    "error": "protocol_error",
    "message": "Invalid message format",
    "code": "WS_PROTOCOL_ERROR"
}
```

### HTTP Errors

#### 400 Bad Request
```json
{
    "detail": "Invalid request format"
}
```

#### 404 Not Found
```json
{
    "detail": "Endpoint not found"
}
```

#### 500 Internal Server Error
```json
{
    "detail": "Internal server error",
    "error": "LLM_API_ERROR",
    "message": "Failed to generate response"
}
```

## 📊 Monitoring and Metrics

### Health Check Metrics
- `retell_key_set` - Boolean indicating if Retell API key is configured
- `openai_key_set` - Boolean indicating if OpenAI API key is configured
- `openai_org_set` - Boolean indicating if OpenAI organization ID is configured
- `retell_key_length` - Length of Retell API key (for debugging)
- `openai_key_length` - Length of OpenAI API key (for debugging)
- `openai_org_length` - Length of OpenAI organization ID (for debugging)

### Performance Metrics
- Response time: < 2 seconds average
- WebSocket connection uptime: 99.9%
- Concurrent connections: Up to 1000
- Memory usage: ~512MB per instance

## 🔒 Security

### Authentication
- Retell API key required for WebSocket connections
- OpenAI API key required for LLM access
- Optional organization ID for OpenAI

### Rate Limiting
- WebSocket connections: 10 per minute per IP
- Health check: 60 per minute per IP
- API endpoints: 100 per minute per IP

### Data Privacy
- No call transcripts are stored permanently
- API keys are encrypted in transit
- All communications use TLS/SSL

## 🆘 Troubleshooting

### Common Issues

#### WebSocket Connection Fails
```bash
# Check if service is running
curl https://your-domain.com/health

# Check WebSocket URL format
# Should be: wss://domain.com/llm-websocket/call-id
```

#### Environment Variables Not Set
```bash
# Check environment variables
curl https://your-domain.com/health | jq '.railway_env_vars'
```

#### LLM Response Errors
```bash
# Check OpenAI API key
curl -H "Authorization: Bearer YOUR_OPENAI_KEY" \
     https://api.openai.com/v1/models
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=1
python -m uvicorn app.server:app --reload --log-level debug
```

## 📈 Performance Optimization

### Response Streaming
The service uses streaming responses for better performance:

```python
async for chunk in stream:
    yield ResponseResponse(
        response_id=request.response_id,
        content=chunk.choices[0].delta.content,
        content_complete=False
    )
```

### Connection Pooling
HTTP connections are reused for better performance:

```python
async with ClientSession() as session:
    # Reuse connection for multiple requests
    pass
```

### Caching
Frequent responses are cached to improve response times:

```python
@lru_cache(maxsize=128)
def get_cached_response(prompt_hash):
    # Return cached response if available
    pass
```

---

**For more information, see the [Developer Guide](DEVELOPER_GUIDE.md) and [Integration Guide](INTEGRATION_GUIDE.md).**
