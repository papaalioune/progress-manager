import subprocess
from time import perf_counter

process = subprocess.Popen(["python", "simulators.py"], stdout=subprocess.PIPE)
start = perf_counter()
while process.poll() == None:
    pass
end = perf_counter()    
print(f"Fin des executions en {(end - start) * 1000:.0f} milliseconds!\nGoodbye!")