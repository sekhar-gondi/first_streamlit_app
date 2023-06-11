import streamlit
import pandas
import requests
#requirements.txt
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled & Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick up some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

#Creating function for repeatable code
def get_fruityvice_data(this_fruit_choice):
  #streamlit.write('The user entered', fruit_choice) #displaying what user asked for
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) 
  #streamlit.text(fruityvice_response.json()) #just writes data to screen but not in proper format
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #this will normalize the json output
  return fruityvice_normalized
  

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?') #asking user to input fruit name
  if not fruit_choice:
       streamlit.error("Please select fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #now print the normalized json output
    streamlit.dataframe(back_from_function) #dataframe shows in tabular format
      
except URLError as e:
   streamlit.error()


  
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone() #this will fetch only one record
streamlit.text("Hello from Snowflake:")
#streamlit.text("The Fruit Load List Contains:")

streamlit.header("The Fruit Load List contains:") #streamlit.text(my_data_row)
#snowflake related functions:
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#add button to load fruit
if streamlit.button('Get Fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

#streamlit.stop()

def insert_row_into_SF(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('from streamlit')")
    return 'Thanks for adding new fruit:' + new_fruit

add_my_fruit = streamlit.text_input('What Fruit would you like to add?')  
#add button for new fruit
if streamlit.button('Add new fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_into_SF(add_my_fruit)
  streamlit.text(back_from_function)



