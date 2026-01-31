import httpx
import argparse
import logging
from dataclasses import dataclass
                                                                          
# Default proxy sources - hardcoded so no external file is required
DEFAULT_SOURCES = [
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/https/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/protocols/http.txt",
    "https://raw.githubusercontent.com/ClearProxy/checked-proxy-list/main/http/raw/all.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/refs/heads/main/http.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/proxies.txt",
    "https://raw.githubusercontent.com/mzyui/proxy-list/refs/heads/main/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt"
    "https://github.com/vakhov/fresh-proxy-list/blob/master/https.txt",
    "https://raw.githubusercontent.com/elliottophellia/proxylist/refs/heads/master/results/http/global/http_checked.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/https/https.txt"
    
]


@dataclass
class Proxy:
    ip: str
    port: int
    protocol: str


# Configure logging to display thread information
logging.basicConfig(
    format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)


class ProxyScraper:
    """A simple HTTP proxy scraper using threading."""

    def __init__(self):
        self.proxies = []

    def fetch_proxies(self, url: str):
        """Fetch proxies from a given URL."""
        try:
            response = httpx.get(url)
            if response.status_code == 200:
                proxy_list = response.text.splitlines()
                self.proxies.extend(proxy_list)
                print(f"Fetched {len(proxy_list)} proxies from {url}")
            else:
                logging.error(f"Failed to fetch proxies from {url}")
        except Exception as e:
            logging.error(f"Error fetching from {url}: {e}")

    def fetch_from_multiple_urls(self, urls: list[str]):
        """Fetch proxies from multiple URLs."""
        for url in urls:
            self.fetch_proxies(url)
        print(f"Total proxies collected: {len(self.proxies)}")

    def fetch_proxies_from_file(self, file_path: str):
        """Fetch proxies from a local file containing proxy URLs."""
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
            print(f"Found {len(urls)} proxy sources in file.")
            self.fetch_from_multiple_urls(urls)

    def dedupe_proxies(self):
        """Remove duplicate proxies from the list."""
        self.proxies = list(set(self.proxies))
        logging.info(f"Deduped proxies: {len(self.proxies)} unique proxies remaining")


    def return_fetched_proxies(self) -> list[Proxy]:
        """Return a deduped list of proxies with protocols ready for checking."""
        self.dedupe_proxies()
        result = []
        
        # Track which sources were HTTPS to inform protocol guessing
        https_sources = ["https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/https/data.txt",
                        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
                        # Add other HTTPS sources from DEFAULT_SOURCES
                        ]
        
        for proxy_str in self.proxies:
            proxy_str = proxy_str.strip()
            if not proxy_str:
                continue

            # Check if proxy already has a protocol prefix
            protocol = "http"  # default protocol
            
            # Try to determine protocol from the format
            if proxy_str.startswith("http://"):
                protocol = "http"
                proxy_str = proxy_str[7:]
            elif proxy_str.startswith("https://"):
                protocol = "https"
                proxy_str = proxy_str[8:]
            elif proxy_str.startswith("socks5://") or proxy_str.startswith("socks4://"):
                # Skip SOCKS proxies if you only want HTTP/HTTPS
                continue
            
            # Parse ip:port format
            if ":" in proxy_str:
                parts = proxy_str.split(":")
                if len(parts) != 2:
                    continue
                ip = parts[0]
                try:
                    port = int(parts[1])
                except ValueError:
                    continue

                # Validate IP format (basic check)
                if not ip or not all(c.isdigit() or c == '.' or c.isalpha() for c in ip.split('.')[0]):
                    continue

                result.append(Proxy(ip=ip, port=port, protocol=protocol))
        
        return result


import time


def print_banner():
    print("  ▄ .▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄·.▄▄ ·      ▄▄·  ▄ .▄▄▄▄ . ▄▄· ▄ •▄ ▄▄▄ .▄▄▄  ")
    print("  ██▪▐█•██  •██  ▐█ ▄█▐█ ▀.     ▐█ ▌▪██▪▐█▀▄.▀·▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·")
    print("  ██▀▐█ ▐█.▪ ▐█.▪ ██▀·▄▀▀▀█▄    ██ ▄▄██▀▐█▐▀▀▪▄██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ ")
    print("  ██▌▐▀ ▐█▌· ▐█▌·▐█▪·•▐█▄▪▐█    ▐███▌██▌▐▀▐█▄▄▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌")
    print("  ▀▀▀ · ▀▀▀  ▀▀▀ .▀    ▀▀▀▀     ·▀▀▀ ▀▀▀ · ▀▀▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀")
    print("---------------------------------------------------------------")
    time.sleep(1)


def main():

    parser = argparse.ArgumentParser(description="HTTP Proxy Scraper")
    parser.add_argument(
        "-s",
        "--sources",
        help="Path to a file containing proxy source URLs (uses built-in sources by default)",
    )
    args = parser.parse_args()

    scraper = ProxyScraper()

    if args.sources:
        print(f"Loading sources from file: {args.sources}")
        scraper.fetch_proxies_from_file(args.sources)
    else:
        print(f"Using {len(DEFAULT_SOURCES)} built-in proxy sources")
        scraper.fetch_from_multiple_urls(DEFAULT_SOURCES)

    print(f"{len(scraper.proxies)} proxies collected.")
    proxies = scraper.return_fetched_proxies()
    with open("unchecked.txt", "w") as f:
        for proxy in proxies:
            f.write(f"{proxy.protocol}://{proxy.ip}:{proxy.port}\n")
    print(f"{len(proxies)} proxies written to unchecked.txt")


if __name__ == "__main__":
    main()
