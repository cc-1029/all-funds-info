import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import demjson
import pandas as pd

from src.constant import *


def selenium_option_settings():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    return chrome_options, option


def get_company_data():
    print("----------")
    company_response = requests.get(url=company_url, headers=headers)
    print("基金公司信息已爬取")
    company_info_list = demjson.decode(company_response.text.split('json=')[1])['datas']
    save_company_data(company_info_list)
    print("基金公司信息已保存")
    time.sleep(1)


def save_company_data(company_info_list, data_path=fund_company_data_path):
    company_id_list, company_full_name_list, create_time_list, fund_count_list, general_manager_list, \
    company_abbr_list, fund_amount_sum_list, rank_list, company_name_list, update_time_list = \
        [], [], [], [], [], [], [], [], [], []
    for company_info in company_info_list:
        company_id_list.append(company_info[0])
        company_full_name_list.append(company_info[1])
        create_time_list.append(company_info[2])
        fund_count_list.append(company_info[3])
        general_manager_list.append(company_info[4])
        company_abbr_list.append(company_info[5])
        fund_amount_sum_list.append(company_info[7])
        rank_list.append(len(company_info[8]))
        company_name_list.append(company_info[9])
        update_time_list.append(company_info[11])
    company_info_dict = {
        'company_id': company_id_list,
        'company_name': company_name_list,
        'fund_amount_sum': fund_amount_sum_list,
        'fund_count': fund_count_list,
        'rank': rank_list,
        'create_time': create_time_list,
        'company_full_name': company_full_name_list,
        'company_abbr': company_abbr_list,
        'general_manager': general_manager_list,
        'update_time': update_time_list
    }
    company_info_df = pd.DataFrame(company_info_dict)
    company_info_df.to_csv(data_path, encoding='utf-8', index=False)


def get_manager_data():
    get_manager_info_data()
    get_manager_detail_data()


def get_manager_info_data():
    print("----------")
    initial_response = requests.get(url=initial_manager_url, headers=headers)
    pages = demjson.decode(initial_response.text.split('returnjson= ')[1])['pages']
    manager_info_list = []
    for i in range(pages):
        manager_id_url = manager_url.format(i + 1)
        manager_id_response = requests.get(url=manager_id_url, headers=headers)
        manager_id_data = demjson.decode(manager_id_response.text.split('returnjson= ')[1])['data']
        manager_info_list.extend(manager_id_data)
        print("基金经理基本信息第{0}页已爬取".format(i + 1))
        time.sleep(1)
    save_manager_info_data(manager_info_list)
    print("基金经理基本信息已保存")


def save_manager_info_data(manager_info_list, data_path=fund_manager_info_data_path):
    manager_id_list, manager_name_list, company_id_list, company_name_list, now_funds_code_list, \
    now_funds_name_list, work_days_list, now_best_fund_return_list, now_best_fund_code_list, now_best_fund_name_list, \
    now_amount_sum_list, history_best_fund_return_list = [], [], [], [], [], [], [], [], [], [], [], []
    for manager_info in manager_info_list:
        manager_id_list.append(manager_info[0])
        manager_name_list.append(manager_info[1])
        company_id_list.append(manager_info[2])
        company_name_list.append(manager_info[3])
        now_funds_code_list.append(manager_info[4].replace(',', '|'))
        now_funds_name_list.append(manager_info[5].replace(',', '|'))
        work_days_list.append(manager_info[6])
        now_best_fund_return_list.append(manager_info[7])
        now_best_fund_code_list.append(manager_info[8])
        now_best_fund_name_list.append(manager_info[9])
        now_amount_sum_list.append(manager_info[10])
        history_best_fund_return_list.append(manager_info[11])
    manager_info_dict = {
        'manager_id': manager_id_list,
        'manager_name': manager_name_list,
        'company_id': company_id_list,
        'company_name': company_name_list,
        'work_days': work_days_list,
        'now_amount_sum': now_amount_sum_list,
        'history_best_fund_return': history_best_fund_return_list,
        'now_best_fund_return': now_best_fund_return_list,
        'now_best_fund_code': now_best_fund_code_list,
        'now_best_fund_name': now_best_fund_name_list,
        'now_funds_code': now_funds_code_list,
        'now_funds_name': now_funds_name_list
    }
    manager_info_df = pd.DataFrame(manager_info_dict)
    manager_info_df.to_csv(data_path, encoding='utf-8', index=False)


def get_manager_detail_data(data_path=fund_manager_info_data_path):
    manager_detail_list = []
    manager_info_df = pd.read_csv(data_path)
    more_than_2000_df = manager_info_df[manager_info_df['work_days'] >= 2000]
    manager_id_list = list(more_than_2000_df['manager_id'])
    chrome_options, option = selenium_option_settings()
    for i, manager_id in tqdm(enumerate(manager_id_list)):
        browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options, options=option)
        manager_detail_url = manager_mobile_url.format(manager_id)
        try:
            browser.get(manager_detail_url)
            wait = WebDriverWait(browser, 3)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'column-item')))
            html = browser.page_source
            manager_detail_data = parse_manager_detail_data(html)
            manager_detail_data.insert(0, manager_id)
            manager_detail_list.append(manager_detail_data)
        except:
            pass
        finally:
            browser.quit()
        time.sleep(0.3)
        if (i + 1) % 100 == 0:
            print("基金经理详情信息前{0}页已爬取".format(i + 1))
    save_manager_detail_data(manager_detail_list)


def parse_manager_detail_data(html):
    manager_detail_data = []
    soup = BeautifulSoup(html, "lxml")
    info_table = soup.find_all(attrs={'class': 'column-item weex-ct weex-div'})
    for info in info_table:
        detail_data = info.find(name='p').text
        manager_detail_data.append(detail_data)
    return manager_detail_data


def save_manager_detail_data(manager_detail_list, data_path=fund_manager_detail_data_path):
    manager_id_list, maximum_profit_list, maximum_drawdown_list, annualized_return_list, last_month_return_list, \
    last_season_return_list, last_year_return_list = [], [], [], [], [], [], []
    for manager_detail in manager_detail_list:
        manager_id_list.append(manager_detail[0])
        maximum_profit_list.append(manager_detail[4])
        maximum_drawdown_list.append(manager_detail[5])
        annualized_return_list.append(manager_detail[6])
        last_month_return_list.append(manager_detail[7])
        last_season_return_list.append(manager_detail[8])
        last_year_return_list.append(manager_detail[9])
    manager_detail_dict = {
        'manager_id': manager_id_list,
        'maximum_profit': maximum_profit_list,
        'maximum_drawdown': maximum_drawdown_list,
        'annualized_return': annualized_return_list,
        'last_month_return': last_month_return_list,
        'last_season_return': last_season_return_list,
        'last_year_return': last_year_return_list
    }
    manager_detail_df = pd.DataFrame(manager_detail_dict)
    manager_detail_df.to_csv(data_path, encoding='utf-8', index=False)


def get_all_data():
    get_company_data()
    get_manager_data()