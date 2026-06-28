from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_stock_zara(driver, sizes_to_check):
    try:
        # Tıklama yapmıyoruz, sadece bekleme yapıyoruz
        wait = WebDriverWait(driver, 10)
        # Beden listesini bul
        size_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-action='size-selector-sizes']")))
        elements = size_list.find_elements(By.CSS_SELECTOR, "li")
        
        for li in elements:
            try:
                label = li.find_element(By.CSS_SELECTOR, "div[data-qa-qualifier='size-selector-sizes-size-label']").text.strip()
                if label in sizes_to_check:
                    # Butonun durumunu (stokta mı değil mi) oku
                    button = li.find_element(By.CSS_SELECTOR, "button")
                    status = button.get_attribute("data-qa-action")
                    if status in ["size-in-stock", "size-low-on-stock"]:
                        return label
            except: continue
        return None
    except Exception as e:
        print(f"Zara kontrol hatası: {e}")
        return None

def check_stock_stradivarius(driver, sizes_to_check):
    # Stradivarius aynı altyapıyı kullanır
    return check_stock_zara(driver, sizes_to_check)

def check_stock_bershka(driver, sizes_to_check):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-anchor='productDetailSize']")))
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']")
        for btn in buttons:
            label = btn.find_element(By.CSS_SELECTOR, "span.text__label").text.strip()
            if label in sizes_to_check:
                # 'is-disabled' sınıfı yoksa stoktadır
                if "is-disabled" not in btn.get_attribute("class"):
                    return label
        return None
    except: return None
