import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Setting up a list here so the user can select any fruits from the lists
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Displaying selected fruits_to_show on the page
streamlit.dataframe(fruits_to_show)

# Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

#New Section to display Fruityvice API response
# import requests
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

#Stop anything beyond this wile we troubleshoot
streamlit.stop()

#connecting with snowflake.
# import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["Snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list;")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Allow the end user to add a fruit to the list
add_my_fruit =streamlit.text_input("What fruits would ypu like to add?: ")
if len(add_my_fruit) != 0:
  my_cur.execute(f"Insert into PC_RIVERY_DB.PUBLIC.fruit_load_list (fruit_name) values ('{add_my_fruit}');")

# Display the table on the page
#streamlit.dataframe(my_fruit_list)
