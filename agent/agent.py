# Python interface for the TypeScript agent
# Assumes TypeScript is compiled to JS and run via Node.js

import json
import subprocess
from pathlib import Path


def call_agent(task: str, data=None):
    """Call the TypeScript agent via Node.js."""
    agent_script = Path(__file__).parent / "agent.js"  # Assume compiled JS
    if not agent_script.exists():
        return {"error": "Agent script not found"}

    cmd = ["node", str(agent_script), json.dumps({"task": task, "data": data})]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            return {"error": result.stderr.strip()}
    except Exception as e:
        return {"error": str(e)}
