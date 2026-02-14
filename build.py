import os
import subprocess
import sys

def build():
    print("开始打包电子教鞭工具...")
    
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = sys.executable
    
    print(f"使用Python: {venv_python}")
    
    print("检查并安装PyInstaller...")
    subprocess.run([venv_python, "-m", "pip", "install", "pyinstaller"], check=True)
    
    print("开始打包...")
    cmd = [
        venv_python, "-m", "PyInstaller",
        "--name=电子教鞭工具",
        "--windowed",
        "--onefile",
        "--clean",
        "--noconfirm",
        "-y",
        "src/main.py"
    ]
    
    result = subprocess.run(cmd, check=False)
    
    if result.returncode == 0:
        print("\n打包成功!")
        print("可执行文件位于: dist/电子教鞭工具.exe")
    else:
        print("\n打包失败!")
        sys.exit(1)

if __name__ == "__main__":
    build()
