import streamlit as st
import plotly.express as px
import backend

st.title("Weather forecast for the next days")

place = st.text_input("Place: ")
days = st.slider("Forecast days", min_value=1, max_value=3, help="Select the number of days to forecast, maximum 3 days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))

# Creating a intelligent subhead text

if days == 1:
    sub_head = f"{option} for the current day in {place}"
elif days == 2:
    sub_head = f"{option} for today and tomorrow in {place}"
else:
    sub_head = f"{option} for {days} days from today"

st.subheader(sub_head)

if place:

    try:
        # Getting raw dates and extracting unique values and sorting them

        raw_dates = backend.get_dates_data(place=place, days=days)
        sorted_dates = sorted(set(raw_dates))

        # Passing sorted dates to get a final dates, temperatures and images list
        dates, temperatures, image_paths = backend.get_dates_temperatures_data(place=place, srtd_dates_list=sorted_dates)

        # Adding timestamp to the final dates list
        dates_timestamp = backend.add_timestamp(sorted_dates)

        # Visualizing data to the user
        if option == "Temperature":
            figure = px.line(x=dates_timestamp, y=temperatures, labels={"x": "Date", "y": "Temperature(C)"})

            st.plotly_chart(figure, use_container_width=True)

        if option == "Sky":
            st.image(image_paths, width=115)

    except KeyError:
        st.info("You entered a non-existent place, Please enter a existing place")