import streamlit as st                                                
import pandas as pd                                                                                                 
from utils.styles import apply_styles, divider

# --- Page Config ---
apply_styles()

# --- Load Data ---                                                                                                 
@st.cache_data                                                         
def load_data():                                                                                                    
    df = pd.read_csv("data/cleaned/saas_sales_clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df                                                                                                       
                                                                          
df = load_data()                                                                                                    

# --- Landing Page Content ---
st.markdown(
    "<h1 style='text-align: center;'>"                                                                              
    "<i class='bi bi-cloud' style='margin-right: 12px;'></i>"               
    "AWS SaaS Sales Analysis</h1>",                                                                                 
    unsafe_allow_html=True                                                     
)                                                                                                                   
st.markdown(                                                                                                        
    f"<p style='text-align: center; font-size: 1.1rem; color: #555;'>"             
    f"A data-driven deep dive into ~10,000 SaaS transactions "                                                  
    f"across {df['Region'].nunique()} global regions</p>",                                                          
    unsafe_allow_html=True                                                                                          
)                                                                                                                   
                                                                                                
divider()                                                                                                           

st.markdown(
    "<p style='font-size: 0.85rem; text-transform: uppercase; "
    "letter-spacing: 0.08em; color: #999; margin-bottom: 0.5rem;'>"                                                 
    "At a glance</p>",                                                                                              
    unsafe_allow_html=True                                                                                          
)                                                                                                                   
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transactions", f"{len(df):,}")                                                                         
col2.metric("Regions", df["Region"].nunique())                                                       
col3.metric("Countries", df["Country"].nunique())                                                                   
col4.metric("Products", df["Product"].nunique())                                                                    
                                                                                                          
divider()                                                                                                           

st.markdown(""" 
      <div style='max-width: 680px; margin: 0 auto;'>                                                                 
        <h3>The Story</h3>                                                                                          
            <p>Every dataset tells a story. Ours is about <strong>~10,000 AWS SaaS
            transactions</strong> spanning three global regions — EMEA, AMER, and APJ —                                 
            enriched with <strong>World Bank data</strong> on GDP per capita and internet                               
            penetration. And one critical question:</p>                                                                 
        <blockquote style='border-left: 3px solid #a8d5e2; padding-left: 1rem; color: #555;'>                       
            <strong>Why are some regions profitable while others bleed money?</strong>                              
        </blockquote>                                                                                               
            <p>Is it the wealth of a country? The size of its digital infrastructure?                                   
        The type of customer? We tested all of it — with real statistics.                                           
        The answer is simpler, and more actionable, than you'd expect.</p>                                          
        <p>Navigate through the chapters using the sidebar:</p>                                                     
        <ol>                                                                                                        
            <li><strong>The Protagonist</strong> — Who is the typical AWS SaaS customer?</li>                       
            <li><strong>The Hero Stories</strong> — Five business questions, tested with statistics</li>
            <li><strong>Summary</strong> — Key findings and recommendations</li>                                    
        </ol>                                                                                                       
    </div>                                                                                                          
""", unsafe_allow_html=True)                                                                       
                                                                                                                      
 