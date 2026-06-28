from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_stock_zara(driver, sizes_to_check):
    try:
        wait = WebDriverWait(driver, 10)
        size_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-action='size-selector-sizes']")))
        items = size_list.find_elements(By.TAG_NAME, "li")
        for item in items:
            label_elem = item.find_element(By.CSS_SELECTOR, "div[data-qa-qualifier='size-selector-sizes-size-label']")
            label = label_elem.text.strip()
            if label in sizes_to_check:
                btn = item.find_element(By.TAG_NAME, "button")
                status = btn.get_attribute("data-qa-action")
                if status and ("in-stock" in status or "low-on-stock" in status):
                    return label
        return None
    except: return None

def check_stock_stradivarius(driver, sizes_to_check):
    return check_stock_zara(driver, sizes_to_check)

def check_stock_bershka(driver, sizes_to_check):
    try:
        # Bershka için farklı bir CSS seçici
        wait = WebDriverWait(driver, 10)
        # Bershka beden listesi
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-anchor='productDetailSize']")))
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']")
        for btn in buttons:
            label = btn.find_element(By.CSS_SELECTOR, "span.text__label").text.strip()
            if label in sizes_to_check:
                # Bershka'da stokta olmayanlar 'is-disabled' sınıfına sahiptir
                if "is-disabled" not in btn.get_attribute("class"):
                    return label
        return None
    except: return None
