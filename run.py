import subprocess
import threading

def run_fastapi():
    subprocess.run(["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8080"])

# Run both concurrently
t1 = threading.Thread(target=run_fastapi)
t2 = threading.Thread(target=run_streamlit)

t1.start()
t2.start()
t1.join()
t2.join()