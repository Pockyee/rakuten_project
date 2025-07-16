# pages/6_FastAPI_demo.py
import streamlit as st
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // FastAPI Demo",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(5 / 9)
st.title("FastAPI Demonstration")

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/6_FastAPI_Demo.py")