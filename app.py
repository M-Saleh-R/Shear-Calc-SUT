import streamlit as st
import base64

# Page configuration
st.set_page_config(
    page_title="Concrete Beam Shear Capacity Calculator", 
    page_icon="🏗️", 
    layout="centered"
)

# Function to set background image and text colors
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            /* Set the background image */
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Dark semi-transparent container to make white text readable */
            .main .block-container {{
                background-color: rgba(0, 0, 0, 0.65);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            
            /* Force all text, headers, labels, and metric values to be white */
            html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, span, .stText {{
                color: white !important;
            }}
            
            /* Specifically target metric values and labels */
            [data-testid="stMetricValue"] > div {{
                color: white !important;
            }}
            [data-testid="stMetricLabel"] > div {{
                color: #e0e0e0 !important;
            }}
            
            /* FIX: Input fields styling (Dark text inside white boxes) */
            input[type="number"], div[data-baseweb="input"] input, .stNumberInput input {{
                color: #1f1f1f !important;
                background-color: #ffffff !important;
            }}
            
            /* Make the +/- buttons inside the input boxes visible */
            div[data-baseweb="input"] svg {{
                fill: #1f1f1f !important;
            }}
            
            /* FIX: Text inside st.info / st.warning / st.success boxes */
            div[data-testid="stAlert"] p, div[data-testid="stAlert"] span {{
                color: #1f1f1f !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image 'background.jpeg' not found. Please check the repository.")

# Apply background and custom CSS
set_background("background.jpeg")

# Title and Description
st.title("Shear Strength of Concrete Beams Without Stirrups")
st.markdown("""
This tool evaluates the ultimate shear capacity ($V_u$) and the critical diagonal crack distance from the support ($a_{cr}$) based on the provided empirical formulas.
""")
st.latex(r"\frac{V_u}{bd} = 21.7 \rho^{0.363} (f'_c)^{0.249} d^{-0.314} (a/d)^{-0.352}")
st.latex(r"a_{cr} = 0.521 a")

st.markdown("---")
st.subheader("Geometric & Material Parameters")

# Input parameters
col1, col2 = st.columns(2)

with col1:
    b = st.number_input("Section Width (b) - mm", min_value=10.0, value=300.0, step=10.0)
    d = st.number_input("Effective Depth (d) - mm", min_value=10.0, value=400.0, step=10.0)
    a = st.number_input("Shear Span (a) - mm", min_value=10.0, value=1000.0, step=50.0)

with col2:
    fc = st.number_input("Concrete Compressive Strength (f'c) - MPa", min_value=1.0, value=25.0, step=1.0)
    rho = st.number_input("Longitudinal Reinforcement Ratio (ρ)", min_value=0.0001, max_value=0.0500, value=0.0150, format="%.4f")

st.markdown("---")

# Calculation Block
if st.button("Calculate Results", type="primary"):
    # Calculate shear stress term (Vu / bd)
    a_over_d = a / d
    
    vu_over_bd = (21.7 
                  * (rho ** 0.363) 
                  * (fc ** 0.249) 
                  * (d ** -0.314) 
                  * (a_over_d ** -0.352))
    
    # Calculate ultimate shear force (Newtons) and convert to KiloNewtons (kN)
    vu_newtons = vu_over_bd * b * d
    vu_kn = vu_newtons / 1000.0
    
    # Calculate crack distance
    a_cr = 0.521 * a
    
    # Display Outputs
    st.subheader("Results Report:")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric(label="Ultimate Shear Capacity (Vu)", value=f"{vu_kn:.2f} kN")
    col_res2.metric(label="Crack Distance from Support (a_cr)", value=f"{a_cr:.2f} mm")
    
    # Information Box
    st.info(f"Calculated Nominal Shear Stress (Vu/bd): {vu_over_bd:.3f} MPa")
