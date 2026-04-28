import os
import traceback
from farmer_agent import FarmerAgent, AgentError


def main():
    print("AgriGPT Farmer Agent\n--------------------")

    try:
        print("Step 1: Initializing agent...")
        agent = FarmerAgent()
        if agent.use_api:
            print("Step 2: OpenAI API key found. Using API mode.")
        else:
            print("Step 2: No OpenAI API key found. Using local fallback mode.")

        print("Step 3: Ready for farmer questions.")

        while True:
            try:
                question = input("\nAsk AgriGPT for farming advice or type quit: ").strip()
            except EOFError:
                print("\nInput stream closed. Exiting AgriGPT.")
                break

            if question.lower() in {"quit", "exit"}:
                print("Exiting AgriGPT. Stay safe on the farm!")
                break

            print("Step 4: Sending question to agent...")
            try:
                answer = agent.ask(question)
                print("Step 5: Agent response received.")
                print("\n--- AgriGPT Response ---")
                print(answer)
            except AgentError as error:
                print(f"Error: {error}")
            except Exception as error:
                print("Unexpected error occurred while querying the agent.")
                traceback.print_exc()

    except Exception as error:
        print("Fatal error during agent startup:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
