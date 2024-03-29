import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
#from datetime import datetime
import datetime as dt
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pymysql  

# read csv from a github repo
#df = pd.read_csv("https://raw.githubusercontent.com/sat4git/streamlit/main/bank.csv")


st.set_page_config(
    page_title = 'My Trading Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title
st.title(f"My first trading Dashboard")
st.markdown(
"90% of people love to enjoy music, while they are working! \n  "  
"are you one of them, we have a curated list of chillout tracks \n"
"that may help you bring out the calmness in you."
)
first_col1, first_col2, first_col3 = st.columns(3)
first_col1.metric(label="Opening Balance ⏳", value=1111111, delta= 1111111*0.111111)
first_col2.metric(label="Current Balance ⏳", value=2222222, delta= 2222222-111111)
pageView = first_col3.radio(
    "Choose the page view you wish to see:",
    ('Trade_view', 'Daily_results', 'Documentary'))

my_conn = create_engine("mysql+pymysql://sql7586812:eUs4d8LNPB@sql7.freemysqlhosting.net:3306/sql7586812")

#st.write(data)
#gb = GridOptionsBuilder.from_dataframe(data)
#gb.configure_columns(list(df.columns.values), editable=True)
#gb.configure_column('virtual column a + b', valueGetter='Number(data.age)', cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])
#go = gb.build()
#grid_table = AgGrid(data, 
#            gridOptions = go, 
#            enable_enterprise_modules = True,
#            fit_columns_on_grid_load = False,
#            height=350,
#            width='100%',
#            theme = "streamlit",
#            update_mode = GridUpdateMode.SELECTION_CHANGED,
#            reload_data = True
#                   )
today = dt.date.today().strftime('%b-%d-%Y')
second_col1, second_col2, second_col3 = st.columns(3)
d = second_col2.date_input(
    "Choose your date for the trade view")
text_markdown = f"### {today}"          
second_col1.metric(label="Today\'s Date is:", value=today)
# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

#df = df[df['job']==job_filter]
def color_Profit(val):
    color = '#00FA9A' if val>0 else '#FF6347'
    return f'background-color: {color}'

# near real-time / live feed simulation 

#for seconds in range(200):
if pageView == 'Trade_view':
    while True: 

        #df['age_new'] = df['age'] * np.random.choice(range(1,5))
        #df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

        # creating KPIs 
        #avg_age = np.mean(df['age_new']) 

        #count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))

        #balance = np.mean(df['balance_new'])

        with placeholder.container():
            # create three columns
            #kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs 
            #kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
            #kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
            #kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

            text1 = f"### Detailed TradeBook View for {d}"
            st.markdown(text1)
            sql = f"select id, Date, Time, Bitcoin_EUR, CryptoCoin, Quantity, BuyPrice, SellPrice, Profit_Loss_percentage, Bitcoin_diff, Profit_after_fees from TradeBook WHERE DATE(Date) = '{d}'"
            data = pd.read_sql(sql,con=my_conn)
            if len(data)>0:
                data['Time'] = data['Time'].astype("str")
                st.dataframe(data.style.applymap(color_Profit, subset=['Profit_Loss_percentage','Bitcoin_diff','Profit_after_fees']))
                # create two columns for charts 

                #fig_col1, fig_col2 = st.columns(2)
                #fig_col1 = st.empty()
                #with fig_col1.container():
                st.markdown("### First Chart")
                fig = px.bar(data, x=data["id"].astype("str")+"_"+data["CryptoCoin"], y="Profit_Loss_percentage",
                             color=['red' if i<0 else 'green' for i in data['Profit_Loss_percentage']], color_discrete_map="identity",
                             category_orders={"x": data["id"].astype("str")+"_"+data["CryptoCoin"]}
                            )
                #['red' if i>0 else 'green' for i in data['Profit_Loss_percentage'].astype("float")]
                st.plotly_chart(fig,use_container_width=True)
                #with fig_col2:
                #    st.markdown("### Second Chart")
                #    fig2 = px.histogram(data_frame = df, x = 'age_new')
                #    st.write(fig2)
            else:
                st.subheader("There are no records for this date. Please choose another date")
            
            time.sleep(10)
            
elif pageView == 'Daily_results':
    with placeholder.container():
        st.markdown("### Daily View")
        sql_daily = "select * from DailyBook"
        data_daily = pd.read_sql(sql_daily,con=my_conn)
        data_daily['Time'] = data_daily['Time'].astype("str")
        st.dataframe(data_daily.style.applymap(color_Profit, subset=['BTC_TotalVale','BTC_BNB_Diff']))
else:
    st.markdown("### Currently work in progress please select either of the first 2 options. Thank you")
    #placeholder.empty()


