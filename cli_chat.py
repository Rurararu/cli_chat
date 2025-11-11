import datetime
import json
import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# py cli_chat.py --system "You are You're an assistant who always tells bad jokes." --temperature 0.7 --max_tokens 200

class ChatSession:
    def __init__(self, system_prompt:str="You are helpful assistant.", temperature:float=1.0, max_tokens:int=100):
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.total_tokens_used = 0

    def add_user_message(self, message:str):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message:str):
        self.messages.append({"role": "assistant", "content": message})

    def save_to_json(self):
        filename = datetime.datetime.now().strftime("logs/%Y-%m-%d_%H-%M.json")

        log_data = {
            "messages": self.messages,
            "total_tokens_used": self.total_tokens_used,
            "model": "gpt-4o-mini",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=4)

        print(f"[LOG SAVED] {filename}")

    def generate_response(self):
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        reply = response.choices[0].message.content
        tokens = response.usage.total_tokens
        self.total_tokens_used += tokens
        self.add_assistant_message(reply)
        return reply

    def cli_chat(self):
        print(f"System Prompt: {self.system_prompt}\n")

        while True:
            user_input = input("User > ")
            if user_input.lower() in ("quit", "exit", "q"):
                self.save_to_json()
                break

            self.add_user_message(user_input)
            reply = self.generate_response()
            print(f"Assistant> {reply}\n")


def parse_args():
    parser = argparse.ArgumentParser(description="CLI Chat with OpenAI API")
    parser.add_argument("--system", type=str, default="You are helpful assistant.")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max_tokens", type=int, default=100)
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    args = parse_args()
    session = ChatSession(system_prompt=args.system,
                          temperature=args.temperature,
                          max_tokens=args.max_tokens)
    session.cli_chat()
