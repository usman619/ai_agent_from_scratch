from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from models import ResearchResponse
from constants import gemini_api_key
from tools import search_tool, wikipedia_tool, note_tool

# Gemini LLM
llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=gemini_api_key,
        )
# Local Deepseek LLM
# local_llm = OllamaLLM(
#         model="deepseek-r1:1.5b", 
#         base_url="http://localhost:11434",
#         )

# Output Parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Your are an AI research assistant. You are asked to provide a summary of a topic,
            including the sources (links) and tools used to gather the information.
            Warp the output in the following format and provide no other text \n{format_instructions}
            """
        ),
        ("placeholder", "{chat_history}",),
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        # ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


# Available Tools
tools = [search_tool, wikipedia_tool, note_tool]

# Chat Agent
agent = create_tool_calling_agent(
    llm=llm, 
    prompt=prompt, 
    tools=tools
)

query = input("What can I help you with today?\n ❯ ")

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
raw_response = agent_executor.invoke({"query": query})

# print(raw_output.get("output"))

# Parse the output
try:
    parsed_output = parser.parse(raw_response.get("output"))
    print(parsed_output)
except Exception as e:
    print("Error: ", e ,"\nRaw Response:", raw_response)
    