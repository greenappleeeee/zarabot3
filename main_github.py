import json
import time
import random
import subprocess
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

# --- Telegram ve Config Fonksiyonları ---

def load_config():
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Config yüklenemedi: {e}")
        return None

def save_config_and_push(config):
    """Dosyayı kaydet ve GitHub'a gönder"""
    with open("config.json", "w", encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    if os.getenv('GITHUB_ACTIONS'):
        try:
            subprocess.run(['git', 'config', '--global', 'user.name', 'StockBot'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'], check=True)
            subprocess.run(['git', 'add', 'config.json'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Telegram uzerinden guncelleme [skip ci]'], check=True)
            subprocess.run(['git', 'push'], check=True)
            print("✅ GitHub'a başarıyla push edildi.")
        except Exception as e:
            print(f"❌ Git push hatası: {e}")

def send_telegram_message(message):
    bot_api = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    if not bot_api or not chat_id: return
    url = f"https://api.telegram.org/bot{bot_api}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})

def check_telegram_commands():
    bot_api = os.getenv("BOT_API")
    chat_id = os.getenv("CHAT_ID")
    if not bot_api: return
    
    url = f"https://api.telegram.org/bot{bot_api}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            config = load_config()
            for result in response["result"]:
                msg = result.get("message", {}).get("text", "")
                
                # Komut: /ekle [URL] [ISIM]
                if msg.startswith("/ekle "):
                    parts = msg.split(" ", 2)
                    if len(parts) >= 3:
                        new_item = {"store": "zara", "url": parts[1], "sizes": ["S"], "person": parts[2]}
                        config["urls"].append(new_item)
                        save_config_and_push(config)
                        send_telegram_message(f"✅ {parts[2]} için ürün eklendi.")
                
                # Komut: /listele
                elif msg == "/listele":
                    list_text = "\n".join([f"🛍️ {i['person']} - {i['url']}" for i in config["urls"]])
                    send_telegram_message(f"Takip edilen ürünler:\n{list_text}")
    except Exception as e:
        print(f"Telegram kontrol hatası: {e}")

# --- Stok Kontrol Fonksiyonları ---

def setup_chrome_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service('/usr/bin/chromedriver') if os.path.exists('/usr/bin/chromedriver') else Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    # 1. Telegram Komutlarını Kontrol Et
    check_telegram_commands()
    
    # 2. Stok Kontrolüne Başla
    config = load_config()
    if not config: return
    
    driver = setup_chrome_driver()
    
    for item in config["urls"]:
        try:
            driver.get(item["url"])
            time.sleep(2)
            # Burada scraperHelpers fonksiyonlarını kullanarak stok kontrolü yap
            # (Mevcut mantığını buraya ekleyebilirsin)
        except Exception as e:
            print(f"Hata: {e}")
            
    driver.quit()

if __name__ == "__main__":
    main()
