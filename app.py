import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data_source import DataSource
from charts import ChartCreator

# Define constants
UPDATE_INTERVAL_SEC = 10  # seconds

def main():
    # Auto-refresh the app every UPDATE_INTERVAL_SEC seconds
    st_autorefresh(interval=UPDATE_INTERVAL_SEC * 1000, key="refresh")

    st.title("TrackMarket Dashboard")

    status_container = st.empty()
    crypto_container = st.empty()
    summary_container = st.empty()

    chart_creator = ChartCreator()
    data_source = DataSource()

    try:
        # Get cryptocurrency data
        crypto_data = data_source.get_crypto_prices()

        # Update display containers
        with status_container.container():
            st.subheader("Status Messages")
            st.write("Got new cryptocurrency prices!")

        with crypto_container.container():
            chart = chart_creator.create_crypto_chart(crypto_data)
            st.plotly_chart(chart)

        with summary_container.container():
            chart_creator.create_summary_metrics(crypto_data)

    except Exception as e:
        with status_container.container():
            st.error(f"Error updating data: {e}")

if __name__ == "__main__":
    main()
    