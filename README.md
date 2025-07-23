# LangGraph Agent Template and Demo Server

This template provides infrastructure and demo serving with a web interface for interacting with LangGraph agents. The template uses LangGraph with LangChain and OpenAI as the underlying LLM provider. The point is to make it easy to run and interact with a LangGraph agent, gain visibility into the internal process through Phoenix, and produce an interactive demo of the system that is quick and easy to run.

## Prerequisites

- Docker, python3, and pyenv installed
- API key credentials (OpenAI or whichever provider/framework you prefer)
- Environment variables configured (see Configuration section)

## Quick Start

1. Create your project repo using the template and clone in locally
2. Set your environment variables in the directory in a new `.env` file
3. Create the local `.venv` for the repository by running ```./bin/bootstrap.sh```
   - follow any instructions to install python3 and python3-venv if necessary
   - when the script completes, activate the environment with `source .venv/bin/activate` (on Mac, pc is slightly different)
   - Re-run the script to install any new packages added to requirements
4. Make sure [docker](https://docs.docker.com/get-started/get-docker/) is running on your laptop in the background.
5. Run the demo server from the project root with ```./bin/run_agent.sh --build```

To re-run the containers without building:
```bash
./bin/run_agent.sh
```

## Configuration

The agent is configured to use LangGraph with LangChain and OpenAI as the underlying LLM provider. This is controlled through environment variables in your `.env` file. The phoenix collector and fastapi endpoint will be fixed when running locally.

### Environment Variables
```env
OPENAI_API_KEY="your-openai-api-key"
OPENAI_MODEL="gpt-4"
OPENAI_TEMPERATURE=0.2
FASTAPI_URL="http://fastapi:8000"
PHOENIX_COLLECTOR_ENDPOINT="http://phoenix:6006/v1/traces"
```

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
   - Verify OPENAI_API_KEY and check OPENAI_MODEL is valid

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
The agent code is in [agent/agent.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/agent.py). It implements a LangGraph state graph that processes requests through defined nodes and edges. The current implementation uses LangChain's ChatOpenAI client for LLM interactions within the graph structure.

Key components:
- `setup_client()` - Instantiates the LangChain ChatOpenAI client
- `node()` - Defines the processing logic for each graph node
- `graph()` - Creates and compiles the LangGraph StateGraph with START → node → END flow
- `analyze_request()` - Invokes the compiled graph with the request state

The graph structure allows for complex agent workflows with multiple processing steps, conditional routing, and state management between nodes.

### Prompts
The prompts and formatting are defined in [agent/prompts.py](https://github.com/duncankmckinnon/AgentTemplate/tree/main/agent/prompts.py). This class is meant to contain any prompt logic for LLM calls or individual agents. The benefit of the prompt class is that it provides an interface for passing in requests and context between steps and produces the formatting expected by the agentic framework or LLM client. 

You will need to add your own prompts here for a specific application. The current implementation uses LangChain's ChatPromptTemplate for structured prompt formatting with system and human message roles.

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

This template is currently configured to use LangGraph with LangChain and OpenAI with the following setup:

### Agent Implementation
- Uses `langchain_openai.ChatOpenAI` as the LLM client
- Implements a LangGraph `StateGraph` with nodes and edges for workflow management
- State management through a custom `State` schema with request, context, and response fields
- Processes requests through `agent.invoke(state)` which executes the compiled graph

### Graph Structure
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("node", self.node)
graph.add_edge(START, "node")
graph.add_edge("node", END)
```

### Instrumentation
The server includes LangChain instrumentation for comprehensive tracing:
```python
from openinference.instrumentation.langchain import LangChainInstrumentor

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
```

### Dependencies
Key packages in requirements.txt:
- `langchain>=0.3.1`
- `langgraph>=0.3.1`
- `langchain-openai>=0.3.1`
- `openinference-instrumentation-langchain>=0.0.1`

## Changing to Other Frameworks

If you need to switch to a different agentic framework, you can follow these general steps:
1. Update the python package imports in `agent.py`
2. Modify `setup_client()` to instantiate your preferred LLM provider
3. Update the graph structure and node logic as needed for your framework
4. Find and install the appropriate OpenInference instrumentor package
5. Update the imports and instrumentation setup in `server.py`
6. Update requirements.txt with the new dependencies
7. Modify the State schema if needed for your framework's data structures

