# Chat with Spotify

A console-based Python app that lets you control Spotify with natural language — using ChatGPT to interpret commands and the Spotify & Genius APIs to find and play music.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dendredi/chat-with-spotify.git
   cd chat-with-spotify
   ```

2. **(Optional) Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Setup

1. **Copy the example environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and fill in your Spotify credentials and any other required settings.

---

## Running the Application

Start the console app with:

```bash
python src/main.py
```

You can chat with the app via the terminal. — to quit the app, type `exit`.

---

## Requirements

- Python 3.8 or newer
- A **Spotify Premium** account and a **Spotify Developer App**, created and configured at [developer.spotify.com](https://developer.spotify.com/)
- Access to an **OpenAI deployment** (e.g., OpenAI API or Azure OpenAI)
- **Genius API credentials**, used to look up songs by partial lyrics. You can register an app and obtain your credentials at: [genius.com/api-clients/new](https://genius.com/api-clients/new)

---

## Example Interaction

Here are some example messages you can type into the console to interact with the app:

- `Play Thriller by Michael Jackson`
- `Play the song where MJ is a zombie`
- `Play the song that goes like 'You 'bout to witness hip-hop in its most purest. Most rawest form, flow almost flawless'`


---

## License

This project is licensed under the MIT License.
