# headers相关参数
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36 '
}
headers_ranking = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36 ',
    'Referer': 'http://fund.eastmoney.com/data/fundranking.html'
}

# selenium路径
executable_path = "./selenium/chromedriver"
## 也可以将其放在绝对路径
## executable_path = "/Applications/chromedriver"

# 相关的URL
company_url = "http://fund.eastmoney.com/Data/FundRankScale.aspx"
initial_manager_url = "https://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=50&pi=1&sc=totaldays&st=desc"
manager_url = "https://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn=50&pi={0}&sc=totaldays&st=desc"
manager_mobile_url = "https://h5.1234567.com.cn/app/fund-manager/pages/manager/index?MGRID={0}"
index_fund_1_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=zs&rs=&gs=0&sc=3nzf&st=desc&sd=2020-03-15&ed=2021-03-15&qdii=001|&tabSubtype=,,001,,,&pi=1&pn=10000&dx=1&v=0.3696675203397466"
index_fund_2_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=3nzf&st=desc&sd=2020-03-15&ed=2021-03-15&qdii=318&tabSubtype=,,001,,,&pi=1&pn=10000&dx=1&v=0.5921614509277884"
index_fund_3_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=3nzf&st=desc&sd=2020-03-15&ed=2021-03-15&qdii=319&tabSubtype=,,001,,,&pi=1&pn=10000&dx=1&v=0.051883730174978826"
index_fund_url_list = [index_fund_1_url, index_fund_2_url, index_fund_3_url]
fund_url = "http://fund.eastmoney.com/{0}.html"

# 相关的文件路径
fund_company_data_path = "data/fund_company.csv"
fund_manager_info_data_path = "data/fund_manager_info.csv"
fund_manager_detail_data_path = "data/fund_manager_detail.csv"
all_fund_manager_data_path = "data/all_fund_manager.csv"
filter_fund_manager_data_path = "data/filter_fund_manager.csv"

# 数据分析的变量
rename_col_dict = {
    'now_amount_sum': 'manager_amount_sum', 'company_name_x': 'company_name', 'fund_count': 'company_fund_count',
    'fund_amount_sum': 'company_amount_sum', 'rank': 'company_rank', 'create_time': 'company_create_time'
}
col_list = [
    'manager_name', 'company_name', 'work_days', 'annualized_return', 'maximum_profit', 'maximum_drawdown',
    'now_best_fund_code', 'now_best_fund_name', 'now_best_fund_return', 'history_best_fund_return',
    'manager_amount_sum', 'manager_fund_count', 'company_amount_sum', 'company_fund_count', 'company_rank',
    'manager_id', 'company_id', 'company_create_time'
]
limit_work_days = 3650
limit_annualized_return = 10
limit_manager_amount_sum = 50
limit_company_amount_sum = 400