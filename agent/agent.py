from typing import Dict
from openinference.instrumentation import using_session
from agent.schema import RequestFormat, ResponseFormat
from agent.prompts import Prompts
from agent.caching import LRUCache
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger("agent_demo")

load_dotenv()


def setup_client():
    # For the template, we're using OpenAI, but you can use any LLM provider or agentic framework
    import dspy

    logger.info(
        f"Setting up OpenAI with endpoint: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}"
    )
    model = dspy.LM(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    dspy.configure(lm=model)
    qa = dspy.ChainOfThought("question, context -> response")
    return qa


class Agent:

    def __init__(self, cache: LRUCache):
        self.client = setup_client()
        self.prompts = Prompts()
        self.cache = cache

    def analyze_request(self, message: RequestFormat) -> Dict:
        """Analyze the request and determine the appropriate response"""
        conversation_hash = message.conversation_hash
        request = message.customer_message
        if self.cache.get(conversation_hash):
            context, session_id = self.cache.get(conversation_hash)
        else:
            context = "start"
            session_id = self.cache.set(conversation_hash)
        prompt = self.prompts.format_prompt(request, str(context))

        try:
            with using_session(session_id):
                response = self.client(**prompt)
            response = response.response
            self.cache.add_interaction(conversation_hash, request, response)
            return {"response": response}
        except Exception as e:
            error_response = {
                "response": "I apologize, but I'm having trouble processing your request. Please try again."
            }
            print(f"Error calling OpenAI API: {str(e)}")
            return error_response

    def handle_request(self, message: RequestFormat) -> ResponseFormat:
        """Process a request and generate a response"""

        # Analyze the request
        analysis = self.analyze_request(message)
        return ResponseFormat(**analysis)
