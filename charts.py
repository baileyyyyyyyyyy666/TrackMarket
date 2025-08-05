# Main plotting library
import plotly.graph_objects as go
# Web interface library
import streamlit as st


class ChartCreator:

    # Create chart for crypto prices
    def create_crypto_chart(self, crypto_data):
        if crypto_data.empty:
            return go.Figure()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=crypto_data['name'],
            y=crypto_data['price'],
            text=[f"${price:.2f}" for price in crypto_data['price']],
            textposition='auto',
            marker_color=[
                'green' if change >= 0 else 'red'
                for change in crypto_data['change']
            ],
            name='Cryptocurrency Prices'
        ))
        fig.update_layout(
            title="Live Cryptocurrency Prices",
            xaxis_title="Cryptocurrency",
            yaxis_title="Price (USD)",
            height=400,
            template="plotly_dark"
        )
        return fig

    # Create summary info about our data
    def create_summary_metrics(self, crypto_data):
        if not crypto_data.empty:
            avg_change = crypto_data['change'].mean()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="Cryptocurrencies Tracked",
                    value=len(crypto_data),
                    delta=None
                )
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
