# Trendyol Fiyat Toplayıcı - Basit Sürüm

import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

search_input = input("Almak istediğiniz ürünü giriniz:")

# ---------------------------------------------------------------
# 1) Tarayıcıyı aç ve Trendyol'a git
# ---------------------------------------------------------------

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.trendyol.com/")
time.sleep(0.5)

# ---------------------------------------------------------------
# 2) Tüm Popları kapat
# ---------------------------------------------------------------

try:
    cerez_butonu = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cerez_butonu.click()
except :
    print("Çerez popundan çıkamadı.")

time.sleep(0.5)

for i in range(3):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    time.sleep(1)

    # class isminde "close" geçen ve ekranda görünen elemanlara tıkla

    close_buttons = driver.find_elements(By.CSS_SELECTOR, "[class*='close']")
    for button in close_buttons:
        try:
            if button.is_displayed():
                button.click()
                print("Tüm çerezler kapatıldı.")
                time.sleep(0.5)
        except:
            pass

    time.sleep(0.5)


# ---------------------------------------------------------------
# 3) Arama kutusuna ürünü yaz ve Enter'a bas
# ---------------------------------------------------------------

search_box_find = driver.find_elements(By.XPATH, "//*[contains(text(), 'Ürün, kategori veya marka ara')]")
print("Bulunan eleman sayısı:", len(search_box_find))

for search_box in search_box_find:
    if search_box.is_displayed():
        search_box.click()
        print("Arama kutusna tıklandı.")
        break

time.sleep(1)

arama_kutusu = driver.find_element(By.CSS_SELECTOR, "div.search-bar-new-input-active input")
arama_kutusu.send_keys(search_input)
arama_kutusu.send_keys(Keys.ENTER)
time.sleep(0.5)

# ---------------------------------------------------------------
# 5) ANA KARTI bul (tüm ürünleri içeren büyük kutu)
# ---------------------------------------------------------------

main_card= driver.find_element(By.CLASS_NAME, "search-result-content")

# ---------------------------------------------------------------
# 6) Ana kartın İÇİNDEKİ küçük kartları bul (her biri bir ürün)
# ---------------------------------------------------------------

small_cards = driver.find_elements(By.CLASS_NAME, "product-card")
print(len(small_cards))

product = []

for small_card in small_cards:
    try :
        brand = small_card.find_element(By.CLASS_NAME, "product-brand").text
        name = small_card.find_element(By.CLASS_NAME, "product-name").text
        title = brand + " " + name
        price = small_card.find_element(By.CSS_SELECTOR, ".sale-price, .price-section").text
        link = small_card.get_attribute("href")

        product.append([title, price, link])
    except:
        print("bu kart okunamadı")

# ---------------------------------------------------------------
# 8) Sonuçları CSV dosyasına yaz
# ---------------------------------------------------------------

with open(file="scraping.csv",mode="w",encoding="utf-8") as file:
    writer = csv.writer(file,delimiter=";")
    writer.writerow(["Ürün Adı", "Fiyat", "Link"])
    writer.writerows(product)

print(len(product), "dosyaya kaydedildi")

# ---------------------------------------------------------------
# 9) Tarayıcıyı kapat
# ---------------------------------------------------------------

driver.quit()






