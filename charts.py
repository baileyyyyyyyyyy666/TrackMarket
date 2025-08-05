# Main plotting library
import plotly.graph_objects as go
# Web interface library
import streamlit as st


class ChartCreator:

    # Create chart for crypto prices
    def create_crypto_chart(self, crypto_data):
        # Check if data to display is there
        if crypto_data.empty:
            # Return empty chart
            return go.Figure()
        # Create new figure
        fig = go.Figure()

        # Add bars to our chart
        fig.add_trace(go.Bar(
            x=crypto_data['name'], # X axis is crypto names
            y=crypto_data['price'], # Y axis is prices
            text=[f"${price:.2f}" for price in crypto_data['price']], # Text on bars
            textposition='auto', # Automatically position text
            marker_color=[
                'green' if change >= 0 else 'red'
                for change in crypto_data['change']
            ], # Green for positive, red for negative changes
            name='Cryptocurrency Prices' # Legend name
        ))

        # Customize chart appearance
        fig.update_layout(
            title="Live Cryptocurrency Prices", # Chart title
            xaxis_title="Cryptocurrency", # X axis label
            yaxis_title="Price (USD)", # Y axis label
            height=400, # Chart height in pixels
            template="plotly_dark" # Color theme
        )

        return fig

    # Create weather info display
    def create_weather_display(self, weather_data):
        # Create columns for different weather metrics
        col1, col2, col3 = st.columns(3)

        # Display temperature
        with col1:
            st.metric(
                label="Temperature", # What we're showing
                value=f"{weather_data['temperature']}""F", # Current value
                delta=None # No change indicator for now
            )

        # Display humidity
        with col2:
            st.metric(
                label="Humidity",
                value=f"{weather_data['humidity']}%",
                delta=None
            )

        # Display city and description
        with col3:
            st.write(f"City: {weather_data['city']}")
            st.write(f"Weather: {weather_data['description']}")

    # Create summary info ab our data
    def create_summary_metrics(self, crypto_data):
        if not crypto_data.empty:
            # Calculate average change
            avg_change = crypto_data['change'].mean()

            # Display summary metrics
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