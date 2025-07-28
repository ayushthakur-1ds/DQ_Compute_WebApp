import streamlit as st

# 

st.set_page_config(page_title="DQ KPI Compilation App", layout="wide")

col_left_margin, col_content, col_right_margin = st.columns([1, 4, 1])

with col_content:
    # Welcome Heading
    st.write("") # Add some vertical space
    st.write("")
    st.markdown("<h1>WELCOME TO DQ COMPILE;</h1>", unsafe_allow_html=True) # Removed inline style as it's in CSS
    st.write("") # Add some vertical space

    # Introduction Text
    st.markdown("""
    This tool is designed to help you efficiently compile your Data Quality Key Performance Indicators
    across various timeframes: Monthly, Month-to-Date (MTD), and Quarterly.

    We're continuously enhancing the application with new features. In the meantime, you can navigate to
    the Monthly Compile section to process your monthly KPIs, or visit the Quarterly Compile section for
    your quarterly data.

    Should you encounter any problems or have any queries, please don't hesitate to contact the 1DS DQ
    Team.
    """)

    st.write("")