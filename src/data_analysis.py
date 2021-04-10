import pandas as pd

from src.constant import *


def read_csv_data(data_path):
    df = pd.read_csv(data_path, encoding='utf-8')
    return df


def write_csv_data(df, data_path):
    df.to_csv(data_path, encoding='utf-8', index=False)


def merge_all_data(data_path=all_fund_manager_data_path):
    print("----------")
    company_df = read_csv_data(fund_company_data_path)
    manager_info_df = read_csv_data(fund_manager_info_data_path)
    manager_info_df['now_best_fund_code'].astype('object')
    manager_detail_df = read_csv_data(fund_manager_detail_data_path)
    all_data_df = manager_info_df.merge(company_df, how='left', on='company_id')
    all_data_df = all_data_df.merge(manager_detail_df, how='left', on='manager_id')
    all_data_df.rename(columns=rename_col_dict, inplace=True)
    all_data_df.loc[:, 'manager_fund_count'] = all_data_df['now_funds_code'].apply(
        lambda x: len(x.split('|')) if len(x) > 0 else 0)
    res_df = all_data_df[col_list]
    write_csv_data(res_df, data_path)
    print("所有数据合并完毕")


def filter_fund_manager(
        work_days=limit_work_days, annualized_return=limit_annualized_return,
        manager_amount_sum=limit_manager_amount_sum, company_amount_sum=limit_company_amount_sum,
        data_path=filter_fund_manager_data_path
):
    print("----------")
    raw_df = read_csv_data(all_fund_manager_data_path)
    filter_df = raw_df.copy()
    filter_df['now_best_fund_code'] = filter_df['now_best_fund_code'].apply(
        lambda x: '0'*(6-len(str(x)))+str(x))
    if work_days is not None:
        filter_df = filter_df[filter_df['work_days'] >= work_days]
    if annualized_return is not None:
        filter_df.loc[:, 'annualized_return'] = filter_df['annualized_return'].apply(
            lambda x: float(str(x).split('%')[0]) if len(str(x)) > 0 else 0)
        filter_df = filter_df[filter_df['annualized_return'] >= annualized_return]
    if manager_amount_sum is not None:
        filter_df.loc[:, 'manager_amount_sum'] = filter_df['manager_amount_sum'].apply(
            lambda x: float(str(x).split('亿元')[0]) if '亿元' in str(x) else 0)
        filter_df = filter_df[filter_df['manager_amount_sum'] >= manager_amount_sum]
    if company_amount_sum is not None:
        filter_df = filter_df[filter_df['company_amount_sum'] >= company_amount_sum]
    filter_df.sort_values(by=['company_amount_sum', 'work_days', 'annualized_return'], ascending=[False, False, False], inplace=True)
    print("筛选后共有{0}个基金经理".format(filter_df.shape[0]))
    write_csv_data(filter_df, data_path)
