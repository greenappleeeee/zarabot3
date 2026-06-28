import json, os, requests, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message, bot_api, chat_id):
    if not bot_api or not chat_id: return
    requests.post(f"https://api.telegram.org/bot{bot_api}/sendMessage", 
                  data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})

def load_config():
    with open("config.json", "r", encoding='utf-8') as f: return json.load(f)

def check_for_commands(bot_api, chat_id):
    url = f"https://api.telegram.org/bot{bot_api}/getUpdates"
    try:
        response = requests.get(url).json()
        if response.get("ok") and response["result"]:
            for update in response["result"]:
                if update.get("message", {}).get("text", "").lower() == "listele":
                    config = load_config()
                    items = "\n".join([f"• {i['person']}: {i['store']}" for i in config.get("urls", [])])
                    send_telegram_message(f"📋 <b>Takip edilenler:</b>\n\n{items}", bot_api, chat_id)
    except: pass

def main():
    print("🚀 Bot başlatılıyor...")
    check_for_commands(BOT_API, CHAT_ID)
    
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=opts)
    config = load_config()
    
    for item in config.get("urls", []):
        try:
            print(f"🔗 Gidiliyor: {item['person']}")
            driver.get(item['url'])
            time.sleep(3)
            res = None
            if item["store"].lower() == "zara": res = check_stock_zara(driver, item["sizes"])
            elif item["store"].lower() == "stradivarius": res = check_stock_stradivarius(driver, item["sizes"])
            elif item["store"].lower() == "bershka": res = check_stock_bershka(driver, item["sizes"])
            
            if res:
                send_telegram_message(f"🛍️ <b>STOKTA:</b> {item['person']} ({res})\n{item['url']}", BOT_API, CHAT_ID)
                print(f"✅ Stokta: {res}")
            else:
                print(f"❌ {item['person']} için stok yok.")
        except Exception as e:
            print(f"Hata: {e}")
    driver.quit()

if __name__ == "__main__":
    main()
