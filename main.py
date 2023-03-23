import threading
import tracemalloc

from paramiko.client import SSHClient, WarningPolicy

# docker run -d --name=openssh-server -e PASSWORD_ACCESS=true -e USER_NAME=user -e USER_PASSWORD=password -p 2222:2222 lscr.io/linuxserver/openssh-server:latest
# python3 -Wall -m main

# expected output
# correct password - before run - num of threads: 1
# correct password - after run - num of threads: 1
# wrong password - before run - num of threads: 1
# wrong password - after run - num of threads: 6
# wrong password with stop_thread - before run - num of threads: 6
# wrong password with stop_thread - after run - num of threads: 7

tracemalloc.start()

print("openssh-server needs to be running on 2222")

client = SSHClient()
client.set_missing_host_key_policy(WarningPolicy)


def run(client, password):
    client.connect("127.0.0.1", port=2222, username="user", password=password)

    stdin, stdout, stderr = client.exec_command("whoami")
    output = stdout.readlines()
    # print(output)


print(f"correct password - before run - num of threads: {threading.active_count()}")

for _ in range(0, 5):
    try:
        run(client, "password")
        client.close()
    except:
        pass

print(f"correct password - after run - num of threads: {threading.active_count()}")

print(f"wrong password - before run - num of threads: {threading.active_count()}")

for _ in range(0, 5):
    try:
        run(client, "wrong_password")
        client.close()
    except:
        pass

print(f"wrong password - after run - num of threads: {threading.active_count()}")

print(
    f"wrong password with stop_thread - before run - num of threads: {threading.active_count()}"
)

for _ in range(0, 5):
    try:
        run(client, "wrong_password")
        client.close()
    except:
        pass
    finally:
        client.get_transport().stop_thread()

print(
    f"wrong password with stop_thread - after run - num of threads: {threading.active_count()}"
)
