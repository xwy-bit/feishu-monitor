from setuptools import setup, find_packages

setup(
    name="feishu-monitor",
    version="0.1.0",
    description="监控命令运行状态并推送到飞书",
    author="Weiye Xu",
    packages=find_packages(),
    install_requires=["requests", "click"],
    entry_points={
        "console_scripts": [
            "feishu=feishu_monitor.cli:cli",
        ],
    },
    python_requires=">=3.7",
)
