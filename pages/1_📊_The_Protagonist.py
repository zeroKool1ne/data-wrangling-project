import streamlit as st                                                          
import pandas as pd
import numpy as np
import plotly.graph_objects as go                                               
from scipy import stats
from utils.styles import apply_styles, divider
                                                                                  
# --- Page Config ---
apply_styles()
                                                                                  
# --- Load Data (cached to avoid reloading on every interaction) ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/saas_sales_clean.csv")                       
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df                                                                   
                  
df = load_data()

                                                                                  
# --- Page Header ---
st.markdown(   
    "<h1 style='text-align: center;'>"                                                                              
    "<i class='bi bi-person-circle' style='margin-right: 10px;'></i>"                                               
    "The Protagonist</h1>",                                                                                         
    unsafe_allow_html=True                                                                                          
  )            
                                                  
st.markdown( 
    "<p style='font-size: 1.05rem; font-weight: bold;  color: #555; text-align: center;'>"                                                                     
    "Who is the typical AWS SaaS customer?</p>",                                                                    
      unsafe_allow_html=True
  )       
st.markdown(                                                                                                    
    "Before we ask *why* some regions bleed money, we need to establish a baseline: "                               
    "**who is the typical AWS SaaS customer?** "                                                                    
    "Using **95% confidence intervals** on {:,} transactions, we estimate the true "                                
    "population parameters — not just what we see in the data, but what is likely true "                            
    "for all AWS SaaS customers globally.".format(len(df))                                                          
)                                                                                                                   
st.markdown(                                                                                                        
    "Two things stand out immediately: the **profit CI is wide** ($24–$33), signalling "                            
    "high variance in profitability across transactions. Yet the **discount CI is "                                 
    "remarkably narrow** (15–16%), meaning discounts are applied in fixed, consistent "                             
    "steps. A 12% profit margin is also far below the SaaS industry benchmark of "                                  
    "60–80% — something is eating into margins."                                                                    
)                                                                               
                  
divider()                                                                    
                  
                                                                                  
# --- Calculate Confidence Intervals ---
def calc_ci(data, confidence=0.95):
    """Calculate mean and 95% confidence interval."""
    n = len(data)                                                               
    mean = data.mean()
    se = stats.sem(data)                                                        
    ci = stats.t.interval(confidence, df=n-1, loc=mean, scale=se)
    return mean, ci[0], ci[1]                                                   
   
                                                                                  
# Define which metrics to estimate
metrics = {
    "Sales per Transaction": df["Sales"],
    "Averge Profit per Transaction": df["Profit"],                                     
    "Profit Margin (%)": df["Profit Margin"],
    "Discount Rate (%)": df["Discount"] * 100       # convert decimal to %                                 
}                                                                               
   
# Calculate all CIs                                                             
ci_results = {} 
for name, data in metrics.items():
    mean, lower, upper = calc_ci(data.dropna())                                 
    ci_results[name] = {"mean": mean, "lower": lower, "upper": upper}
                                                                                  
                  
# --- Metric Cards Row ---                                                      
cols = st.columns(4)
for i, (name, vals) in enumerate(ci_results.items()):
    with cols[i]:
        # Format based on metric type                                           
        if "%" in name:
            display = f"{vals['mean']:.1f}%"                                    
            ci_text = f"95% CI: [{vals['lower']:.1f}%, {vals['upper']:.1f}%]"   
        else:                                                                   
            display = f"${vals['mean']:,.2f}"                                   
            ci_text = f"95% CI: [${vals['lower']:,.2f}, ${vals['upper']:,.2f}]" 
        st.metric(name, display)                                                
        st.caption(ci_text)
                                                                                  
divider()    

                                                                                  
# --- Forest Plot: visual overview of all CIs ---
st.markdown("<h3 style='text-align: center;'>Confidence Interval Overview</h3>", unsafe_allow_html=True)                                 
st.markdown(                                                                    
    "Each bar shows the **point estimate** (mean) with error bars "
    "representing the **95% confidence interval**. Narrower intervals "         
    "= more precise estimates."                                                 
)                                                                               
                                                                                  
# Build the forest plot
fig = go.Figure()

# Pastel palette — no bright/neon colors                                                          
colors = ["#a8d5e2", "#f9b4ab", "#fae3b0", "#b5ead7"]
                                                                                  
for i, (name, vals) in enumerate(ci_results.items()):
    fig.add_trace(go.Bar(                                                       
        x=[vals["mean"]],
        y=[name],                                                               
        orientation="h",
        marker_color=colors[i],                                                                                             
        marker_line_color="#ccc",                                                                                           
        marker_line_width=1,                                                  
        error_x=dict(
            type="data",                                                        
            symmetric=False,
            array=[vals["upper"] - vals["mean"]],                               
            arrayminus=[vals["mean"] - vals["lower"]],
            color="#666",                                                       
            thickness=2,
            width=6                                                             
        ),      
        hovertemplate=(                                                         
            "<b>%{y}</b><br>"
            "Mean: %{x:.2f}<br>"
            f"95% CI: [{vals['lower']:.2f}, {vals['upper']:.2f}]"               
            "<extra></extra>"       # Removes default tooltip box
        ),                                                                      
        showlegend=False                                                        
))
                                                                                  
fig.update_layout(
    height=300,
    margin=dict(l=0, r=40, t=20, b=20),
    xaxis_title="Value",                                                        
    yaxis=dict(autorange="reversed"),
    plot_bgcolor="rgba(0,0,0,0)",       # Transparent bg to blend with Streamlit                                             
    paper_bgcolor="rgba(0,0,0,0)",                                              
    font=dict(size=14)
)                                                                               
                  
st.plotly_chart(fig, use_container_width=True)                                  
   
                                                                                  
# --- Interpretation ---
divider()
st.markdown("### What does this tell us?")

col1, col2 = st.columns(2)                                                      
   
with col1:                                                                      
    st.markdown(
        """
        **The typical AWS SaaS transaction:**
        - Generates **~\$230 in sales** and **~\$29 in profit**                   
        - Has a profit margin of **~12%**                                       
        - Includes a discount of **~16%**                                       
        """                                                                     
    )                                                                           
   
with col2:                                                                      
    st.markdown(
        """
        **Key observation:**
        - The profit CI is wide → high variance in profitability
        - The discount CI is narrow → discounts are applied consistently        
        - This raises a question: **are discounts eating into profit?**
        """                                                                     
    )           
                                                                                  
st.info(                                                                                                            
      "These estimates set the baseline. "                                                                            
      "Next, we test 5 hypotheses to find out what drives profitability.",                                            
      icon=":material/arrow_forward:"                                                                                 
)                                                                             
                          