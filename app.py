import subprocess
import time

subprocess.Popen(['python3', './API_REST/app.py'])
subprocess.Popen(['python3', './WORKER/app.py'])