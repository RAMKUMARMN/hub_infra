import time
import concurrent.futures
from app.router.engine import RoutingEngine

# Initialize a single engine instance
engine = RoutingEngine()

# 15 Prompts: A gauntlet of General, Coding, Reasoning, and Ambiguous queries
TEST_PROMPTS = [
    # --- Fast Path (General/Chat) ---
    "Hello there! How are you doing?",
    "What is the capital of Japan?",
    "Tell me a short joke about computers.",
    "Who wrote the book 1984?",
    "Good morning!",
    
    # --- Escalation Path (Heavy Coding/Reasoning) ---
    "Write a Java class that implements a thread-safe Singleton pattern.",
    "Explain the time complexity of a HashMap in Java under worst-case collision scenarios.",
    "Create a C++ function to invert a binary tree.",
    "Write a Node.js express route that handles file uploads.",
    "Solve this riddle: I speak without a mouth and hear without ears. What am I?",
    "Explain the difference between TCP and UDP sockets.",
    
    # --- Ambiguous/Edge Cases (Testing the Router's confidence) ---
    "Fix this.", 
    "How do I do it?",
    "Make it faster.",
    "What is the best way?"
]

def simulate_request(prompt_id, prompt):
    print(f"[Thread {prompt_id:02d}] 📤 Sending: '{prompt[:40]}...'")
    start_time = time.time()
    
    try:
        response = engine.process_query(f"stress_session_{prompt_id}", prompt)
        
        elapsed = time.time() - start_time
        target = response.get("target_model", "Unknown")
        category = response.get("recommended", "Unknown")
        output_text = response.get("response", "NO_RESPONSE_FOUND").replace('\n', ' ')
        
        print(f"[Thread {prompt_id:02d}] ✅ {target} ({category}) in {elapsed:.2f}s | Output: {output_text[:50]}...")
        
        return {"target": target, "time": elapsed}
    except Exception as e:
        print(f"[Thread {prompt_id:02d}] ❌ FAILED: {str(e)}")
        return None

def run_stress_test(concurrency_level):
    print(f"🚀 Starting HEAVY Stress Test with {concurrency_level} parallel workers...\n")
    start_time = time.time()
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        futures = [
            executor.submit(simulate_request, i, prompt) 
            for i, prompt in enumerate(TEST_PROMPTS)
        ]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    total_time = time.time() - start_time
    
    # --- Calculate Analytics ---
    router_times = [r["time"] for r in results if r["target"] == "llama3.2:3b"]
    worker_times = [r["time"] for r in results if r["target"] != "llama3.2:3b" and r["target"] != "Unknown"]
    
    avg_router = sum(router_times) / len(router_times) if router_times else 0
    avg_worker = sum(worker_times) / len(worker_times) if worker_times else 0
    
    print("\n" + "="*50)
    print(f"🏁 TEST COMPLETE: {len(results)}/{len(TEST_PROMPTS)} Successful")
    print(f"⏱️ Total Wall Clock Time: {total_time:.2f}s")
    print(f"⚡ Fast Path (Llama 3.2 3B) Average: {avg_router:.2f}s (Count: {len(router_times)})")
    print(f"🐢 Worker Path (Qwen 7B) Average: {avg_worker:.2f}s (Count: {len(worker_times)})")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Pushing 10 simultaneous threads to really test the VRAM queueing
    run_stress_test(concurrency_level=10)