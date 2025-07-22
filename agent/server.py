from fastapi import FastAPI, HTTPException
from agent.agent import Agent
from phoenix.otel import register
from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
from openinference.instrumentation.pydantic_ai.utils import is_openinference_span
from openinference.instrumentation.openai import OpenAIInstrumentor
from agent.schema import RequestFormat, ResponseFormat
from agent.caching import LRUCache
from agent.constants import PROJECT_NAME
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Initializing FastAPI application...")

# Get Phoenix endpoint from environment
phoenix_endpoint = os.getenv(
    "PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces"
)
logger.info(f"Configuring Phoenix tracing with endpoint: {phoenix_endpoint}")

tracer_provider = register(
    project_name=PROJECT_NAME,
    endpoint=phoenix_endpoint,
)

# Add the OpenInference processor to enhance spans
openinference_processor = OpenInferenceSpanProcessor(span_filter=is_openinference_span)
tracer_provider.add_span_processor(openinference_processor)

OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

app = FastAPI()
cache = LRUCache()
agent = Agent(cache=cache)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/clear_cache")
def clear_cache():
    cache.clear()
    return {"message": "Cache cleared"}


@app.post("/agent", response_model=ResponseFormat)
def process_request(request: RequestFormat):
    try:
        response = agent.handle_request(request)

        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
