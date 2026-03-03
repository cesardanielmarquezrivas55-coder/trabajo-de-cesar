from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


User = "standard_user"
Password = "secret_sauce"

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    #option.add_argument("--headless")
    option.add_argument("--window-size=1920,1080")
    driver = Chrome(service=service, options=option)
    driver.get("https://www.saucedemo.com/")
#login
    user_input = driver.find_element(By.ID, "user-name")
    user_input.send_keys(User)
    pass_input = driver.find_element(By.ID, "password")
    pass_input.send_keys(Password)
    button = driver.find_element(By.ID, "login-button")
    button.click()
#extraerdatos
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    product_data = []
    for product in products:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
        print(f"Nombre: {name}, Precio: {price}")
        product_data.append([name, price])

#cuadro con datos
    import pandas as pd
    df = pd.DataFrame(product_data, columns=["Nombre", "Precio"])
    print(df)


if __name__ == '__main__':
    main()