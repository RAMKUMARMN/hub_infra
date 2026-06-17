import sys
import asyncio
from app.router.engine import RoutingEngine

async def run_local_simulator():
    print("====================================================")
    print("\033[1;36mCixio AI Router Engine - Local Terminal Simulator\033[0m")
    print("Type your prompt below to see the LLM routing response.")
    print("Type 'exit' or 'quit' to stop the simulation.")
    print("====================================================\n")

    engine = RoutingEngine()
    messages = []

    while True:
        try:
            # Capture user input
            user_input = input("\033[1;32mUser > \033[0m")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("\nShutting down simulator. Goodbye!")
                break
                
            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            # Process through the core engine
            print("\n\033[33mThinking (Inference running via local Ollama)...\033[0m")
            print("\033[1;34mResponse Stream:\033[0m")
            
            full_response = ""
            async for token in engine.process_stream(messages):
                print(token, end="", flush=True)
                full_response += token
                
            print("\n" + "-" * 50 + "\n")
            
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print("\n\nExiting simulator safely.")
            sys.exit(0)
        except Exception as e:
            print(f"\033[1;31mError processing request:\033[0m {e}\n")

if __name__ == "__main__":
    asyncio.run(run_local_simulator())