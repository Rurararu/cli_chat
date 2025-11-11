# CLI Chat with OpenAI

A Command-Line Interface (CLI) application for interacting with the OpenAI API (specifically the `gpt-4o-mini` model), allowing customization of session parameters and automatic saving of conversation logs.

## Project Structure

The project has the following file structure:

```
cli_chat/
├── logs/             # Directory to store chat session JSON logs
├── venv/             # Python virtual environment (recommended)
├── .env              # File for storing environment variables (API Key)
├── .gitignore        # Specifies files and folders to ignore in Git
├── cli_chat.py       # Main Python script for the CLI application
└── requirements.txt  # List of required Python packages
```

-----

## Getting Started

### Prerequisites

  * Python 3.x
  * An **OpenAI API Key**

### Installation and Setup

1.  **Clone the Repository** and navigate to the main directory (`Lab2`).

2.  **Set up the Virtual Environment** (recommended):

    ```bash
    python -m venv venv
    # Activate the environment (Linux/macOS)
    source venv/bin/activate
    # Activate the environment (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key**:

    Open the **`.env`** file and add your OpenAI API key:

    ```
    OPENAI_API_KEY="YOUR_API_KEY_HERE"
    ```

-----

## Usage

### Running the Application

Start the chat session by running the main script:

```bash
python cli_chat.py
```

### Command-Line Arguments

You can customize the chat session's behavior using optional arguments:

| Argument | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `--system` | `str` | `"You are helpful assistant."` | Defines the initial instructions/role for the AI assistant. |
| `--temperature` | `float` | `1.0` | Controls the randomness of the output (0.0 to 2.0). |
| `--max_tokens` | `int` | `100` | The maximum length of the assistant's response. |

**Example of use:**

```bash
python cli_chat.py --system "You're an assistant who always tells bad jokes." --temperature 0.7 --max_tokens 200
```

### Exiting the Chat

To end the chat session, type one of the following commands and press Enter:

  * `quit`
  * `exit`
  * `q`

-----

## How It Works

The core of the application is the **`ChatSession`** class, which manages the conversation state.

1.  **Initialization**: Upon launch, the script loads the `OPENAI_API_KEY` from `.env` and initializes a `ChatSession` object with parameters parsed from command-line arguments (`--system`, `--temperature`, `--max_tokens`). The system prompt is set as the first message.
2.  **Interaction Loop**: The **`cli_chat()`** method runs a loop, taking user input, adding it to the message history, and calling **`generate_response()`**.
3.  **API Call**: The **`generate_response()`** method calls the `client.chat.completions.create` endpoint using the `gpt-4o-mini` model with the current message history and configured parameters.
4.  **Token Tracking**: The total tokens used are tracked and updated after each response.
5.  **Logging**: When the user exits the session (`quit`, `exit`, `q`), the **`save_to_json()`** method is called. It saves the entire conversation history (`messages`), total tokens used, and configuration settings into a timestamped JSON file within the **`logs/`** directory.