from fastapi import FastAPI, HTTPException
from agent.agent import Agent
from phoenix.otel import register
from openinference.instrumentation.dspy import DSPyInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from agent.schema import RequestFormat, ResponseFormat
from agent.caching import LRUCache
from agent.constants import PROJECT_NAME
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Initializing FastAPI application...")

trace_provider = register(
    project_name=PROJECT_NAME,
)

DSPyInstrumentor().instrument(tracer_provider=trace_provider)


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
