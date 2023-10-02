import streamlit as st

st.title("Bangalore House Price Prediction")
st.markdown("This app predicts the **Bangalore House Price**!")

area = st.number_input("Area in sqft", min_value=100, max_value=10000, value=2000)
print(area)