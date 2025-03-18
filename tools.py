from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# def take_note(data: str, filename: str = "research_output.txt"):
#     time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     formatted_note = f"--- Research Note ---\nDate: {time_stamp}\nNote: {data}\n"
    
#     with open(filename , "a", encoding="utf-8") as f:
#         f.write(formatted_note)

#     return f"Note saved to {filename}"


def take_note(input: str, filename: str = "research_output.txt"):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_note = f"--- Research Note ---\nDate: {time_stamp}\nNote: {input}\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_note)

    return f"Note saved to {filename}"

# --- Tools ---
# Custom Tool: Take Note
note_tool = Tool(
    name="note",
    func=take_note,
    description="Take a note of the research and save it to a file."
)

# DuckDuckGo Search
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information."   
)

# Wikipedia
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)