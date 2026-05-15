# Import python packages.
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

#option = st.selectbox("What is your favorite fruit?", 
#                     ('Banana', 'Strawberries', 'Peaches')) 
#st.write(f'Your favorite fruit is {option}.')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()

# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on smoothie:")
st.write(f"The name on your Smoothie will be: {name_on_order}")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections = 5
)
if ingredients_list:
    # st.write(ingredients_list)
    for item in ingredients_list:
        st.subheader(item + ' Nutrition Information')

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == item, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {item} is {search_on}.')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    ingredients_string = " ".join(ingredients_list)
    my_insert_stmt = (
        f""" insert into smoothies.public.orders (ingredients, name_on_order)
             values ('{ingredients_string}', '{name_on_order}')"""
    )

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


