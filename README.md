# Agentic Framework Comparison Repository

This repository provides a comprehensive comparison of different agentic AI orchestration frameworks through working implementations. Each branch contains the same core application built with a different framework, allowing you to explore and compare approaches to building AI agents.

## 📋 Table of Contents - Framework Implementations

| Framework&nbsp;   | Branch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description | Key Features |
|-------------|--------------|-------------|--------------|
| **OpenAI&nbsp;Direct** | [📁&nbsp;`openai`](https://github.com/duncankmckinnon/openinference_frameworks/tree/openai) | Direct OpenAI API integration | Simple, minimal setup with raw OpenAI calls |
| **CrewAI** | [📁&nbsp;`crewai`](https://github.com/duncankmckinnon/openinference_frameworks/tree/crewai) | Multi-agent collaboration framework | Agent crews, role-based workflows, task delegation |
| **LangGraph** | [📁&nbsp;`langgraph`](https://github.com/duncankmckinnon/openinference_frameworks/tree/langgraph) | Graph-based agent workflows | State management, conditional routing, complex workflows |
| **Pydantic&nbsp;AI** | [📁&nbsp;`pydantic`](https://github.com/duncankmckinnon/openinference_frameworks/tree/pydantic) | Type-safe AI agent framework | Built-in validation, structured outputs, type safety |
| **LiteLLM** | [📁&nbsp;`litellm`](https://github.com/duncankmckinnon/openinference_frameworks/tree/litellm) | Multi-provider LLM gateway | Unified API for 100+ LLM providers, easy provider switching |
| **DSPy** | [📁&nbsp;`dspy`](https://github.com/duncankmckinnon/openinference_frameworks/tree/dspy) | Declarative language model programming | Signatures, modules, prompt optimization, composability |

## 🚀 What This Repository Demonstrates

Each implementation provides the same core functionality:
- **Interactive chat interface** with a web-based demo
- **Phoenix observability** for tracing and monitoring agent behavior
- **Docker containerization** for consistent deployment
- **REST API** for programmatic agent interaction
- **Conversation memory** and context management

## 🏗️ Common Infrastructure

All implementations share the same foundational components:

### Core Features
- **FastAPI server** for HTTP endpoints
- **Flask demo interface** for interactive testing
- **Phoenix integration** for comprehensive observability and tracing
- **Docker containerization** with Python 3.12 and uv package management
- **LRU caching** for conversation state management
- **Pydantic schemas** for request/response validation

### Observability & Monitoring
- **Phoenix dashboard** at `localhost:6006` for trace visualization
- **OpenInference instrumentation** specific to each framework
- **Request/response tracing** with conversation context
- **Performance metrics** and error tracking

### Development Tools
- **Automatic environment setup** with `./bin/bootstrap.sh`
- **Hot reload** for development iterations
- **Comprehensive logging** for debugging
- **Standardized project structure** across all implementations

## 🔧 Quick Start (Any Branch)

1. **Choose your framework** - Switch to the branch you want to explore
2. **Set up environment** - Run `./bin/bootstrap.sh` (installs Python 3.12 + uv automatically)
3. **Configure API keys** - Create `.env` file with your OpenAI API key
4. **Launch the stack** - Run `./bin/run_agent.sh --build`
5. **Explore the demo** - Visit `localhost:8080` for the chat interface
6. **Monitor with Phoenix** - Visit `localhost:6006` for observability

## 📊 Framework Comparison

### Complexity vs. Capability

| Framework | Setup Complexity | Learning Curve | Capability | Best For |
|-----------|------------------|----------------|------------|----------|
| **OpenAI Direct** | Low | Low | Basic | Simple chatbots, prototyping |
| **CrewAI** | Medium | Medium | High | Multi-agent workflows, team collaboration |
| **LangGraph** | High | High | Very High | Complex state machines, conditional logic |
| **Pydantic AI** | Low | Low | Medium | Type-safe applications, structured data |
| **LiteLLM** | Low | Low | Medium | Multi-provider applications, vendor flexibility |
| **DSPy** | Medium | Medium | High | Declarative prompting, optimization, research |

### Key Differences

**OpenAI Direct**
- Minimal abstraction over OpenAI API
- Direct control over all parameters
- Simplest to understand and debug

**CrewAI**
- Multi-agent orchestration
- Role-based agent definitions
- Built-in task delegation and collaboration

**LangGraph**
- Graph-based workflow definition
- Advanced state management
- Conditional routing and complex logic flows

**Pydantic AI**
- Type-safe agent interactions
- Built-in validation and structured outputs
- Clean, pythonic API design

**LiteLLM**
- Unified API for 100+ LLM providers
- Easy provider switching without code changes
- Built-in cost tracking and fallback mechanisms

**DSPy**
- Declarative approach to LM programming
- Automatic prompt optimization
- Modular components (ChainOfThought, ReAct, etc.)
- Research-focused with composability

## 🛠️ Switching Between Implementations

Each branch is fully self-contained. To explore a different framework:

```bash
# Switch to desired framework branch
git checkout <framework-branch>

# Set up and activate the environment (if you want to make changes)
./bin/bootstrap.sh && source .venv-{framework}/bin/activate.sh

# Launch the application
./bin/run_agent.sh --build
```

## 📁 Project Structure

All implementations follow this consistent structure:

```
├── agent/
│   ├── agent.py          # Core agent implementation (framework-specific)
│   ├── server.py         # FastAPI server with observability
│   ├── prompts.py        # Prompt templates and formatting
│   ├── schema.py         # Pydantic models for validation
│   ├── caching.py        # Conversation state management
│   └── demo_code/        # Flask demo interface
├── bin/
│   ├── bootstrap.sh      # Environment setup script
│   └── run_agent.sh      # Docker launch script
├── Dockerfile            # Python 3.12 + uv container
├── docker-compose.yml    # Multi-service orchestration
├── requirements.txt      # Framework-specific dependencies
└── README.md            # Framework-specific documentation
```

## 🔍 Observability Features

All implementations include comprehensive observability through Phoenix:

- **Trace Visualization** - See complete request flows
- **Performance Monitoring** - Track response times and errors
- **Conversation Context** - View full conversation history
- **Framework-Specific Metrics** - Understand framework internals
- **Real-time Dashboards** - Monitor live agent interactions

## 🎯 Learning Path Recommendations

1. **Start with OpenAI Direct** - Understand the basics without framework abstractions
2. **Explore Pydantic AI** - Learn type-safe agent development
3. **Try LiteLLM** - Experience multi-provider flexibility and cost optimization
4. **Experiment with DSPy** - Try declarative prompting and optimization
5. **Experience CrewAI** - Build multi-agent orchestration systems
6. **Master LangGraph** - Create complex, stateful agent workflows

## 🤝 Contributing

Each branch maintains the same application interface while showcasing different framework approaches. When contributing:

- Keep the core API consistent across implementations
- Update framework-specific documentation in each branch
- Ensure observability features work across all frameworks
- Maintain the same development experience (bootstrap, run scripts, etc.)

## 📖 Further Reading

- **Phoenix Observability**: [Phoenix Documentation](https://docs.arize.com/phoenix)
- **OpenInference Standards**: [OpenInference Specification](https://github.com/Arize-ai/openinference)
- **Framework Documentation**: See individual branch READMEs for framework-specific guides

---

Choose a branch above to start exploring different approaches to building AI agents! Each implementation provides the same functionality with different architectural patterns and capabilities.