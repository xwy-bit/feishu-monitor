import os
import json
import click
import getpass
from feishu_monitor.core import run_and_monitor
import sys

CONFIG_DIR = os.path.expanduser("~/.feishu_monitor")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def print_logo():
    logo = r"""         
          :---------------:             
              .-------------:            
                .------------: .:-:.    
  :-             :----------=*#######+: 
  :+-             :-------=###########: 
  :+++=            .----+###########*   
  :++++++++++=:   :*##############:        
  :++++++++++++++++++++*#####**-        
  :++++++++++++++++++++++++++-           
   -++++++++++++++++++++++=.               
         .-==+++++=-:                                  
         Feishu Monitor CLI
    """
    print(logo)

def save_webhook(webhook):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"webhook": webhook}, f)

def load_webhook():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("webhook")
    return None


@click.group(invoke_without_command=True, context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def cli(ctx, command):
    """Feishu Monitor CLI"""
    if ctx.invoked_subcommand is None:
        # 没有子命令时，默认执行 run
        webhook = load_webhook()
        if not webhook:
            click.echo("❌ 请先运行: feishu login")
            sys.exit(1)

        if not command:
            click.echo("❌ 必须指定要运行的命令")
            sys.exit(1)

        run_and_monitor(list(command), webhook, idle_timeout=60)



@cli.command()
@click.option("--show-input", is_flag=True, help="是否明文输入 webhook")
def login(show_input):
    """登录并保存 webhook"""
    print_logo()
    if show_input:
        webhook = input("请输入飞书 webhook: ").strip()
    else:
        import getpass
        webhook = getpass.getpass("请输入飞书 webhook (输入时不显示): ").strip()

    if webhook:
        save_webhook(webhook)
        click.echo("✅ Webhook 已保存")
    else:
        click.echo("❌ 输入为空，未保存")


@cli.command()
def whoami():
    """查看当前保存的 webhook"""
    webhook = load_webhook()
    if webhook:
        masked = webhook[:10] + "..." + webhook[-5:]
        click.echo(f"当前 webhook: {masked}")
    else:
        click.echo("❌ 还没有登录，请运行: feishu login")


