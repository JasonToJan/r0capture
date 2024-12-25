import subprocess
import time
import sys
import os
import signal
import platform


def kill_existing_frida_server():
    """终止已经运行的frida-server进程"""
    try:
        # 在Android设备上查找并终止frida-server进程
        pid_cmd = "adb shell \"su -c 'ps -ef | grep frida-server | grep -v grep | awk \"{print \\$2}\"'\""
        pid = subprocess.check_output(pid_cmd, shell=True).decode().strip()

        if pid:
            kill_cmd = f"adb shell \"su -c 'kill -9 {pid}'\""
            subprocess.run(kill_cmd, shell=True, check=True)
            print(f"Killed existing frida-server (PID: {pid})")
            time.sleep(1)  # 等待进程完全终止
    except subprocess.CalledProcessError:
        pass  # 如果没有找到进程，就忽略错误


def get_frida_ps_path():
    """获取frida-ps的正确路径"""
    try:
        # 先尝试通过pip找到安装位置
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "frida-tools"],
            capture_output=True,
            text=True,
            check=True
        )

        # 确保frida-tools已安装
        if "Location:" not in result.stdout:
            print("Installing frida-tools...")
            subprocess.run([sys.executable, "-m", "pip", "install", "frida-tools"], check=True)

            # 在Windows上查找frida-ps.exe
        if platform.system() == "Windows":
            # 使用where命令查找frida-ps
            try:
                result = subprocess.run(
                    "where frida-ps",
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                return result.stdout.splitlines()[0].strip()
            except subprocess.CalledProcessError:
                # 如果where命令失败，尝试在Scripts目录中查找
                base_path = os.path.dirname(sys.executable)
                return os.path.join(base_path, "Scripts", "frida-ps.exe")
        else:
            # 在Unix系统上使用which命令
            result = subprocess.run(
                "which frida-ps",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
    except Exception as e:
        print(f"Error finding frida-ps: {e}")
        return None


def run_frida_server_and_list_processes():
    try:
        # 1. 先终止已存在的frida-server
        print("Checking for existing frida-server...")
        kill_existing_frida_server()

        # 2. 启动 frida-server
        print("Starting frida-server...")
        commands = [
            "su -c 'cd /data/local/tmp; ls; chmod 755 /data/local/tmp/frida-server-16.2.1-android-arm64; ./frida-server-16.2.1-android-arm64'"
        ]

        # 在后台执行frida-server
        server_process = subprocess.Popen(f'adb shell "{commands[0]}"', shell=True)

        # 等待frida-server启动
        print("Waiting for frida-server to start...")
        time.sleep(3)

        # 3. 获取frida-ps路径
        frida_ps_path = get_frida_ps_path()
        if not frida_ps_path:
            print("Error: Could not find frida-ps executable")
            return

        print(f"Using frida-ps at: {frida_ps_path}")

        # 4. 执行 frida-ps -U 并获取输出
        print("\nListing processes (frida-ps -U):")
        try:
            frida_ps_result = subprocess.run(
                f'"{frida_ps_path}" -U',
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print(frida_ps_result.stdout)
            if frida_ps_result.stderr:
                print("Error:", frida_ps_result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error running frida-ps: {e}")
            # 尝试直接使用命令名称
            try:
                frida_ps_result = subprocess.run(
                    "frida-ps -U",
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(frida_ps_result.stdout)
            except subprocess.CalledProcessError as e2:
                print(f"Failed to run frida-ps directly: {e2}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        print(traceback.format_exc())
    finally:
        try:
            # 如果需要在脚本结束时关闭frida-server，取消下面的注释
            # kill_existing_frida_server()
            pass
        except:
            pass


if __name__ == "__main__":
    # 确保使用的是非Windows Store版本的Python
    if "WindowsApps" in sys.executable:
        print("Warning: You are using Windows Store Python. This may cause permission issues.")
        print("Please install Python directly from python.org")

    run_frida_server_and_list_processes()