import json
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

def check_for_commands(bot_api, chat_id):
    """Telegram'dan gelen 'listele' komutunu kontrol eder."""
    url = f"https://api.telegram.org/bot{bot_api}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok") and response["result"]:
            for update in response["result"]:
                msg = update.get("message", {}).get("text", "").lower()
                if msg == "listele":
                    # Config dosyasını oku
                    config = load_config()
                    items = "\n".join([f"• {i['person']}: {i['store']}" for i in config.get("urls", [])])
                    summary = f"📋 <b>Takip edilen ürünler:</b>\n\n{items}"
                    send_telegram_message(summary, bot_api, chat_id)
                    # Not: Normalde burada offset kullanarak mesajı 'okundu' işaretlemek gerekir 
                    # ama basit olması için sadece listeyi göndermesini sağladık.
    except Exception as e:
        print(f"Komut kontrol hatası: {e}")

# Telegram Bilgileri (GitHub Secrets'tan gelir)
BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message, bot_api, chat_id):
    """Telegram'a mesaj gönderir."""
    if not bot_api or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_api}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram mesajı gönderilemedi: {e}")

def load_config():
    """Config dosyasını yükler."""
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Config yükleme hatası: {e}")
        return {"urls": []}

def main():
    print("🚀 Bot başlatılıyor...")
    check_for_commands(BOT_API, CHAT_ID) # Listele komutunu burada dinliyor
    # ... botun geri kalanı ...
    
    # Chrome ayarları (Bot algılanmaması için en kararlı mod)
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=opts)
    config = load_config()
    
    found_stock = False
    
    try:
        for item in config.get("urls", []):
            try:
                print(f"🔗 Gidiliyor: {item.get('person', 'Bilinmeyen')} ({item.get('store', 'Mağaza')})")
                driver.get(item['url'])
                
                # Sayfanın yüklenmesi için kısa ve güvenli bekleme
                time.sleep(3) 
                
                res = None
                store = item["store"].lower()
                
                # Sadece okuma yapan fonksiyonları çağırıyoruz
                if store == "zara": 
                    res = check_stock_zara(driver, item["sizes"])
                elif store == "stradivarius": 
                    res = check_stock_stradivarius(driver, item["sizes"])
                elif store == "bershka":
                    res = check_stock_bershka(driver, item["sizes"])
                
                if res:
                    print(f"✅ Stokta bulundu: {res}")
                    message = f"🛍️ <b>STOKTA:</b> {item.get('person')}\n<b>Beden:</b> {res}\n<a href='{item['url']}'>Ürüne Git</a>"
                    send_telegram_message(message, BOT_API, CHAT_ID)
                    found_stock = True
                else:
                    print(f"❌ {item.get('person')} için stok yok.")
                    
            except Exception as e:
                print(f"❌ Bu ürün için hata: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Genel hata: {e}")
    finally:
        driver.quit()
        print("🏁 Bot kapandı.")

if __name__ == "__main__":
    main()
