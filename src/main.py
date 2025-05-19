from langchain_openai import AzureChatOpenAI, ChatOpenAI
from chat import ChatWithSpotify, ChatWithSpotifyCallback
from config import GPT_URL, GPT_API_VERSION, GPT_ACCESS_TOKEN, GPT_IS_AZURE


def get_llm(model: str = "gpt-4o", temperature: float = 0.7):
    if GPT_IS_AZURE:
        return AzureChatOpenAI(
            azure_endpoint=GPT_URL,
            api_key=GPT_ACCESS_TOKEN,
            api_version=GPT_API_VERSION,
            model=model,
            temperature=temperature,
        ) 
    else:
        return ChatOpenAI(
            base_url=GPT_URL,
            api_key=GPT_ACCESS_TOKEN,
            model=model,
            temperature=temperature,
        )

def main():
    chat = ChatWithSpotify(
        llm=get_llm(),
        callback=ChatWithSpotifyCallback(
            chat_response=lambda message: print(f"Assistent: {message}"),
            tool_entered=lambda name, params: print(
                f"Tool '{name}' called with params {params} ..."
            ),
            tool_finished=lambda name, response: None,
        ),
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
