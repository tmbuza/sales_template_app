# @Email:  info@complexdatainsights.com
# @Website:  https://complexdatainsights.com
# @Project:  Interactive Dashboard w/ Streamlit

# !pip install pandas openpyxl
# !pip install plotly-express
# !pip install streamlit
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", 
                   page_icon=":bar_chart:", 
                   layout="wide")



# ---- STYLE ----
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# DATA PREPARATION

@st.cache
def get_data_from_excel():
  df = pd.read_excel(
      io="data/supermarkt_sales.xlsx",
      engine="openpyxl",
      sheet_name="Sales",
      skiprows=3,
      usecols="B:R",
      nrows=1000,
  )
  # Add 'hour' column to dataframe
  df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
  return df

with st.container():
  st.title("Sales EDA App")

  st.header("Data Structure!")
  df = get_data_from_excel()
  st.dataframe(df.head())
  st.write("---")
  
# ---- SIDEBAR ----
st.sidebar.header("User Input Widget:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

branch = st.sidebar.multiselect(
    "Select the Branch:",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)


payment = st.sidebar.multiselect(
    "Select the Payment:",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Branch == @branch & Payment == @payment"
)

# TOP KEY PERFORMANCE INDICATORS (KPIs)
with st.container():
  st.header(":bar_chart: Key Performance Indicators (KPIs)")
  st.write("##")
  
  total_sales = int(df_selection["Total"].sum())
  average_rating = round(df_selection["Rating"].mean(), 1)
  star_rating = ":star:" * int(round(average_rating, 0))
  average_sale_by_transaction = round(df_selection["Total"].mean(), 2)
  
  left_column, middle_column, right_column = st.columns(3)
  with left_column:
      st.subheader("1\. Total Sales:")
      st.subheader(f"US $ {total_sales:,}")
  with middle_column:
      st.subheader("2\. Average Rating:")
      st.subheader(f"{average_rating} {star_rating}")
  with right_column:
      st.subheader("3\. Average Sales Per Transaction:")
      st.subheader(f"US $ {average_sale_by_transaction}")
  
  st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
  sales_by_product_line,
  x="Total",
  y=sales_by_product_line.index,
  orientation="h",
  title="<b>Sales by Product Line</b>",
  color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
  template="plotly_white",
)

fig_product_sales.update_layout(
  plot_bgcolor="rgba(0,0,0,0)",
  xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
  sales_by_hour,
  x=sales_by_hour.index,
  y="Total",
  title="<b>Sales by hour</b>",
  color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
  template="plotly_white",
)
fig_hourly_sales.update_layout(
  xaxis=dict(tickmode="linear"),
  plot_bgcolor="rgba(0,0,0,0)",
  yaxis=(dict(showgrid=False)),
)

# PLOTING
text_column,left_column, right_column = st.columns((1,2, 2))
with text_column:
  st.markdown("""
  Add description here. Introduce what this app does and how incredibly it can help in exploring the sales data features interactively. Enjoy :tada:
  """)
left_column.plotly_chart(
  fig_hourly_sales, 
  use_container_width=True)
right_column.plotly_chart(
  fig_product_sales, 
  use_container_width=True)

##################################
# CONTACT FORM 
#(from: https://formsubmit.co/)
##################################
with st.container():
  st.write("---")
  st.header("Get In Touch")
  st.write("Please feel free to fill out the form below and let\'s get intouch!")
  
  contact_form = """
  <form action="https://formsubmit.co/ndelly@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="email" name="email" placeholder="Your email" required>
    <textarea name="message" placeholder="Your message here" required></textarea>
    <button type="submit">Send</button>
  </form>
  """
  
  left_column, right_column = st.columns(2)
  with left_column:
    st.markdown(contact_form, unsafe_allow_html=True)
  with right_column:
    st.image("https://complexdatainsights.com/wp-content/uploads/2020/09/contactNewk.png") # or st.empty()

##################################
# st.balloons()
##################################
