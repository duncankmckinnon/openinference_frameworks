# Groq Agent Template and Demo Server

This template provides infrastructure and demo serving with a web interface for interacting with Groq agents. The template uses Groq's high-performance inference API with various open-source models. The point is to make it easy to run and interact with a Groq agent, gain visibility into the internal process through Phoenix, and produce an interactive demo of the system that is quick and easy to run.

## Prerequisites

- Docker, python3, and pyenv installed
- API key credentials (Groq API key)
- Environment variables configured (see Configuration section)

## Quick Start

1. Create your project repo using the template and clone in locally
2. Set your environment variables in the directory in a new `.env` file
3. Create the local `.venv-groq` for the repository by running ```./bin/bootstrap.sh```
   - follow any instructions to install python3 and python3-venv if necessary
   - when the script completes, activate the environment with `source .venv-groq/bin/activate` (on Mac, pc is slightly different)
   - Re-run the script to install any new packages added to requirements
4. Make sure [docker](https://docs.docker.com/get-started/get-docker/) is running on your laptop in the background.
5. Run the demo server from the project root with ```./bin/run_agent.sh --build```

To re-run the containers without building:
```bash
./bin/run_agent.sh
```

## Configuration

The agent is configured to use Groq's high-performance inference API with open-source models. This is controlled through environment variables in your `.env` file. The phoenix collector and fastapi endpoint will be fixed when running locally.

### Environment Variables
```env
GROQ_API_KEY="your-groq-api-key"
GROQ_OPENAI_MODEL="openai/gpt-oss-120b"
GROQ_TEMPERATURE=0.1
FASTAPI_URL="http://fastapi:8000"
PHOENIX_COLLECTOR_ENDPOINT="http://phoenix:6006/v1/traces"
```

#### Environment Variables Explained:
- **GROQ_API_KEY**: Your Groq API key for authentication. Get one from [console.groq.com](https://console.groq.com)
- **GROQ_OPENAI_MODEL**: The model to use for inference. Default is `openai/gpt-oss-120b`. Other options include:
  - `openai/gpt-oss-120b` - Large open-source model with 120B parameters
  - `llama-3.1-70b-versatile` - Meta's Llama 3.1 70B model
  - `llama-3.1-8b-instant` - Faster Llama 3.1 8B model
  - `mixtral-8x7b-32768` - Mixtral model with large context window
- **GROQ_TEMPERATURE**: Controls randomness in responses (0.0-2.0). Lower values = more deterministic. Default: 0.1
- **FASTAPI_URL**: Internal URL for FastAPI server communication
- **PHOENIX_COLLECTOR_ENDPOINT**: Phoenix observability collector endpoint

## Demo Interface

Once running, the demo will be available at:
- Demo Interface: [localhost:8080](http://127.0.0.1:8080)
- Phoenix Dashboard: [localhost:6006](http://127.0.0.1:6006)

The interface allows you to:
- Send messages to the bot
- View the bot's responses
- Review the requests being made and how they are processed step-by-step in Phoenix

## Troubleshooting

### Common Issues

1. **Phoenix Connection Error**
   - Ensure Phoenix container is running
   - Check PHOENIX_COLLECTOR_ENDPOINT in .env

2. **API Key Issues**
   - Verify GROQ_API_KEY is valid and active
   - Check GROQ_OPENAI_MODEL is supported by your account

3. **Container Build Issues**
   - Run with --build flag: `./bin/run_agent.sh --build`
   - Check Docker logs: `docker-compose logs`
        - `docker-compose logs agent` for agent container logs
        - `docker-compose logs phoenix` for phoenix container logs

## Development

### Demo
The demo logic is located in [agent/demo_code/demo_server.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/demo_code). This contains all the logic for interactive chat demos.
Key components:

- `demo_server.py`: Main Flask application (calls the REST API to avoid duplicate logic)
- `templates/index.html`: Web interface for chat
- `static/`: CSS and JavaScript files for running the chat interface

### Server
The server code is in [agent/server.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/server.py). This contains the python fastAPI interface that processes chat requests. 
The server is where the open-inference tracing is setup for the application. 

### Agent
The agent code is in [agent/agent.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/agent.py). It instantiates the Groq client for requests in a setup method, and includes some basic open-telemetry and open-inference boilerplate for capturing information about requests and responses.
The current implementation uses Groq's Python client with the OpenAI-compatible chat completions API. The request is sent to the agent via `client.chat.completions.create()` method.

You probably wont really need to change the tracing or caching logic in the agent, unless there is specific context you need to include beyond the history of the chat.

### Prompts
The prompts and formatting are defined in [agent/prompts.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/prompts.py). This class is meant to contain any prompt logic for LLM calls or individual agents. The benefit of the prompt class is that it provides an interface for passing in requests and context between steps and produces the formatting expected by the agentic framework or LLM client. 

You will need to add your own prompts here for a specific application, and may need to adjust the formatting function to match Groq's expected input format (OpenAI-compatible).

### Schema
The schema is defined in [agent/schema.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/schema.py). It provides validations and defaults for the requests and responses to the agent. The default schema is

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RequestFormat(BaseModel):
    conversation_hash: str = Field(description="The conversation hash associated with the request")
    request_timestamp: Optional[str] = Field(default=datetime.now().isoformat(), description="The timestamp of the request")
    customer_message: str = Field(description="The message of the request")


class ResponseFormat(BaseModel):
    response: str = Field(description="The response to the request")
```

You may need to adjust this to handle other specific information the system needs to produce in the response or any intermediate validations for responses passed between LLMs.

### Caching
The built in caching logic is in [`agent/caching.py`](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/caching.py). It implements a basic LRU cache to store requests and responses during the conversation and surface them on subsequent interactions within the session. 

If you need to include additional context in the cache, the caching may need to be augmented to store other useful information separately (so it only needs to be retrieved and persisted one time - e.g. customer profile info).

## Current Implementation Details

This template is currently configured to use Groq with the following setup:

### Agent Implementation
- Uses `groq.Groq` client class with OpenAI-compatible API
- Calls the LLM via `client.chat.completions.create()` method
- Configured with Groq API key and model selection
- Accesses response through standard OpenAI format: `response.choices[0].message.content`

### Instrumentation
The server includes Groq instrumentation for comprehensive tracing:
```python
from openinference.instrumentation.groq import GroqInstrumentor

GroqInstrumentor().instrument(tracer_provider=tracer_provider)
```

### Dependencies
Key packages in requirements.txt:
- `groq>=0.1.0`
- `openinference-instrumentation-groq>=0.0.1`
- `openinference-instrumentation>=0.0.1`
- `opentelemetry-sdk>=1.19.0`

### Groq Advantages
- **Ultra-fast inference**: Groq's custom silicon delivers lightning-fast responses
- **Open-source models**: Access to latest open models like Llama, Mixtral
- **OpenAI compatibility**: Drop-in replacement for OpenAI API calls
- **Cost-effective**: Competitive pricing for high-performance inference

## Changing to Other Frameworks

If you need to switch to a different agentic framework, you can follow these general steps:
1. Update the python package imports in `agent.py`
2. Modify `setup_client()` to instantiate your preferred framework
3. Update `analyze_request()` to call the client using the framework's conventions
4. Find and install the appropriate OpenInference instrumentor package
5. Update the imports and instrumentation setup in `server.py`
6. Update requirements.txt with the new dependencies
7. Modify environment variables as needed for the new framework

## Groq Specific Features

Groq provides high-performance inference for open-source models:
- **Lightning Speed**: Custom silicon optimized for transformer inference
- **Open Models**: Access to Llama, Mixtral, and other open-source models
- **OpenAI API**: Compatible with existing OpenAI client libraries
- **Reliability**: Enterprise-grade infrastructure with high availability
- **Transparency**: Open-source models with clear licensing and capabilities

For more advanced use cases, you can:
- Switch between different Groq-supported models by changing GROQ_OPENAI_MODEL
- Adjust temperature and other parameters for different use cases
- Leverage Groq's speed for real-time applications requiring fast responses
- Use different models for different tasks (e.g., fast models for simple queries, larger models for complex reasoning)