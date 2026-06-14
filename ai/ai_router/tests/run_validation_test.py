import time
import concurrent.futures
from unittest.mock import patch
from app.router.engine import RoutingEngine

# Initialize the integrated engine
engine = RoutingEngine()

# 12 Prompts designed to test every branch of the new engine
TEST_PROMPTS = [
    # General / Chat
    ("Hello! can you help me?", "General"),
    ("What is the capital of Italy?", "General"),
    ("Tell me a story about a whale.", "General"),
    
    # Coding (Will trigger Regex if load-shedding activates)
    ("Write a quick python script to parse json.", "Coding"),
    ("How do I implement a binary search in C++?", "Coding"),
    ("Create a clean Java class for a user profile.", "Coding"),
    
    # Reasoning
    ("If a tree falls in a forest and no one is around, does it make a sound?", "Reasoning"),
    ("Solve: A farmer has 17 sheep, all but 9 die. How many are left?", "Reasoning"),
    
    # Vision
    ("Look at this image data and describe the layout.", "Vision"),
    ("Describe this uploaded png photo.", "Vision"),
    
    # More requests to completely saturate the router queue (forcing load-shedding)
    ("Just a casual greeting to keep the line busy.", "General"),
    ("Another quick question about world history.", "General")
]

def simulate_request(prompt_id, prompt_tuple):
    prompt, expected_type = prompt_tuple
    start_time = time.time()
    
    # Track the initial state of the queue right as the thread enters
    with engine.queue_lock:
        router_load_at_entry = engine.active_queues["llama3.2:3b"]
        
    try:
        response = engine.process_query(f"validation_session_{prompt_id}", prompt)
        elapsed = time.time() - start_time
        
        strategy = response.get("strategy", "Unknown")
        target_model = response.get("target_model", "Unknown")
        category = response.get("recommended", "Unknown")
        
        # Color coding console output for clear reading
        if strategy == "Load-Shedding-Regex":
            strat_display = f"\033[93m{strategy}\033[0m" # Yellow
        elif "EMERGENCY" in target_model:
            strat_display = f"\033[91m{target_model}\033[0m" # Red
        else:
            strat_display = f"\033[92m{strategy}\033[0m" # Green

        print(f"[Thread {prompt_id:02d}] Entry Router Queue: {router_load_at_entry} | "
              f"Strategy: {strat_display} -> Model: {target_model} ({category}) in {elapsed:.2f}s")
        
        return response
    except Exception as e:
        print(f"[Thread {prompt_id:02d}] ❌ CRITICAL SCRIPT BREAK: {str(e)}")
        return None

def run_test_suite(concurrency, simulate_worker_crash=False):
    print(f"\n{'='*70}")
    print(f"🚀 RUNNING VALIDATION SUITE (Concurrency: {concurrency} | Simulate Crash: {simulate_worker_crash})")
    print(f"{'='*70}\n")
    
    if simulate_worker_crash:
        # We patch the worker generation call to raise an exception to test Stage 2
        with patch.object(engine.client, 'generate_worker_response', side_block_mock_crash):
            execute_threads(concurrency)
    else:
        execute_threads(concurrency)

def side_block_mock_crash(*args, **kwargs):
    """Simulates an Ollama 500 error or VRAM allocation failure"""
    raise RuntimeError("Ollama HTTP 500: VRAM Allocation Failed (Mocked Crash)")

def execute_threads(concurrency):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(simulate_request, i, prompt_tuple) 
            for i, prompt_tuple in enumerate(TEST_PROMPTS)
        ]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    # TEST 1: Verify Load-Shedding works under heavy load (Concurrency 10)
    # Since ROUTER_QUEUE_LIMIT = 5, threads 6-10 should instantly trigger Regex pathing.
    run_test_suite(concurrency=10, simulate_worker_crash=False)
    
    # Give the hardware a moment to clear queues
    time.sleep(3)
    
    # TEST 2: Verify Stage 2 Pass-Through Fallback works when a worker dies
    run_test_suite(concurrency=2, simulate_worker_crash=True)