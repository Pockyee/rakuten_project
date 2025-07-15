# pages/6_FastAPI_demo.py
import streamlit as st
import requests
import os
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // FastAPI Demo",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(5 / 9)
st.title("FastAPI Demonstration")

# Get FastAPI URL from environment or default to localhost
FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000')

st.markdown(f"""
### Live FastAPI Integration
Connected to: `{FASTAPI_URL}`

This page demonstrates real-time interaction with our ML prediction API.
""")

# Create two columns for the demo
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔮 Product Prediction")
    
    # Input form
    with st.form("prediction_form"):
        title = st.text_input(
            "Product Title (French)", 
            value="Nintendo Switch",
            help="Enter the product title in French"
        )
        
        description = st.text_area(
            "Product Description (French)", 
            value="console de jeux portable avec écran tactile",
            help="Enter the product description in French"
        )
        
        submitted = st.form_submit_button("🚀 Get Prediction")
    
    if submitted and (title or description):
        with st.spinner("Making prediction..."):
            try:
                # Call FastAPI endpoint
                response = requests.post(
                    f"{FASTAPI_URL}/predict/",
                    json={
                        "title": title,
                        "description": description
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result["predictions"][0]
                    
                    st.success("✅ Prediction successful!")
                    
                    # Display main prediction
                    st.metric(
                        "📦 Predicted Category",
                        prediction["category"],
                        f"{prediction['confidence']:.1%} confidence"
                    )
                    
                    # Display top 3 predictions
                    if len(prediction["top_3"]) > 1:
                        st.subheader("🎯 Top 3 Predictions")
                        for i, pred in enumerate(prediction["top_3"], 1):
                            st.write(f"{i}. **{pred['category']}** ({pred['confidence']:.1%})")
                    
                else:
                    st.error(f"❌ Prediction failed: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI service. Is it running?")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The service may be busy.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("📊 API Status")
    
    # Check API health
    try:
        health_response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API is healthy")
            
            # Display service info
            for service, status in health_data.get("services", {}).items():
                st.write(f"**{service}**: `{status}`")
                
        else:
            st.warning(f"⚠️ API health check returned {health_response.status_code}")
            
    except Exception as e:
        st.error("❌ API health check failed")
        st.code(str(e))
    
    st.subheader("🧪 Example Products")
    
    example_products = [
        {
            "title": "iPhone 13",
            "description": "smartphone avec écran OLED et appareil photo avancé",
            "expected": "Electronics"
        },
        {
            "title": "Livre Harry Potter",
            "description": "livre de fantasy pour enfants et adolescents",
            "expected": "Books"
        },
        {
            "title": "Ballon de football",
            "description": "ballon de sport en cuir synthétique",
            "expected": "Sports"
        }
    ]
    
    for i, product in enumerate(example_products):
        if st.button(f"Try: {product['title']}", key=f"example_{i}"):
            st.session_state.example_title = product['title']
            st.session_state.example_description = product['description']
            st.rerun()

# API Documentation section
st.markdown("---")
st.subheader("📚 API Documentation")

col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("""
    **Available Endpoints:**
    - `GET /health` - API health check
    - `POST /predict/` - Product classification
    - `GET /models/` - List available models
    - `POST /training/` - Trigger model training
    """)

with col4:
    st.markdown("""
    **Request Format:**
    ```json
    {
        "title": "Product title",
        "description": "Product description"
    }
    ```
    """)

# Interactive API explorer
st.subheader("🔍 API Explorer")

endpoint = st.selectbox(
    "Choose endpoint to test:",
    ["/health", "/models/", "/predict/"]
)

if st.button("🌐 Test Endpoint"):
    try:
        if endpoint == "/health":
            response = requests.get(f"{FASTAPI_URL}{endpoint}")
        elif endpoint == "/models/":
            response = requests.get(f"{FASTAPI_URL}{endpoint}")
        elif endpoint == "/predict/":
            response = requests.post(
                f"{FASTAPI_URL}{endpoint}",
                json={"title": "Test", "description": "test product"}
            )
        
        st.code(f"Status: {response.status_code}")
        st.json(response.json())
        
    except Exception as e:
        st.error(f"Request failed: {str(e)}")

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/6_FastAPI_Demo.py")