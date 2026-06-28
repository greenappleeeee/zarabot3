from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_stock_zara(driver, sizes_to_check):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-action='size-selector-sizes']")))
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-action^='size-selector']")
        for btn in buttons:
            label = btn.text.strip()
            # Senin verdiğin listeden herhangi biri, butondaki yazının içinde geçiyor mu?
            if any(size in label for size in sizes_to_check):
                status = btn.get_attribute("data-qa-action")
                if status and ("in-stock" in status or "low-on-stock" in status):
                    return label
        return None
    except: return None

def check_stock_stradivarius(driver, sizes_to_check):
    return check_stock_zara(driver, sizes_to_check)

def check_stock_bershka(driver, sizes_to_check):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-qa-anchor='productDetailSize']")))
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']")
        for btn in buttons:
            label = btn.find_element(By.CSS_SELECTOR, "span.text__label").text.strip()
            if any(size in label for size in sizes_to_check):
                if "is-disabled" not in btn.get_attribute("class"):
                    return label
        return None
    except: return None
