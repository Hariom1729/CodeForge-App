import docker
import os
import tempfile
import asyncio
from typing import Dict, Any

# Map language string to Docker image and file extension
RUNTIME_MAP = {
    "python": {"image": "codeforge-python", "ext": ".py", "command": ["python", "/code/main.py"]},
    "javascript": {"image": "codeforge-node", "ext": ".js", "command": ["node", "/code/main.js"]},
    "cpp": {"image": "codeforge-cpp", "ext": ".cpp", "command": ["sh", "-c", "g++ /code/main.cpp -o /tmp/main && /tmp/main"]},
    "go": {"image": "codeforge-go", "ext": ".go", "command": ["go", "run", "/code/main.go"]},
    "rust": {"image": "codeforge-rust", "ext": ".rs", "command": ["sh", "-c", "rustc /code/main.rs -o /tmp/main && /tmp/main"]},
}

class ExecutionManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Warning: Docker not available ({e}). Execution will fail.")
            self.client = None

    async def execute_code(self, language: str, code: str, test_cases: list = None) -> Dict[str, Any]:
        if language not in RUNTIME_MAP:
            return {"status": "error", "output": f"Unsupported language: {language}", "execution_time": 0.0, "test_results": None}
            
        if not self.client:
             return {"status": "error", "output": "Docker daemon is not available on the backend.", "execution_time": 0.0}

        runtime_config = RUNTIME_MAP[language]
        
        # Create a temporary directory to mount into the container
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = f"main{runtime_config['ext']}"
            file_path = os.path.join(temp_dir, file_name)
            
            with open(file_path, "w") as f:
                f.write(code)

            start_time = asyncio.get_event_loop().time()
            
            try:
                # Run the container asynchronously in an executor to not block the FastAPI event loop
                loop = asyncio.get_event_loop()
                container = await loop.run_in_executor(
                    None,
                    lambda: self.client.containers.run(
                        image=runtime_config["image"],
                        command=runtime_config.get("command"),
                        volumes={temp_dir: {'bind': '/code', 'mode': 'ro'}},
                        mem_limit='512m',
                        cpu_quota=50000,
                        network_disabled=True,
                        detach=True,
                        user='runner'
                    )
                )

                # Wait for container to finish or timeout
                try:
                    result = await loop.run_in_executor(None, lambda: container.wait(timeout=10))
                    status_code = result.get('StatusCode', 1)
                except Exception as e: # Catch timeout specifically if requests raises it
                    status_code = 124 # Custom timeout code
                    await loop.run_in_executor(None, lambda: container.kill())

                logs = await loop.run_in_executor(None, lambda: container.logs().decode('utf-8'))
                
                await loop.run_in_executor(None, lambda: container.remove(force=True))
                
                end_time = asyncio.get_event_loop().time()
                execution_time = round(end_time - start_time, 3)

                status = "success" if status_code == 0 else "error"
                if status_code == 124:
                    logs = "Execution Timed Out (10 seconds limit)"

                # --- Auto Grader Logic ---
                test_results = None
                if status == "success" and test_cases:
                    test_results = []
                    for tc in test_cases:
                        expected = str(tc.get("expected_output", "")).strip()
                        actual = logs.strip()
                        passed = expected in actual if expected else True
                        test_results.append({
                            "input": tc.get("input", ""),
                            "expected": expected,
                            "actual": actual,
                            "passed": passed
                        })
                    
                    # If any test case failed, change status to 'failed_tests'
                    if any(not tr["passed"] for tr in test_results):
                        status = "failed_tests"

                return {
                    "status": status,
                    "output": logs,
                    "execution_time": execution_time,
                    "test_results": test_results
                }

            except Exception as e:
                end_time = asyncio.get_event_loop().time()
                return {
                    "status": "error",
                    "output": str(e),
                    "execution_time": round(end_time - start_time, 3),
                    "test_results": None
                }

execution_manager = ExecutionManager()
