import streamlit as st

def probability_gauge(prob: float):
    st.progress(min(max(prob, 0.0), 1.0))
    st.caption(f"Fraud probability: {prob:.2%}")