import threading, requests, json, time, os, sys
from urllib.parse import urlparse

save = []
print("Developer: github.com/mishakorzik")
print("Modified: Added support for authenticated proxies")
list = input("proxy list (ex. list.txt) : ")
type = input("proxy type (ex. http, socks5) : ")

read = open(list, "r")
get = read.read()
read.close()
get = get.split()

def parse_proxy(proxy_line):
    """Parse proxy from various formats and return (proxy_url, display_name)."""
    proxy_line = proxy_line.strip()
    
    # If it's already a full URL (http://user:pass@host:port)
    if proxy_line.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
        parsed = urlparse(proxy_line)
        display = f"{parsed.hostname}:{parsed.port}"
        # Return the full URL for requests, stripping the scheme if we'll add our own
        if parsed.username and parsed.password:
            return f"{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}", display
        return f"{parsed.hostname}:{parsed.port}", display
    
    # If it's user:pass@host:port format
    if '@' in proxy_line:
        return proxy_line, proxy_line.split('@')[1]
    
    # Simple ip:port format
    return proxy_line, proxy_line

def check(proxy):
    try:
        proxy_url, display = parse_proxy(proxy)
        full_proxy = f"{type}://{proxy_url}"
        
        check = requests.get(
            "https://ipwho.is/", 
            timeout=10, 
            headers={"User-Agent": "he1zen proxy checker."}, 
            proxies={"http": full_proxy, "https": full_proxy}
        ).json()
        
        dat2 = check.get("country_code", "??")
        dat3 = check.get("country", "Unknown")
        dat4 = check.get("city", "Unknown")
        print(f"✓ {display} - {dat2} - {dat3}, {dat4}")
        save.append(proxy)
    except Exception as e:
        pass  # Silent fail

print(f"\nChecking {len(get)} proxies...\n")

for proxy in get:
    proxies = threading.Thread(target=check, kwargs={"proxy": proxy})
    proxies.start()

time.sleep(20)
total = 0
os.system(f"rm -rf {type}.txt")
f = open(f"{type}.txt", "w")
for data in save:
    total = total + 1
    f.write(data+"\n")
f.close()
print("saved as: "+type+".txt")
total = str(total)
print(f"{total} proxies work!")
