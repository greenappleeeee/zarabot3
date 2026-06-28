from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver_ready(driver):
    """Çerezleri kapatmak için tıklama yapar."""
    try:
        # Çerez kabul butonunu bul ve tıkla
        wait = WebDriverWait(driver, 5)
        accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_btn.click()
    except: pass

def check_stock_zara(driver, sizes_to_check):
    try:
        get_driver_ready(driver)
        wait = WebDriverWait(driver, 5)
        # Beden listesini bul
        size_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-action='size-selector-sizes']")))
        buttons = size_list.find_elements(By.TAG_NAME, "button")
        
        for btn in buttons:
            label = btn.text.strip()
            if label in sizes_to_check:
                # Beden butonuna tıkla (sayfanın durumu güncellemesi için)
                btn.click() 
                # Stokta olup olmadığını anla
                status = btn.get_attribute("data-qa-action")
                if status and "out-of-stock" not in status:
                    return label
        return None
    except: return None

def check_stock_stradivarius(driver, sizes_to_check):
    return check_stock_zara(driver, sizes_to_check)

def check_stock_bershka(driver, sizes_to_check):
    return check_stock_zara(driver, sizes_to_check)
