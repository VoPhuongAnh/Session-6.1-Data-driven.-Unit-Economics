# PRACTICE PROJECT  

## Session-6.1-Data-driven.-Unit-Economics

This project is to analysize the TechStream Solutions's unit economics to understand the profitability of their procduct called Streamline Pro on a per-customer basis.

### A - Data description and usage

Dataset is collected from TechStream Solutions through several years of operation. Dataset is mainly about their costs and revenues.
The datasets are in the shared folder on Google Drive:
https://drive.google.com/drive/folders/1qhOW9Y2orRXuzbX-kXEmuJ7TMQiRs2Uv?usp=drive_link

We collected data from 5 different excel files and try to idientify the connection among the files.

First 5 rows of Customer lifespan data:

|   | Unnamed: 0 | start_date | churn_date |
|--:|-----------:|-----------:|-----------:|
| 0 |       1000 | 2021-11-15 | 2022-09-14 |
| 1 |       1001 | 2022-04-15 | 2023-02-16 |
| 2 |       1002 | 2022-10-30 | 2023-02-04 |
| 3 |       1003 | 2021-08-22 | 2023-02-07 |
| 4 |       1004 | 2021-08-23 | 2022-02-02 |

First 5 rows of Daily Marketing spending data:

|     |       date |      channel | spending |
|----:|-----------:|-------------:|---------:|
| 236 | 2023-03-01 |   Google Ads |      449 |
| 237 | 2023-03-01 | Facebook Ads |      229 |
| 238 | 2023-03-01 | LinkedIn Ads |      835 |
| 239 | 2023-03-01 |  Twitter Ads |      986 |
| 240 | 2023-03-02 |   Google Ads |      912 |

First 5 rows of Daily expense data:

|    |  # |      month |          category |                 item | amount |
|---:|---:|-----------:|------------------:|---------------------:|-------:|
| 18 | 19 | 2023-03-01 |      Server Costs |          AWS Hosting |   8400 |
| 19 | 20 | 2023-03-01 |      Server Costs | Google Cloud Storage |   4400 |
| 20 | 21 | 2023-03-01 | Software Licenses |       Atlassian Jira |   1400 |
| 21 | 22 | 2023-03-01 | Software Licenses |                Slack |    900 |
| 22 | 23 | 2023-03-01 | Software Licenses |           Salesforce |   1700 |

First 5 rơws of Payroll data:

|    |      month | department | employee_name |          position | paid |
|---:|-----------:|-----------:|--------------:|------------------:|-----:|
| 34 | 2023-03-01 |      Sales |      John Doe |     Sales Manager | 1500 |
| 35 | 2023-03-01 |      Sales |    Jane Smith |   Sales Associate |  600 |
| 36 | 2023-03-01 |      Sales |     Jim Brown |   Sales Associate |  700 |
| 37 | 2023-03-01 |      Sales |  Laura Miller |   Sales Associate |  800 |
| 38 | 2023-03-01 |  Marketing | Alice Johnson | Marketing Manager | 1650 |


First 5 row of Receipt history head :

|     |       date | customer_id | receipt_amount | new_customer |
|----:|-----------:|------------:|---------------:|-------------:|
| 618 | 2023-03-01 |        1062 |            103 |            0 |
| 619 | 2023-03-01 |        2243 |            157 |            0 |
| 620 | 2023-03-01 |        1166 |            372 |            0 |
| 621 | 2023-03-01 |        2406 |            426 |            1 |
| 622 | 2023-03-01 |        2761 |             41 |            1 |

### B - The main goals

By doing this analysis, TechStream Solutions's aiming to :

* Identify the profitability of acquiring and retaining customers.
* Assess the efficiency of their marketing and sales strategies.
* Make informed decisions on scaling their operations and optimizing their resource allocation.
* refine their business strategies, ensure sustainable growth and maximize profitability.

### C - Results

Calculate such Unit Economics below via identifying key metrics about their operations. For some of the metrics, The calculation shall be applied for data in March 2023 only.

#### 1. CAC : CUSTOMER ACQUISITION COST

1.1 - Total sales and marketing expense include below factor:

* Total salary paid for Sales & Marketing: collected from payroll file. Result is $5,950.
* Total monthly expense for marketing software costs: collected from monthly expense file. Result is $1,700.
* Total cost for online ads: collected from daily marketing spending file. Result is $68,830


Total sales and marketing expense we calculated is $76,480. [1]

##### Codes:

```
# 1. Online ads: Daily Marketing spending --> Sum of Spending:
online_ad_cost = df_daily_mkt_spending_data.spending.sum()

# 2. Payroll of sales and mkt: 
sale_mkt_salary = df_payroll_data[df_payroll_data["department"].isin(['Sales','Marketing'])]["paid"].sum()

# 3. Marketing sofware: Daily expense --> Category (Software Licenses) --> Item (item=saleforce)
mkt_software_cost = df_monthly_expense_data[df_monthly_expense_data["item"] == "Salesforce"]["amount"].sum()

# 4.Content creation: included trong chi phí online mkt



total_sale_mkt_espenses = sale_mkt_salary + mkt_software_cost + online_ad_cost


print('Total Salary of Sales is: ', sale_mkt_salary)
print('Total Cost of marketing software is: ', mkt_software_cost)
print('Total cost of online ads is: ', online_ad_cost)
print('Total expense for sales and marketing is: ', total_sale_mkt_espenses)
```

Total Salary of Sales and Marketing is:  5950
Total Cost of marketing software is:  1700
Total cost of online ads is:  68830
Total expense for sales and marketing is:  76480

1.2 - Number of new customers acquired:

We collect number of new customer TechStream acquired from the receipt history file, but not the Churn data due to the fear of mising out such new customer who is not yet been remarked as churn.
We will filter the column new_customer  in "recceipt history file"  (New customers are remarked as 1), and then count the total of them. Number of new customers acquired is 63. [2] 

##### Codes:

```
# number of new customer acquired: (không lấy trong bảng churn date vì sẽ bị miss data của những khách hàng chưa là churn)

new_cust_count = df_receipt_history_data[df_receipt_history_data["new_customer"] == 1].new_customer.count()

#len(df_receipt_history_data[df_receipt_history_data["new_customer"] == 1]["customer_id"].unique())
```

From the [1] and [2], CAC is:  1213.968253968254 or TechStream need to spend around $1,213.97 in March 2023 to acquire a new customer.

#### 2. ARPU: Average Revenue Per User 

2.1 - Total revenue is $83,033, which is the summed amount collected from receipt history file. [3]

2.2 - Total number of users is 292, which is the total customer from receipt history file. [4]

##### Codes:

```
# total revenue : receipt amount --> sum
revenue_total = df_receipt_history_data.receipt_amount.sum()

#number of customer : receipt history --> count account unique
#num_cust = df_receipt_history_data.customer_id.unique().size
num_cust = len(df_receipt_history_data.customer_id.unique())

```
From [3] and [4], ARPU is 284.3595890410959 meaning each customer generated ~$284 in revenue on average
during March 2023.


#### 3. COGS

COGS is calculated from such cost and expense direclty and indirreclty relates to producing its services such as sever expense, software license fee for such operation service. Saleforce should not be included since it's already calculated in CAC. Labor cost for Engineering team is also a factor to be considered when we calculate COGS.

##### Codes:
```
# Expense for server and sofware license: 
server_cost = df_monthly_expense_data[df_monthly_expense_data['category'] == 'Server Costs']['amount'].sum()

software_licenses_cost = df_monthly_expense_data[df_monthly_expense_data['item'].isin(['Atlassian Jira', 'Slack', 'Zoom'])]['amount'].sum()

# Direct relating labor cost --> Salary of Engineering in Payroll data:
labor_cost = df_payroll_data[df_payroll_data['department'] == 'Engineering'].paid.sum()

# Cost of Goods Sold:
COGS = server_cost + software_licenses_cost + labor_cost

```
Total cost for Server is $12,800; cost for Software License is $2,840; Direct labor cost is $5,200.
From the calculation of these factors, we have the direct cost of producing the goods or services that TechStream sold in March 2023 is $20,840. 

#### 4. Gross Margin

##### Codes:
```
# Sales revenue --> revenue_total

# COGS:

# Gross Margin = (revenue - COGS) / Revenue * 100
gross_margin = (revenue_total - COGS) / revenue_total * 100

print('Gross margin is: ',gross_margin)

```
The Gross margin of TechStream in March 2023 is around 74.9% means that the businesss heath of this company is quite good.


#### 5. LTV

##### Codes:
```
# ARPU --> arpu (calculated above)

# avg_lifespan_months --> churn_date - start_date

df_customer_life_span_data['cust_life_span'] = df_customer_life_span_data['churn_date']- df_customer_life_span_data['start_date']
df_customer_life_span_data['cust_life_span'].mean()

# GrossMargin --> gross_margin

cust_lifespan_month = (295 + ((5 * 3600 + 45 * 60 + 36) / (24 * 60 * 60))) / 31  

ltv = arpu * cust_lifespan_month * (gross_margin /100)

print('LTV is: ', ltv)
```

LTV is:  2028.4866681396377
So, total revenue that TechStream can expect from a customer over the entire duration of their relationship is around $2,028.5


#### 6. LTV / CAC

##### Codes:
```
print('LTV/CAC is: ', ltv/cac)
```
LTV/CAC is:  1.6709552836401305
LTV/CAC ratio is greater than 1 so that TechStream seems to be spending less to acquire customers than it earns from them over their lifetime. This could indicate an sustainable business model.

## Findings Summary:

From the data collected during March 2023, 
Total revenue of TechStream is $83,033; the company needs approximatly $1,213.97 to get a new customer. In this period, they already acquired 63 new customers (churn ones inclusive) and total of 292 user in March 2023. During March 2023, each customer generated ~$284 in revenue on average. From calculation, total revenue that TechStream can expect from a customer over the entire duration of their relationship is around $2,028.5

The direct cost of producing the goods or services that TechStream sold in March 2023 is $20,840. 
The Gross margin of TechStream in March 2023 is around 74.9% and LTV/CAC ratio is curently showing that its business is still in good health and expecting a sustainable growth.

