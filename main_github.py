import json
import os
import subprocess
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{BOT_API}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

def get_telegram_commands():
    try:
        res = requests.get(f"https://api.telegram.org/bot{BOT_API}/getUpdates").json()
        if res.get("ok") and res["result"]:
            for update in res["result"]:
                msg = update.get("message", {}).get("text", "").lower()
                if msg == "listele":
                    config = load_config()
                    items = "\n".join([f"- {i['person']}: {i['store']}" for i in config['urls']])
                    send_msg(f"📋 <b>Takip Edilenler:</b>\n{items}")
                    # Mesajı işlendi işaretlemek için offset kullanmalı (Basitlik için atlandı)
    except: pass

def load_config():
    with open("config.json", "r", encoding='utf-8') as f: return json.load(f)

def save_and_push(config):
    with open("config.json", "w", encoding='utf-8') as f: json.dump(config, f, indent=2, ensure_ascii=False)
    if os.getenv('GITHUB_ACTIONS'):
        subprocess.run(['git', 'config', '--global', 'user.name', 'Stock Bot'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'], check=True)
        subprocess.run(['git', 'add', 'config.json'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Stok bulundu, config güncellendi'], check=True)
        subprocess.run(['git', 'push'], check=True)

def main():
    get_telegram_commands() # Listele komutunu kontrol et
    config = load_config()
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=opts)
    
    new_urls = []
    found_stock = False

    for item in config.get("urls", []):
        driver.get(item["url"])
        time.sleep(3)
        res = None
        s = item["store"].lower()
        if s == "zara": res = check_stock_zara(driver, item["sizes"])
        elif s == "bershka": res = check_stock_bershka(driver, item["sizes"])
        elif s == "stradivarius": res = check_stock_stradivarius(driver, item["sizes"])
        
        if res:
            send_msg(f"🛍️ STOKTA: {item['person']} ({res})\n{item['url']}")
            found_stock = True
        else:
            new_urls.append(item)
            
    if found_stock:
        config["urls"] = new_urls
        save_and_push(config)
        
    driver.quit()

if __name__ == "__main__":
    main()
