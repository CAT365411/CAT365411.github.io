import os
import re
from typing import Any
import ollama
from .vm import VMManager
from .review import ReviewManager
from .security import SecurityMonitor
from .automation import AutomationEngine


class TaskManager:

  def __init__(self):
    self.vm_manager = VMManager()
    self.kali_iso_path = os.getenv("KALI_ISO_PATH")
    self.review = ReviewManager()
    self.security = SecurityMonitor()
    self.automation = AutomationEngine()
    self.allow_autonomous = True  # Fully autonomous by default for local tasks
    self.allow_dangerous = True

  def execute_prompt(self, prompt: str) -> dict[str, Any]:
    normalized = prompt.strip().lower()
    if not normalized:
      return {"status": "error", "message": "No prompt provided."}

    # Intelligent intent handling for automation features
    if "sandbox" in normalized:
      enable = "enable" in normalized or "turn on" in normalized
      os.environ["ALLOW_DANGEROUS"] = "false" if enable else "true"
      return {
          "status": "executed",
          "action": "sandbox_toggle",
          "enabled": enable,
      }

    # Use Qwen via Ollama to execute any arbitrary desktop automation task autonomously
    try:
      system_prompt = (
          "You are an autonomous desktop automation agent. Convert the user"
          " prompt into executable Python code using the `self.automation`"
          " object (methods: move_mouse(x, y), click(x, y), type_text(text),"
          " press_key(key), hotkey(*keys), wait(seconds), capture_screenshot())."
          " Only return the executable code block inside ```python and ``` tags."
      )

      response = ollama.chat(
          model="qwen2.5-coder:7b",
          messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": prompt},
          ],
      )

      content = response["message"]["content"]
      if "```python" in content:
        code_block = content.split("```python")[1].split("```")[0].strip()
        local_scope = {"self": self, "automation": self.automation}
        exec(code_block, globals(), local_scope)

        return {
            "status": "executed",
            "prompt": prompt,
            "generated_code": code_block,
        }
      else:
        return {
            "status": "error",
            "message": "Could not parse python code from local LLM response.",
        }

    except Exception as e:
      return {"status": "error", "message": str(e)}