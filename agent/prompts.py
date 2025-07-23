from langchain_core.prompts import ChatPromptTemplate


class Prompts:
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that can answer questions and help with tasks."),
        ("human", "Customer message: {request}\n\nContext: {context}")
    ])
