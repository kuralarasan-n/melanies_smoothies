# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(f"""Choose the fruits you want in your custom Smoothie!""")

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favourite fruit is:", option)

# import streamlit as st

name_on_order = st.text_input('Name on Smoothie')
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect('choose up to 5 ingredient: ', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    # st.write (ingredients_string)
    my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
    ORDER_UID = session.sql(order_seq).collect()
    st.text('order_uid')
    my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_UID")==0).collect()

    my_insert_stmt = """insert into smoothies.public.orders
            values ('"""+order_uid+"""','"""+order_filled+"""','""" +ingredients_string+ """', '"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button ('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")




