import subprocess
import time

subprocess.Popen(['python', './API_REST/app.py'])
subprocess.Popen(['python', './WORKER/app.py'])