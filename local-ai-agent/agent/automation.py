import io
import time
import pyautogui
from PIL import Image

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

class AutomationEngine:
    def move_mouse(self, x: int, y: int, duration: float = 0.2) -> dict:
        pyautogui.moveTo(x, y, duration=duration)
        return {"status": "moved", "x": x, "y": y, "duration": duration}

    def click(self, x: int | None = None, y: int | None = None, button: str = "left") -> dict:
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button)
        else:
            pyautogui.click(button=button)
        return {"status": "clicked", "button": button, "x": x, "y": y}

    def double_click(self, x: int | None = None, y: int | None = None, button: str = "left") -> dict:
        if x is not None and y is not None:
            pyautogui.doubleClick(x=x, y=y, button=button)
        else:
            pyautogui.doubleClick(button=button)
        return {"status": "double_clicked", "button": button, "x": x, "y": y}

    def type_text(self, text: str, interval: float = 0.05) -> dict:
        pyautogui.write(text, interval=interval)
        return {"status": "typed", "text": text, "interval": interval}

    def press_key(self, key: str) -> dict:
        pyautogui.press(key)
        return {"status": "pressed", "key": key}

    def hotkey(self, *keys: str) -> dict:
        pyautogui.hotkey(*keys)
        return {"status": "hotkey", "keys": keys}

    def wait(self, seconds: float) -> dict:
        time.sleep(seconds)
        return {"status": "waited", "seconds": seconds}

    def capture_screenshot(self, max_width: int = 1024, quality: int = 70) -> bytes:
        """Captures the screen, resizes for optimal latency, and returns JPEG bytes."""
        screenshot = pyautogui.screenshot()
        if screenshot.width > max_width:
            ratio = max_width / float(screenshot.width)
            new_height = int(float(screenshot.height) * ratio)
            screenshot = screenshot.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG", quality=quality)
        return buffer.getvalue()

    def get_screen_size(self) -> dict:
        """Returns primary display resolution for coordinate mapping."""
        width, height = pyautogui.size()
        return {"width": width, "height": height}