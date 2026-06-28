from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_stock_zara(driver, sizes_to_check):
    try:
        # Zara bazen farklı etiketler kullanır, en güncel olanları deniyoruz
        selectors = [
            "ul[data-qa-action='size-selector-sizes']",
            "ul.size-selector-list",
            "div.product-size-selector"
        ]
        
        for selector in selectors:
            try:
                wait = WebDriverWait(driver, 5)
                size_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                
                # Tüm butonları bul
                buttons = size_list.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    label = btn.text.strip()
                    if label in sizes_to_check:
                        # Eğer buton "disabled" değilse stoktadır
                        if not btn.get_attribute("disabled"):
                            return label
                return None
            except:
                continue
        return None
    except Exception as e:
        print(f"Zara genel okuma hatası")
        return None

def check_stock_stradivarius(driver, sizes_to_check):
    # Stradivarius için de Zara mantığı çalışır
    return check_stock_zara(driver, sizes_to_check)
