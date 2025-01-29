# -*- coding: utf-8 -*-
"""Techstreamdata_PhuongAnh.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ubj56M_82XqmzTDxG3RlV4r7rgofSjGA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""## Load dataset (cách 1):"""

df_customer_life_span = pd.read_excel(
"https://docs.google.com/spreadsheets/d/1by8tPHwOnq3uKYK2E7sA9VBUYoPM4p1Rnrm_Ss9cyHI/export?format=xlsx")

df_daily_mkt_spending = pd.read_excel("https://docs.google.com/spreadsheets/d/1AZOIThOV4P-0eYDge53ZwumVkfkHoYPWxst3k3Bv87c/export?format=xlsx")

df_monthly_expense = pd.read_excel("https://docs.google.com/spreadsheets/d/10OGbaywwMIqKgnPGy8VDvpBVtjyqln47iYa2lFhI9Mw/export?format=xlsx")

df_payroll = pd.read_excel("https://docs.google.com/spreadsheets/d/1c_WihqTZCQvNgxzmd-OwhR9i5diwtfxXVLyMn8R-Lp4/export?format=xlsx")

df_receipt_history = pd.read_excel("https://docs.google.com/spreadsheets/d/1qayqML1zCKdmtzutkcy9LWvE6xFRm6TGBEVkHHJKIuE/export?format=xlsx")

"""## Load dataset (cách 2):

filtered data in March 2023 only
"""

def read_file_ggsheet(file_id, month_col = None):
  # cách 2: df_ggsheet = pd.read_excel(f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx")
  df_ggsheet = pd.read_excel("https://docs.google.com/spreadsheets/d/"+ file_id + "/export?format=xlsx")
  if month_col is not None:
    df_202303 = df_ggsheet[(df_ggsheet[month_col].dt.month == 3) & (df_ggsheet[month_col].dt.year == 2023)]
    return df_202303
  else:
    return df_ggsheet

df_customer_life_span_data = read_file_ggsheet(file_id="1by8tPHwOnq3uKYK2E7sA9VBUYoPM4p1Rnrm_Ss9cyHI")
df_daily_mkt_spending_data = read_file_ggsheet(file_id="1AZOIThOV4P-0eYDge53ZwumVkfkHoYPWxst3k3Bv87c",month_col="date")
df_monthly_expense_data = read_file_ggsheet(file_id="10OGbaywwMIqKgnPGy8VDvpBVtjyqln47iYa2lFhI9Mw",month_col="month")
df_payroll_data = read_file_ggsheet(file_id="1c_WihqTZCQvNgxzmd-OwhR9i5diwtfxXVLyMn8R-Lp4",month_col="month")
df_receipt_history_data = read_file_ggsheet(file_id="1qayqML1zCKdmtzutkcy9LWvE6xFRm6TGBEVkHHJKIuE",month_col="date")

# regexp to extract string beetween 2 characters

# dynamic ngày tháng trong function bên trên -> dùng để lọc data cho báo cáo của tháng trước đó
#tìm date hiện tại, replace ngày thành 1,
#trừ ngày vừa tìm cho 1, dùng hàm tìm tháng và năm của ngày

df_receipt_history_data.head()

"""## 1 CAC : CUSTOMER ACQUISITION COST

với customer life span có tính chất seasonality.
không chọn được ngày start và churn date nên không lấy chỉ life time của user trong 1 tháng cụ thể.
trong tháng có thể bị ảnh hưởng bởi trend
hoặc at least là lấy trong cùng 1 năm.

Total sales and marketing expense
"""

# 1. Online ads: Daily Marketing spending --> Sum of Spending:
online_ad_cost = df_daily_mkt_spending_data.spending.sum()

# 2. Payroll of sales and mkt:
sale_mkt_salary = df_payroll_data[df_payroll_data["department"].isin(['Sales','Marketing'])]["paid"].sum()

# 3. Marketing sofware: Daily expense --> Category (Software Licenses) --> Item (item=saleforce)
mkt_software_cost = df_monthly_expense_data[df_monthly_expense_data["item"] == "Salesforce"]["amount"].sum()

# 4.Content creation: included trong chi phí online mkt



total_sale_mkt_espenses = sale_mkt_salary + mkt_software_cost + online_ad_cost


print('Total Salary of Sales & Marketing is: ', sale_mkt_salary)
print('Total Cost of marketing software is: ', mkt_software_cost)
print('Total cost of online ads is: ', online_ad_cost)
print('Total expense for sales and marketing is: ', total_sale_mkt_espenses)

df_receipt_history_data.head()

# number of new customer acquired: (không lấy trong bảng churn date vì sẽ bị miss data của những khách hàng chưa là churn)

#type of user: churn/ retain/ return

new_cust_count = df_receipt_history_data[df_receipt_history_data["new_customer"] == 1].new_customer.count()

#len(df_receipt_history_data[df_receipt_history_data["new_customer"] == 1]["customer_id"].unique())

print(new_cust_count)

cac = total_sale_mkt_espenses / new_cust_count

print('CAC is: ', cac)

"""## ARPU"""

# total revenue : recceipt amount -> sum
revenue_total = df_receipt_history_data.receipt_amount.sum()

#number of customer : rêcipt nistory -. count account unique
#num_cust = df_receipt_history_data.customer_id.unique().size
num_cust = len(df_receipt_history_data.customer_id.unique())

print('Total Revenue : ', revenue_total)
print('Number of customer: ', num_cust)

arpu = revenue_total / num_cust
print('APRU is: ', arpu)

"""## COGS

Dùng trong production
"""

# Expense for server and sofware license
# df_monthly_expense_data['category'].unique()
server_cost = df_monthly_expense_data[df_monthly_expense_data['category'] == 'Server Costs']['amount'].sum()

software_licenses_cost = df_monthly_expense_data[df_monthly_expense_data['item'].isin(['Atlassian Jira', 'Slack', 'Zoom'])]['amount'].sum()

# Direct relating labor cost --> Salary of Engineering in Payroll data:
labor_cost = df_payroll_data[df_payroll_data['department'] == 'Engineering'].paid.sum()

#COGS:
COGS = server_cost + software_licenses_cost + labor_cost

print(server_cost)
print(software_licenses_cost)
print(labor_cost)
print(COGS)

# the direct costs of producing the goods or services a company sells in March 2023 is 20840.

"""## GROSS MARGIN"""

# Sales revenue: revenue_total

# COGS:

# Gross Margin = (revenue - COGS) / Revenue * 100
gross_margin = (revenue_total - COGS) / revenue_total * 100

print('Gross margin is: ',gross_margin)

# gross margin of TechStream in March 2023 is around 74.9% means that the businesss heath of this company is quite good.

"""## LTV"""

# ARPU: arpu (calculated above)

# avg_lifespan_months: churn_date - start_date
# df_customer_life_span_data.head()
df_customer_life_span_data['cust_life_span'] = df_customer_life_span_data['churn_date']- df_customer_life_span_data['start_date']
df_customer_life_span_data['cust_life_span'].mean()
#np.average(df_customer_life_span_data['cust_life_span'])

# GrossMargin: gross_margin (calculated above)

cust_lifespan_month = (295 + ((5 * 3600 + 45 * 60 + 36) / (24 * 60 * 60))) / 31
ltv = arpu * cust_lifespan_month * (gross_margin /100)
print('LTV is: ', ltv)

df_customer_life_span_data['cust_life_span'].describe()

"""So, total revenue that TechStream can expect from a customer over the
entire duration of their relationship is around $2,028.5

## LTV/CAC
"""

print('LTV/CAC is: ', ltv/cac)

"""LTV/CAC ratio is less than 1 so that TechStream seems to be spending more to acquire customers than it earns from them over their lifetime. This could indicate an unsustainable business model."""