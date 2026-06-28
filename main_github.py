import json, requests, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

# Telegram bilgileri
BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    if BOT_API and CHAT_ID:
        requests.post(f"https://api.telegram.org/bot{BOT_API}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def main():
    print("🚀 Bot başlatılıyor...")
    
    # Chrome ayarları
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled") # Bot korumasını aşmak için
    driver = webdriver.Chrome(options=opts)
    
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.load(f)
        
        for item in config.get("urls", []):
            print(f"🔗 Gidiliyor: {item['person']} ({item['store']})")
            driver.get(item['url'])
            
            # Stok kontrolü (Tıklama yok, sadece okuma)
            res = None
            store = item["store"].lower()
            
            if store == "zara": 
                res = check_stock_zara(driver, item["sizes"])
            elif store == "stradivarius": 
                res = check_stock_stradivarius(driver, item["sizes"])
            elif store == "bershka": 
                res = check_stock_bershka(driver, item["sizes"])
            
            if res:
                message = f"🛍️ <b>STOKTA:</b> {item['person']}\n<b>Beden:</b> {res}\n<a href='{item['url']}'>Ürüne Git</a>"
                send_telegram(message)
                print(f"✅ Stokta bulundu: {res}")
            else:
                print("❌ Stok yok veya beden bulunamadı.")
                
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
    finally:
        driver.quit()
        print("🏁 Bot kapandı.")

if __name__ == "__main__":
    main()
