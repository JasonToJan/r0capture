import subprocess
import sys
import os

# 设置应用名称变量
app_name = "HungerStation"


def run_script():
    # pcap文件使用与应用名称相同的名称
    pcap_file = f"{app_name}.pcap"

    # 使用sys.executable获取当前Python解释器的路径
    python_executable = sys.executable

    # 获取r0capture.py的完整路径（假设它与当前脚本在同一目录下）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    r0capture_path = os.path.join(script_dir, "r0capture.py")

    # 构建命令
    command = [python_executable, r0capture_path, "-U", app_name, "-v", "-p", pcap_file]

    try:
        print(f"执行命令: {' '.join(command)}")

        # 检查r0capture.py是否存在
        if not os.path.exists(r0capture_path):
            print(f"错误: 找不到文件 {r0capture_path}")
            print("请确保r0capture.py与此脚本在同一目录下")
            return

            # 使用Popen来实时显示输出
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # 实时读取并打印输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

                # 等待进程结束并获取返回码
        return_code = process.poll()

        if return_code != 0:
            print(f"\n脚本执行失败，返回码: {return_code}")
        else:
            print("\n脚本执行成功完成")

    except Exception as e:
        print(f"\n执行过程中发生错误: {str(e)}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"Python解释器路径: {python_executable}")
        print(f"r0capture.py期望路径: {r0capture_path}")


if __name__ == "__main__":
    run_script()