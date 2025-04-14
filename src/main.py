from langchain_openai import AzureChatOpenAI
from chat import ChatWithSpotify, ChatWithSpotifyCallback
from config import GPT_URL, GPT_API_VERSION, GPT_ACCESS_TOKEN


def main():
    chat = ChatWithSpotify(
        llm = AzureChatOpenAI(
            azure_endpoint=GPT_URL,
            api_version=GPT_API_VERSION,
            api_key=GPT_ACCESS_TOKEN,
            #temperature=0,
        ),
        callback=ChatWithSpotifyCallback(
            chat_response=lambda message : print(f"Assistent: {message}"),
            tool_entered=lambda name, params : print(f"Tool '{name}' called with params {params} ..."),
            tool_finished=lambda name, response : None,
        )
    )

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        try:
            chat.query(user_input)
        except Exception as e:
            print(f"An error has occured: {str(e)}")

        
if __name__ == "__main__":
    main()