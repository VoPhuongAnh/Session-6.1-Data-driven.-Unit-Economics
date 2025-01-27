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

* Total sales amount: collected by summing total receipt amounts from amount in receipt history file. Result is 83033.
* Total salary paid for Sales: collected from payroll file. Result is 5950.
* Total monthly expense for marketing software costs: collected from monthly expense file. Result is 1700.
* Total cost for online ads: collected from daily marketing spending file. Result is 68830


Total sales and marketing expense we calculated is 159513. [1]

##### Codes:

```
# Total sales:
total_sales = df_receipt_history_data.receipt_amount.sum()

# Total payroll of Sales and Marketing team:
sale_salary = df_payroll_data[df_payroll_data["department"].isin(['Sales','Marketing'])]["paid"].sum()

# Total expense for marketing sofware: monthly expense (item=saleforce, )
mkt_software_cost = df_monthly_expense_data[df_monthly_expense_data["item"] == "Salesforce"]["amount"].sum()

#content creation: no need for cals since this is already included in online merketing expenses.

# Total exepnse for online ads:
online_ad_cost = df_daily_mkt_spending_data.spending.sum()

# Total expense relating to sales and marketing activities:
total_sale_mkt_espenses = total_sales + sale_salary + mkt_software_cost + online_ad_cost
```

1.2 - Number of new customers acquired:

We collect number of new customer TechStream acquired from the receipt history file, but not the Churn data due to the fear of mising out such new customer who is not yet been remarked as churn.
We will filter the column new_customer  in "recceipt history file"  (New customers are remarked as 1), and then count the total of them. Number of new customers acquired is 63. [2] 

##### Codes:

```
# number of new customer acquired: (không lấy trong bảng churn date vì sẽ bị miss data của những khách hàng chưa là churn)

new_cust_count = df_receipt_history_data[df_receipt_history_data["new_customer"] == 1].new_customer.count()

#len(df_receipt_history_data[df_receipt_history_data["new_customer"] == 1]["customer_id"].unique())
```

From the [1] and [2], CAC is 2531.9523809523807 or TechStream need to spend around $2,532 in March 2023 to acquire a new customer.

#### 2. ARPU: Average Revenue Per User 

2.1 - Total revenue is 83033, which is the summed amount collected from receipt history file. [3]

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
#### 4. Gross Margin
#### 5. LTV
#### 6. LTV / CAC

## Findings Summary:

From the data collected during March 2023, the company need approximatly $2,532 to get a new customer. In this period, they already acquired 63 new customers (churn ones inclusive).
