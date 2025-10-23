import streamlit as st
from datetime import datetime

# Streamlit App Title
st.set_page_config(page_title="Simple Streamlit App", layout="centered")

st.title("Simple Calculator App")
st.write("This is a basic Python web app for CI/CD demo using **Git**, **Docker**, **Jenkins**, and **Kubernetes**.")

# Input Section
st.header("Add Two Numbers")
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

if st.button("Calculate Sum"):
    result = num1 + num2
    st.success(f"The sum of {num1} and {num2} is **{result}**")

# Health Check Info (useful for Kubernetes readiness probes)
st.markdown("---")
st.caption(f"🟢 App running. Last checked at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

