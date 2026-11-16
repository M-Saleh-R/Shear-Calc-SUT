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
                font-size: 1.5rem !important;
            }}
            [data-testid="stMetricLabel"] > div {{
                color: #e0e0e0 !important;
                font-size: 1rem !important;
            }}
            
            /* Input fields styling (Dark text inside white boxes) */
            input[type="number"], div[data-baseweb="input"] input, .stNumberInput input {{
                color: #1f1f1f !important;
                background-color: #ffffff !important;
            }}
            
            /* Make the +/- buttons inside the input boxes visible */
            div[data-baseweb="input"] svg {{
                fill: #1f1f1f !important;
            }}
            
            /* Text inside st.info / st.warning / st.success boxes */
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
This advanced tool evaluates the ultimate shear capacity ($V_{pred}$), the calibrated design shear capacity ($V_{design}$), and the critical diagonal crack distance ($a_{cr}$) incorporating regime-dependent conformal safety factors.
""")

st.latex(r"\frac{V_{pred}}{bd} = 21.7 \rho^{0.363} (f'_c)^{0.249} d^{-0.314} (a/d)^{-0.352}")
st.latex(r"V_{design} = \gamma_{95} V_{pred}")
st.latex(r"a_{cr} \approx 0.504 a \quad \text{(90\% Interval: } 0.38a - 0.66a \text{)}")

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
    # 1. Shear Strength Calculation
    a_over_d = a / d
    
    vu_over_bd = (21.7 
                  * (rho ** 0.363) 
                  * (fc ** 0.249) 
                  * (d ** -0.314) 
                  * (a_over_d ** -0.352))
    
    # Calculate predicted ultimate shear force (kN)
    v_pred_kn = (vu_over_bd * b * d) / 1000.0
    
    # 2. Regime-Dependent Safety Factor Calibration ('min adj' rule)
    class_factors = []
    
    # Compressive strength classes
    if fc <= 45:
        class_factors.append(0.829)
    elif fc <= 70:
        class_factors.append(0.725)
    else:
        class_factors.append(0.754)
        
    # Effective depth classes
    if d <= 300:
        class_factors.append(0.816)
    elif d <= 600:
        class_factors.append(0.835)
    else:
        class_factors.append(0.643)
        
    # Section width classes
    if b <= 300:
        class_factors.append(0.821)
    else:
        class_factors.append(0.736)
        
    # The governing safety factor is the minimum of the applicable class factors
    gamma_95 = min(class_factors)
    
    # Calculate design capacity
    v_design_kn = gamma_95 * v_pred_kn
    
    # 3. Crack Distance Calculation (Geometric Mean & 90% Prediction Interval)
    a_cr_mean = 0.504 * a
    a_cr_lower = 0.38 * a
    a_cr_upper = 0.66 * a
    
    # Display Outputs
    st.subheader("Structural Assessment Report:")
    
    # Row 1: Shear Capacities
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric(label="Predicted Capacity (V_pred)", value=f"{v_pred_kn:.2f} kN")
    col_res2.metric(label="Safety Factor (γ_95)", value=f"{gamma_95:.3f}")
    col_res3.metric(label="Design Capacity (V_design)", value=f"{v_design_kn:.2f} kN")
    
    # Row 2: Crack Distance
    st.markdown("<br>", unsafe_allow_html=True)
    col_res4, col_res5 = st.columns(2)
    col_res4.metric(label="Critical Crack Distance (a_cr)", value=f"{a_cr_mean:.2f} mm")
    col_res5.metric(label="90% Conformal Interval", value=f"[{a_cr_lower:.0f} - {a_cr_upper:.0f}] mm")
    
    # Information Box
    st.info(f"Nominal Shear Stress (v): {vu_over_bd:.3f} MPa | Governing Regime Factor Applied based on 'min adj' rule.")
