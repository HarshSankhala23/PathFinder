import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn, TextColumn
from rich import print
import argparse
from urllib.parse import urljoin


console = Console()

banner = """

 ██▓███   ▄▄▄     ▄▄▄█████▓ ██░ ██   █████▒██▓ ███▄    █ ▓█████▄ ▓█████  ██▀███  
▓██░  ██▒▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓██   ▒▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒████ ░▒██▒▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░ ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓░▒█░   ░██░▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░ ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒ ▒ ░   ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ▒   ▒▒ ░   ░     ▒ ░▒░ ░ ░      ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░░         ░   ▒    ░       ░  ░░ ░ ░ ░    ▒ ░   ░   ░ ░  ░ ░  ░    ░     ░░   ░ 
               ░  ░         ░  ░  ░        ░           ░    ░       ░  ░   ░     
                                                          ░                      

"""
console.print(banner, style="bold red")

def fuzz_url(target_url, wordlist, threads, timeout):
    def check_url(path):
        url = urljoin(target_url, path.strip())
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code in [200, 301, 302]:
                console.print(f"[bold green]{url}[/bold green] [red](Status: {response.status_code})[/red]")
                return url, response.status_code
        except requests.RequestException:
            pass
        return None

    with open(wordlist, 'r') as file:
        paths = [line.strip() for line in file.readlines()]

    total_paths = len(paths)

    console.print(f"[bold green][+] Starting PathFinder on {target_url}[/bold green]")
    console.print(f"[bold yellow]Total paths: {total_paths}, Threads: {threads}, Timeout: {timeout} seconds[/bold yellow]")

    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Fuzzing...", total=total_paths)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(check_url, path): path for path in paths}

            for future in as_completed(futures):
                progress.advance(task)
                result = future.result()
                if result:
                    results.append(result)

    console.print("[bold green][+] Fuzzing complete![/bold green]")
    if results:
        console.print("\n[bold green]Discovered paths:[/bold green]")
        for url, status in results:
            console.print(f"[bold green]{url}[/bold green] [red](Status: {status})[/red]")
    else:
        console.print("[bold red]No valid paths found.[/bold red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PathFinder - A Modern Directory & File Fuzzing Tool")
    parser.add_argument("url", help="Target URL (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds (default: 5.0)")

    args = parser.parse_args()

    try:
        fuzz_url(args.url, args.wordlist, args.threads, args.timeout)
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Fuzzing interrupted by user.[/bold red]")
