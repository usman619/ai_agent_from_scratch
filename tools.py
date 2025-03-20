from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

import os

from numpy import save

# def take_note(data: str, filename: str = "research_output.txt"):
#     time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     formatted_note = f"--- Research Note ---\nDate: {time_stamp}\nNote: {data}\n"
    
#     with open(filename , "a", encoding="utf-8") as f:
#         f.write(formatted_note)

#     return f"Note saved to {filename}"

notes_dir = os.path.join("notes")


def take_note(input: str, filename: str = "research_output.txt"):
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_note = f"--- Research Note ---\nDate: {time_stamp}\nNote: {input}\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_note)

    return f"Note saved to {filename}"


note_file = os.path.join('notes', 'research_output.txt')

def save_note(note):
    # Ensure the 'notes' directory exists
    notes_dir = os.path.dirname(note_file)
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir, exist_ok=True)
    
    if isinstance(note, dict):
        topic = note.get("topic", "")
        summary = note.get("summary", "")
        sources = note.get("sources", "")
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_text = f"--- Research Note ---\nDate: {time_stamp}\nTopic: {topic}\nSummary: {summary}\nSources: {sources}"
    else:
        note_text = str(note)
    
    with open(note_file, 'a', encoding="utf-8") as f:
        f.write(note_text + "\n")
    
    return "Note Saved"


# --- Tools ---
# Custom Tool: Take Note
note_tool = Tool(
    name="note",
    func=save_note,
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