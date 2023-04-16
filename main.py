import threading
import time
import tracemalloc

import fabric
from paramiko.client import WarningPolicy

# docker run -d --name=openssh-server -e PASSWORD_ACCESS=true -e USER_NAME=user -e USER_PASSWORD=password -p 2222:2222 lscr.io/linuxserver/openssh-server:latest
# python3 -m main

# expected output
# correct password - before run - num of threads: 1
# correct password - after run - num of threads: 1

# wrong password - before run - num of threads: 1
# wrong password - after run - num of threads: 6

# wrong password with stop_thread - before run - num of threads: 1
# wrong password with stop_thread - after run - num of threads: 1

tracemalloc.start()

print("openssh-server needs to be running on 2222")


def make_conn(password):
    conn = fabric.Connection(
        host="127.0.0.1", port=2222, user="user", connect_kwargs={"password": password}
    )

    conn.client.set_missing_host_key_policy(WarningPolicy)

    return conn


def correct():
    print(f"correct password - before run - num of threads: {threading.active_count()}")

    conn = make_conn("password")

    for _ in range(0, 5):
        with conn:
            try:
                conn.run("whoami")
            except:
                pass

    time.sleep(5)

    print(f"correct password - after run - num of threads: {threading.active_count()}")


def wrong():
    print(f"wrong password - before run - num of threads: {threading.active_count()}")

    conn = make_conn("wrong_password")

    for _ in range(0, 5):
        with conn:
            try:
                conn.run("whoami")
            except:
                pass

    time.sleep(5)

    print(f"wrong password - after run - num of threads: {threading.active_count()}")


def wrong_stop_thread():
    print(
        f"wrong password with stop_thread - before run - num of threads: {threading.active_count()}"
    )

    conn = make_conn("wrong_password")

    for _ in range(0, 5):
        with conn:
            try:
                conn.run("whoami")
            except:
                pass
            finally:
                print(f"is_connected: {conn.is_connected}")
                conn.client.close()

    time.sleep(5)

    print(
        f"wrong password with stop_thread - after run - num of threads: {threading.active_count()}"
    )


correct()
# wrong()
# wrong_stop_thread()
