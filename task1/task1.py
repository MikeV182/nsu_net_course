import csv
import subprocess
import re


hostnames = [
    "google.com",
    "stackoverflow.com",
    "github.com",
    "yahoo.com",
    "yandex.ru",
    "wix.com",
    "wikipedia.org",
    "play2048.co",
    "pointerpointer.com",
    "discord.com",
]

try:
    with open("responses.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "web_adress", "rtt_min (ms)", "rtt_avg (ms)", "rtt_max (ms)"])
        for hostname in hostnames:
            command = f"ping -c 3 {hostname}"
            print(f"Executing now: {command}")

            output = subprocess.check_output(command, shell=True, text=True)
            rtt_substring = re.search("rtt min/avg/max/mdev = ", output)
            output = output[rtt_substring.start() + 23 : -3]
            timings = output.split("/")

            writer.writerow([hostname, timings[0], timings[1], timings[2]])
            print(f"Pinging {hostname}: [DONE]\n")
            
except KeyboardInterrupt:
    print("Keyboard interrupt from a user: [OK]")
