import json, os, requests, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

def send_msg(text):
    if BOT_API and CHAT_ID:
        requests.post(f"https://api.telegram.org/bot{BOT_API}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

def main():
    print("🚀 Bot başlatılıyor...")
    
    # Telegramdan 'listele' kontrolü
    try:
        updates = requests.get(f"https://api.telegram.org/bot{BOT_API}/getUpdates").json()
        if updates.get("result"):
            for u in updates["result"]:
                if u.get("message", {}).get("text", "").lower() == "listele":
                    with open("config.json", "r", encoding='utf-8') as f: config = json.load(f)
                    items = "\n".join([f"• {i['person']}" for i in config["urls"]])
                    send_msg(f"📋 <b>Takiptekiler:</b>\n{items}")
    except: pass

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=opts)
    
    try:
        with open("config.json", "r", encoding='utf-8') as f: config = json.load(f)
        for item in config.get("urls", []):
            driver.get(item['url'])
            time.sleep(3)
            
            res = None
            if item["store"] == "zara": res = check_stock_zara(driver, item["sizes"])
            # ... diğer mağazalar ...
            
            if res:
                send_msg(f"🛍️ <b>STOKTA:</b> {item['person']} ({res})\n{item['url']}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
