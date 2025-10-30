from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def pretty_print(result):
    if not any(result.values()):
        return

    console = Console()
    text = Text("Migration Check Failed", style="bold red")
    body = "\n"
    if result.get("DROP_DETECTED"):
        body += "🔥 [bold yellow]DROP[/] statements detected (possible data loss)\n"
    if result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
        body += "🧩 [bold yellow]FOREIGN KEY[/] without index (slow queries)\n"
    if result.get("NON_CONCURRENT_INDEX_BUILDS"):
        body += "⏳ [bold yellow]INDEX[/] not built concurrently (table locks)\n"

    console.print(Panel(body, title=text))
