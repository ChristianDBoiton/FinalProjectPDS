#!/usr/bin/env python
# coding: utf-8

# ### Imports

# In[1]:


import yfinance as yf 
import pandas as pd
import requests
from bs4 import BeautifulSoup


# # Question 1

# In[2]:


Tesla = yf.Ticker("TSLA")
Tesla_data = Tesla.history(period="max")
Tesla_data.reset_index(inplace=True)
Tesla_data.head()


# # Question 2

# In[66]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"


# In[67]:


html_data = requests.get(url).text
soup = BeautifulSoup(html_data,"html5lib")


# In[68]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
Tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        Tesla_revenue = Tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[69]:


print(tesla_revenue.tail())


# # Question 3

# In[70]:


gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()


# # Question 4

# In[71]:


url2 = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue usando la biblioteca requests"


# In[72]:


response = requests.get(url2)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find_all('table')[1]
gamestop_revenue = pd.read_html(str(table))[0]


# In[73]:


gme_revenue.tail()


# # Question 5

# In[74]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[75]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[78]:


make_graph(Tesla_data, Tesla_revenue, 'Tesla')


# # Question 6

# In[77]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




