import threading, requests, json, time, os, sys

save = []
print("Developer: github.com/mishakorzik")
list = input("proxy list (ex. list.txt) : ")
type = input("proxy type (ex. socks5)   : ")

read = open(list, "r")
get = read.read()
read.close()
get = get.split()

def check(proxy):
    try:
        ip, _ = proxy.split(":")
        check = requests.get("https://ipwho.is/", timeout=5, headers={"User-Agent": "he1zen proxy checker."}, proxies={"https": f"{type}://"+proxy}).json()
        dat2 = check["country_code"]
        dat3 = check["country"]
        dat4 = check["city"]
        print(proxy+" - "+dat2+" - "+dat3+", "+dat4)
        save.append(proxy)
    except:
        fail = True

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
