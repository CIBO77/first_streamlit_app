import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healt Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick fruit they want to include
fuits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fuits_selected]
# Display the table on the page
streamlit.dataframe(fruits_to_show)


#New section to display fruityvice api response
streamlit.header('FruityVice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
##streamlit.text(fruityvice_response.json())

#take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

streamlit.header("The fruit load list contains:")
fruit_choiceSQL = streamlit.text_input('What fruit would you like information about?', '%')
streamlit.write('The user entered', fruit_choiceSQL)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list where fruit_name = '" + fruit_choiceSQL + "'")
my_data_rows = my_cur.fetchall()

streamlit.dataframe(my_data_rows)
