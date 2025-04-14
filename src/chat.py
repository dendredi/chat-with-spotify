from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from api_client import Song, search_song_by_lyrics_impl, spotipy_request_impl
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from typing import Callable

examples = [
    HumanMessage(
        f"Can you play the song that goes like [example lyrics]?", name="example_user"
    ),
    AIMessage(
        "",
        name="search_song_by_lyrics",
        tool_calls=[
            {"name": "search_song_by_lyrics", "args": {"lyrics": "[example lyrics]"}, "id": "1"}
        ],
    ),
    ToolMessage(Song(title="[example song]", artist_names="[example artist]"), tool_call_id="1"),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            {
                "name": "spotipy_request", 
                "args": {'function_name': 'search', 'parameters': {'q': f'[example song] [example artist]', 'type': 'track', 'limit': 1}}, 
                "id": "2",
            }
        ],
    ),
    ToolMessage(
        {
            "example_key": "This could be any dictionary with the response to your request.",
            "uri": "[example uri]"
        }, tool_call_id="2"),
    AIMessage(
        "",
        name="spotipy_request",
        tool_calls=[
            {
                "name": "spotipy_request", 
                "args": {
                    "function_name": "start_playback",
                    "parameters": {
                        "uris": ["[example uri]"]
                    }
                },
                "id": "3"
            }
        ] 
    ),
    ToolMessage(None, tool_call_id="3"),
    HumanMessage(
        f"Can you play the song in which MJ was a zombie?", name="example_user"
    ),
    AIMessage(
        "Michael Jackson appeared as a zombie in the iconic music video for 'Thriller'. I will play it for you.",
        name="example_assistant",
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            {
                "name": "spotipy_request", 
                "args": {'function_name': 'search', 'parameters': {'q': f'Thriller Michael Jackson', 'type': 'track', 'limit': 1}}, 
                "id": "4",
            }
        ],
    ),
    ToolMessage(
        {
            "example_key": "This could be any dictionary with the response to your request.",
            "uri": "[example uri]"
        }, tool_call_id="4"),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            {
                "name": "spotipy_request", 
                "args": {
                    "function_name": "start_playback",
                    "parameters": {
                        "uris": ["[example uri]"]
                    }
                },
                "id": "5"
            }
        ],
    ),
    ToolMessage(
        {
            "example_key": "This could be any dictionary with the response to your request.",
            "uri": "[example uri]"
        }, tool_call_id="5"),
]

system = """You are a kind assistant and help controlling spotify. 
Use past tool usage as an example of how to correctly use the tools.
Use 
In case a tool respons with an error, retry only once before briefly telling the user about the problem."""
few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        *examples,
    ]
)


@tool
def search_song_by_lyrics(lyrics: str) -> Song | None:
    """ Finds a song with title and artist names for a part of its lyrics. Use this only when the user actually asks for a song by its lyrics, and you dont know the song yet. """
    try:
        return search_song_by_lyrics_impl(lyrics)
    except ValueError as e:
        return { "error": str(e) }

@tool
def spotipy_request(function_name: str, parameters: dict | None = None) -> dict:
    """
    Executes a Spotipy client method by name with the given parameters.

    This function provides a generic interface to call any public method of the Spotipy client,
    using the method's name as a string and a dictionary of keyword arguments.

    Parameters:
        function_name (str): 
            The name of the Spotipy method to call (e.g., "search", "current_user_playlists").
        parameters (dict): 
            A dictionary of keyword arguments to be passed to the specified Spotipy method.

    Returns:
        dict: 
            The JSON response returned by the Spotipy method, typically containing Spotify API data.
    """
    try:
        return spotipy_request_impl(function_name) if parameters is None else spotipy_request_impl(function_name, **parameters)
    except ValueError as e:
        return { "error": str(e) }


class ChatWithSpotifyCallback:
    def __init__(
        self,
        tool_entered: Callable[[str, dict], None],
        tool_finished: Callable[[str, dict], None],
        chat_response: Callable[[str], None],
    ):
        self.chat_response = chat_response
        self.tool_entered = tool_entered
        self.tool_finished = tool_finished


class ChatWithSpotify:
    def __init__(
        self,
        llm: ChatOpenAI,
        callback: ChatWithSpotifyCallback,
    ):
        self.llm = llm
        self.callback = callback
        
        self.tools = {
            "search_song_by_lyrics": search_song_by_lyrics,
            "spotipy_request": spotipy_request,
        }
        self.llm_with_tools = self.llm.bind_tools(self.tools.values())
        self.messages = few_shot_prompt.format_messages()
        
    def _handle_tool_calls(self, ai_message: AIMessage):
        for tool_call in ai_message.tool_calls:
            selected_tool = self._lookup_tool(tool_call["name"])
            self.callback.tool_entered(tool_call["name"], tool_call["args"])
            tool_message = selected_tool.invoke(tool_call)
            self.callback.tool_finished(tool_call["name"], tool_message.content)
            self.messages.append(tool_message)

    def _lookup_tool(self, tool_name: str):
        try:
            return self.tools[tool_name.lower()]
        except KeyError:
            raise ValueError(f"No tool with name {tool_name} available.")

    def query(self, q: str):
        self.messages.append(HumanMessage(q))
        ai_message = self.llm_with_tools.invoke(self.messages)
        self.messages.append(ai_message)

        if ai_message.content:
            self.callback.chat_response(ai_message.content)
        
        while len(ai_message.tool_calls) > 0:
            self._handle_tool_calls(ai_message)
            
            ai_message = self.llm_with_tools.invoke(self.messages)
            self.messages.append(ai_message)

            if ai_message.content:
                self.callback.chat_response(ai_message.content)
