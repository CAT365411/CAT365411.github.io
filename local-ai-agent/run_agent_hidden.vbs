Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.Run "cmd.exe /c cd /d C:\Users\Utilisateur\AI_Projects\local_ai_agent && uvicorn agent.main:app --host 0.0.0.0 --port 8000 --reload > C:\Users\Utilisateur\AI_Projects\local_ai_agent\agent_error.log 2>&1", 0, False
