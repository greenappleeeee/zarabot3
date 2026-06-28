from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_stock_zara(driver, sizes_to_check):
    try:
        # Zara'nın en güncel DOM yapısında bedenler 'li' elemanlarıdır
        # ve butonun 'data-qa-action' değeri durumu söyler.
        wait = WebDriverWait(driver, 10)
        
        # Beden seçim listesini bul
        size_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-action='size-selector-sizes']")))
        
        # Tüm liste elemanlarını al
        items = size_list.find_elements(By.TAG_NAME, "li")
        
        for item in items:
            # Bedeni oku (Örn: "S", "M")
            label_elem = item.find_element(By.CSS_SELECTOR, "div[data-qa-qualifier='size-selector-sizes-size-label']")
            label = label_elem.text.strip()
            
            if label in sizes_to_check:
                # Butonu bul
                btn = item.find_element(By.TAG_NAME, "button")
                
                # ZARA'NIN GERÇEK STOK MANTIĞI:
                # 'data-qa-action' değerine bakıyoruz
                status = btn.get_attribute("data-qa-action")
                
                # Eğer "size-in-stock" veya "size-low-on-stock" içeriyorsa alabiliriz
                if status and ("in-stock" in status or "low-on-stock" in status):
                    return label
        return None
        
    except Exception as e:
        print(f"Zara kontrol hatası: {type(e).__name__}")
        return None

def check_stock_stradivarius(driver, sizes_to_check):
    # Stradivarius Zara ile aynı altyapıyı kullanır (Inditex Grubu)
    return check_stock_zara(driver, sizes_to_check)
