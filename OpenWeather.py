import os
import requests
import streamlit as st
from dotenv import load_dotenv
import streamlit as st
import pathlib


# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)



def make_request(url, params=None):
    answer = requests.get(url, params=params)
    try:
        answer.raise_for_status()
    except requests.HTTPError as e:
        print(f"request fail: {e}")
        result = None
    else:
        result = answer.json()
    return result

def get_time_by_local(local):
    load_dotenv()
    token = os.environ['OPENWEATHER_API_KEY']

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'appid': token,
        'q': local,
        'units': 'imperial',
    }

    weather_data = make_request(url=url, params=params)
    return weather_data

def main():
    st.title("⛅ OpenWeather Web App ")
    st.write("Integrated with the OpenWeather API to display real-time \n temperature, humidity, feels-like, and cloud coverage for any location.")

    st.code("                 <>   S3ARCH FOR ANY CITY IN THE W0RLD   <>", language="bash")
    st.divider()

    st.button("-> this project was developed by <Pedro Motta> , access my github to see the code", key="grey")

    st.link_button("🔗 Acess                                        the : Github repository link","https://github.com/pedromottadev/OpenWeather_api_project"  ) 

    st.link_button("🔗 Acess the :  OpenWeather API doc","https://openweathermap.org/api")


    local = st.text_input("Search some city:", key="styledinput")
    if not local:
        st.stop()

    weather_data = get_time_by_local(local=local)
    if not weather_data:
        st.warning(f"information not found for the city : {local}")
        st.stop()
    current_weather = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    thermal_sensation = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    cloud = weather_data['clouds']['all']

    st.metric(label='Current weather',value=current_weather)

    col1,col2 = st.columns(2)
    with col1:
        st.metric(label='temperature', value=f'{temperature}°F')
        st.metric(label='Feels like', value=f'{thermal_sensation}°F')

    with col2:
       st.metric(label='humidity', value = f'{humidity}%')
       st.metric(label='cloud', value = f'{cloud}%')

if __name__ == '__main__':
    main()