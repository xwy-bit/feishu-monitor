import subprocess
import threading
import requests
import time

def push_report(web_hook, content):
    """飞书推送"""
    header = {"Content-Type": "application/json;charset=UTF-8"}
    message_body = {"msg_type": "text", "content": {"text": content}}
    try:
        resp = requests.post(url=web_hook, json=message_body, headers=header)
        opener = resp.json()
        if opener.get("StatusMessage") == "success":
            print("[INFO] 飞书消息发送成功:", content)
        else:
            print("[WARN] 飞书消息发送失败:", opener)
    except Exception as e:
        print("[ERROR] 发送飞书消息失败:", e)

def run_and_monitor(cmd, web_hook, idle_timeout=60):
    """运行命令并监控输出和退出"""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    last_output_time = time.time()

    def reader_thread():
        nonlocal last_output_time
        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            if line:
                print("[子进程输出]", line)
                last_output_time = time.time()
        process.stdout.close()

    t = threading.Thread(target=reader_thread, daemon=True)
    t.start()

    push_report(web_hook, f"任务已启动: {' '.join(cmd)}")

    while True:
        ret = process.poll()
        if ret is not None:
            if ret == 0:
                push_report(web_hook, f"任务已正常结束 ✅: {' '.join(cmd)}")
            else:
                push_report(web_hook, f"任务异常退出 ❌ (退出码 {ret}): {' '.join(cmd)}")
            break

        if time.time() - last_output_time > idle_timeout:
            push_report(web_hook, f"任务无输出超过 {idle_timeout}s ⚠️: {' '.join(cmd)}")
            last_output_time = time.time()

        time.sleep(5)
