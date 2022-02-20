import pandas as pd

pd.set_option('display.max_columns', 20)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options  # headless

options = Options()  # headless
options.headless = True  # headless

s = Service('./geckodriver.exe')

license_list = []
given_by_list = []
licensor_name_list = []
licensor_adres_list = []
inn_list = []
type_list = []

driver = webdriver.Firefox(options=options, service=s)

subjects = ['Алтайский+край']


def func_licenses():
    elements = driver.find_elements(By.CLASS_NAME, 'sectionRegistry__resultTableRow')

    try:
        for el in elements:  # licenses
            el_lics = el.find_elements(By.TAG_NAME, 'p')
            lic_mini_list = []
            for el in el_lics:
                lic = el.text
                lic_mini_list.append(lic)
            license_list.append(lic_mini_list)
    finally:
        pass

def func_given_by():
    try:
        given_by_list.append('-')  # given by list
        for i in range(1, 21):
            i = str(i)
            el_giv_n = driver.find_element(By.XPATH,
                                           '/ html / body / div[5] / div / section / div / div[4] / div[2] / div / a[' + i + '] / div[2] / div').text

            given_by_list.append(el_giv_n)
    finally:
        pass

def func_licensiar_name_and_adres():
    try:
        licensor_name_list.append('-')
        licensor_adres_list.append('-')
        for i in range(1, 21):  # licens name
            i = str(i)
            licensor_name = driver.find_element(By.XPATH,
                                                '/ html / body / div[5] / div / section / div / div[4] / div[2] / div / a[' + i + '] / div[4] / div').text

            licensor_name_list.append(licensor_name)

            # licens adr
            if driver.find_elements(By.XPATH,
                                    '/ html / body / div[5] / div / section / div / div[4] / div[2] / div / a[' + i + '] / div[4] / div[2]'):

                licensor_adr = driver.find_element(By.XPATH,
                                                   '/ html / body / div[5] / div / section / div / div[4] / div[2] / div / a[' + i + '] / div[4] / div[2]').text
                licensor_adres_list.append(licensor_adr)
            else:
                licensor_adres_list.append('-')
    finally:
        pass

def func_inn():
    try:  # inn list
        inn_list.append('-')
        for i in range(1, 21):
            i = str(i)
            inn = driver.find_element(By.XPATH,
                                      '/ html / body / div[5] / div / section / div / div[4] / div[2] / div / a[' + i + '] / div[5] / div')
            inn_list.append(inn.text)
    finally:
        pass

def func_type():
    try:  # type list
        type_list.append('-')
        for i in range(1, 21):
            i = str(i)
            type1 = driver.find_element(By.XPATH,
                                        '/html/body/div[5]/div/section/div/div[4]/div[2]/div/a[' + i + ']/div[6]/div[1]').text
            if driver.find_elements(By.XPATH,
                                    '/html/body/div[5]/div/section/div/div[4]/div[2]/div/a[' + i + ']/div[6]/div[2]'):
                type2 = driver.find_element(By.XPATH,
                                            '/html/body/div[5]/div/section/div/div[4]/div[2]/div/a[' + i + ']/div[6]/div[2]').text
            type_list.append(type1 + ' ' + type2)
    finally:
        pass


def pandas_df():
    df = pd.DataFrame()
    df['licence'] = license_list
    df['given_by'] = given_by_list
    df['licensor'] = licensor_name_list
    df['adres'] = licensor_adres_list
    df['INN'] = inn_list
    df['type'] = type_list
    print(df)
    df.to_csv('rpn_gov.csv', sep=';', encoding="utf-8-sig")


for sub in subjects:
    page = '1'
    url = 'https://rpn.gov.ru/licences/?name=&hazard_class=&region=' + sub + '&types=&inn=&org=&status=&page=page-' + page
    print(url)
    driver.get(url)
    pages = driver.find_element(By.XPATH, '/html/body/div[5]/div/section/div/div[4]/div[3]/div[1]/div[2]/a[6]').text
    pages = int(pages)
    driver.close()
    for page in range(1, pages+1):
        page = str(page)
        driver = webdriver.Firefox(options=options, service=s)
        driver.get(url)
        print('page ', page, ' is in process...')
        func_licenses()
        func_given_by()
        func_licensiar_name_and_adres()
        func_inn()
        func_type()

        driver.close()

    pandas_df()
