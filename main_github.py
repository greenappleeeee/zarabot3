import json, time, subprocess, requests, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraperHelpers import check_stock_zara, check_stock_bershka, check_stock_stradivarius

def main():
    print("🚀 Bot başlatılıyor...")
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)
    
    try:
        with open("config.json", "r", encoding='utf-8') as f: config = json.load(f)
        
        for item in config.get("urls", []):
            print(f"🔗 Gidiliyor: {item['url'][:50]}...")
            driver.get(item['url'])
            # Sayfanın sadece 2 saniye yüklenmesini bekle (takılmasın diye)
            time.sleep(2) 
            
            # Stok kontrolü
            res = None
            if item["store"] == "zara": res = check_stock_zara(driver, item["sizes"])
            # ... diğerleri
            
            if res:
                print(f"✅ Stokta: {res}")
                # Telegram mesajı gönder...
                
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        driver.quit()
        print("🏁 Bot kapandı.")

if __name__ == "__main__":
    main()
