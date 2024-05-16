import requests
from bs4 import BeautifulSoup
from colorama import Style, Fore, Back
import time
import urllib.request as urr
import webbrowser as wb
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import ctypes
import ast

def main_title():
    ctypes.windll.kernel32.SetConsoleTitleW("t.me/oussxh")

valid_inputs = {"y", "Y", "yes", "Yes", "yEs", "yeS", "YES", "YEs", "YeS", "yES"}

#########################
##### SCRAPER FUNCTION ####
#########################
def scrapper():
    url = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=500&page=4&sort_by=lastChecked&sort_type=desc')
    if url.status_code != 200:
        print("Bad response")
        exit()
    else:
        data = url.json()
        iplist = [(item["ip"], item["port"], item["protocols"]) for item in data["data"]]

    i = 0
    with open("proxies/hits.txt", "w") as f, open("proxies/type.txt", "w") as ft:
        for ip, port, protocols in iplist:
            i += 1
            # Print in console
            print(Fore.WHITE + "[" + Fore.GREEN + "SUCCESS" + Fore.WHITE + "]: " + Fore.WHITE + ip + ":" + port)
            # Insert into txt file
            f.write(ip + ":" + port + "\n")
            ft.write(str(protocols) + "\n")

    # Printed message after the scraping is completed
    print("\n" + Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Completed! " + "Total Proxies: " + str(i) + "\n")

    # Cool display in browser :P
    userinput = input(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Show results in browser y/n: ")
    if userinput in valid_inputs:
        wb.open_new_tab("index.html")
    else:
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Back to main menu!\n")
        time.sleep(2)
    ################################
    main()

# Load and check proxies
def loadproxy():
    with open("proxies/hits.txt", "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    with open("proxies/type.txt", "r") as file2:
        proxytypes = [ast.literal_eval(line.strip())[0] for line in file2 if line.strip()]
    liveproxies = open("proxies/live_proxies.txt", "w")

    live_count = 0
    dead_count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(pchecker, proxy, proxytypes[idx]): proxy for idx, proxy in enumerate(proxies)}

        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result[1]:
                    live_count += 1
                    print(Fore.WHITE + "[" + Fore.GREEN + "LIVE" + Fore.WHITE + "] " + f"{result[0]} is working!")
                    liveproxies.write(result[0] + "\n")
                    liveproxies.flush()
                else:
                    print(Fore.WHITE + "[" + Fore.RED + "DEAD" + Fore.WHITE + "] " + f"{proxy}")
                    dead_count += 1
            except Exception as exc:
                print(f"Proxy {proxy} generated an exception: {exc}")
            update_title(live_count,dead_count)
            time.sleep(0.1)

    liveproxies.close()

    backorexit = input(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Would you like to go back to main menu? y/n: ")
    main_title()
    if backorexit in valid_inputs:
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Loading main menu...\n")
        time.sleep(2)
        main()
    else:
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Good Bye!")
        exit()

# Proxy checker using requests
def pchecker(proxy, proxy_type):
    url = "http://www.google.com"
    proxies = {}
    if proxy_type == "socks5":
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
    elif proxy_type == "socks4":
        proxies = {
            "http": f"socks4://{proxy}",
            "https": f"socks4://{proxy}"
        }
    elif proxy_type == "http" or proxy_type == "https":
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return proxy, response.text
        else:
            return proxy, None
    except requests.RequestException:
        return proxy, None

# Updates CMD Title
def update_title(live_count, dead_count):
    ctypes.windll.kernel32.SetConsoleTitleW(f"LIVE: {live_count} | DEAD: {dead_count}")

# Main function
def main():

    # Header
    print(Fore.RED + "  _____  _              _____                                      \n |  __ \\(_)            / ____|                                     \n | |__) |_  __ _ ___  | (___   ___ _ __ __ _ _ __  _ __   ___ _ __ \n |  _  /| |/ _` / __|  \\___ \\ / __| '__/ _` | '_ \\| '_ \\ / _ \\ '__|\n | | \\ \\| | (_| \\__ \\  ____) | (__| | | (_| | |_) | |_) |  __/ |   \n |_|  \\_\\_|\\__,_|___/ |_____/ \\___|_|  \\__,_| .__/| .__/ \\___|_|   \n                                            | |   | |               \n                                            |_|   |_|               ")
    print(Fore.YELLOW + "\nSIMPLE PROXY SCRAPER/CHECKER TOOL MADE WITH LOVE OUT OF BOREDOM\n")
    print(Fore.WHITE + "***************************\n|                         |\n| Created by : oussxh     |\n|                         |\n***************************")
    print("")

    print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "[1] Launch Scraper")
    print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "[2] Launch Checker")
    print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "[3] GitHub Page")
    print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "[4] Close")
    numpick = input(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Enter your choice: ")

    if numpick == "1":
        scrapper()
    elif numpick == "2":
        loadproxy()
    elif numpick =="3":
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Opening Browser...\n\n")
        time.sleep(1)
        wb.open_new_tab("https://github.com/oussxh/rias-scraper")
        main()
    elif numpick == "4":
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Have a nice day!\n")
        exit()
    else:
        print(Fore.WHITE + "[" + Fore.RED + "RIAS" + Fore.WHITE + "]: " + "Wrong choice. Bye :)!\n")
        exit()

main_title()
print("\n")
main()
