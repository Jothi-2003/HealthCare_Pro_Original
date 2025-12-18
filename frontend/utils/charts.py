import streamlit as st

def probability_gauge(prob: float):
    """
    Display a probability gauge for fraud detection.

    Args:
        prob (float): Probability between 0 and 1.
    """
    # Clamp probability safely between 0 and 1
    prob = min(max(prob, 0.0), 1.0)

    # Progress bar
    st.progress(prob)

    # Color-coded caption
    if prob >= 0.75:
        st.error(f"🚨 High fraud risk: {prob:.2%}")
    elif prob >= 0.5:
        st.warning(f"⚠️ Moderate fraud risk: {prob:.2%}")
    else:
        st.success(f"✅ Low fraud risk: {prob:.2%}")