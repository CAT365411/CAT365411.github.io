import base64
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .automation import AutomationEngine
from .task import TaskManager
from .auth import authenticate_request, get_current_user, login_user, logout_user
from .sandbox import SandboxManager

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Local AI Agent")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

automation = AutomationEngine()
task_manager = TaskManager()
auth_sandbox = SandboxManager()

class PromptRequest(BaseModel):
    prompt: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/automation/screenshot", dependencies=[Depends(authenticate_request)])
async def get_screenshot():
    if auth_sandbox.is_enabled():
        raise HTTPException(status_code=403, detail="Screen capture disabled in sandbox mode.")
    image_bytes = automation.capture_screenshot()
    return Response(content=image_bytes, media_type="image/jpeg")

@app.websocket("/ws/screen")
async def stream_screen_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if not auth_sandbox.is_enabled():
                frame_bytes = automation.capture_screenshot()
                b64_frame = base64.b64encode(frame_bytes).decode('utf-8')
                await websocket.send_json({"type": "frame", "data": b64_frame})
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass

@app.get("/sandbox/status", dependencies=[Depends(authenticate_request)])
async def sandbox_status():
    return auth_sandbox.status()

@app.post("/task/execute", dependencies=[Depends(authenticate_request)])
async def execute_prompt(request: PromptRequest):
    if auth_sandbox.is_enabled():
        return {"status": "sandbox", "detail": "Prompt execution is disabled in sandbox mode."}
    return task_manager.execute_prompt(request.prompt)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
        <rect width="32" height="32" fill="#0f172a" rx="6"/>
        <text x="50%" y="55%" font-size="18" dominant-baseline="middle" text-anchor="middle">🤖</text>
    </svg>"""
    return Response(content=svg_icon, media_type="image/svg+xml")

@app.get("/")
async def root(request: Request):
    try:
        get_current_user(request)
        return RedirectResponse("/dashboard")
    except HTTPException:
        return RedirectResponse("/login")

@app.get("/login")
async def login_page(request: Request):
    try:
        get_current_user(request)
        return RedirectResponse("/dashboard")
    except HTTPException:
        return FileResponse(STATIC_DIR / "login.html")

@app.post("/login")
async def login(request: LoginRequest, response: Response):
    return await login_user(request.username, request.password, response)

@app.post("/logout")
async def logout(request: Request, response: Response):
    return await logout_user(request, response)

@app.get("/dashboard")
async def dashboard(request: Request):
    try:
        get_current_user(request)
        return FileResponse(STATIC_DIR / "dashboard.html")
    except HTTPException:
        return RedirectResponse("/login")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent.main:app", host="0.0.0.0", port=8000, reload=True)