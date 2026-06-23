import httpx

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJwYXR1cmlraXJhbnRlamEuMjMuY3NlQGFuaXRzLmVkdS5pbiIsImV4cCI6MTc4MjE5NTU2MCwiaWF0IjoxNzgyMTk0NjYwLCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiMDFjMDdiYTQtMGY0Ni00ZDViLWE0MjctZjkyZDU4M2E3Y2I4IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoicGF0dXJpIGtpcmFuIHRlamEiLCJzdWIiOiI2MWE2MzBmYi0xYWEzLTQyNzEtOWI1Mi1kNjBjMGNlOGFkNmIifSwiZW1haWwiOiJwYXR1cmlraXJhbnRlamEuMjMuY3NlQGFuaXRzLmVkdS5pbiIsIm5hbWUiOiJwYXR1cmkga2lyYW4gdGVqYSIsInJvbGxObyI6ImEyMzEyNjUxMDEwNSIsImFjY2Vzc0NvZGUiOiJNVHF4YXIiLCJjbGllbnRJRCI6IjYxYTYzMGZiLTFhYTMtNDI3MS05YjUyLWQ2MGMwY2U4YWQ2YiIsImNsaWVudFNlY3JldCI6InRVcWJwZUtzcGFrd3V3ZFYifQ.Qsn_hvKVcZPkD1dw-RWUQsZg12393vRQjcR8jcZ_mz4"

def log(stack, level, package, message):
    body = { "stack" : stack, "level" : level, "package" : package , "message" : message}
    header = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.post("http://4.224.186.213/evaluation-service/logs", json = body, headers = header)
        print("Status:", response.status_code)
        print("Response:", response.json())
        return response.json()
    except Exception as e:
        print("Error:", e)

