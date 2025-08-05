import streamlit as st
import time
import data_source
from data_source import DataSource
from charts import ChartCreator

# Define constants
UPDATE_INTERVAL_MIN = 5
UPDATE_INTERVAL_MAX = 30
DEFAULT_UPDATE_INTERVAL = 10

def main():
    # Create containers for content (these will update automatically)
    status_container = st.empty()
    crypto_container = st.empty()
    weather_container = st.empty()

    chart_creator = ChartCreator()  # Create an instance of the ChartCreator class

    # Initialize main loop variables
    update_count = 0
    refresh_interval = DEFAULT_UPDATE_INTERVAL

    while True:
        try:
            # Get cryptocurrency and weather data
            crypto_data = data_source.get_crypto_prices()
            weather_data = data_source.get_weather()

            # Update display containers
            with status_container.container():
                st.subheader("Status Messages")
                st.write(f"Got new cryptocurrency prices!")

            with crypto_container.container():
                chart = chart_creator.create_crypto_chart(crypto_data)  # Use the instance to call the method
                st.plotly_chart(chart)

            with weather_container.container():
                chart_creator.create_weather_display(weather_data)  # Use the instance to call the method

            # Update summary metrics
            if not crypto_data.empty:
                avg_change = crypto_data['change'].mean()
                col1, col2, col3 = st.columns(3)
                with col1:
                    label="Cryptocurrencies Tracked",
                    value=len(crypto_data),
                    delta=None
                with col2:
                    st.metric(
                        label="Average 24 hour change",
                        value=f"{avg_change:.2f}%",
                        delta=f"{avg_change:.2f}%"
                    )
                with col3:
                    current_time = crypto_data['time'].iloc[0]
                    st.metric(
                        label="Last Update",
                        value=current_time.strftime("%H:%M:%S"),
                    )

            # Show update info
            st.markdown(f"**Total Updates:** {update_count}")
            st.markdown(f"**Next Update In:** {refresh_interval} seconds.")
        except Exception as e:
            # Handle any exceptions that occur during updates
            with status_container.container():
                st.error(f"Error updating data: {e}")

        # Wait before next update
        time.sleep(refresh_interval)