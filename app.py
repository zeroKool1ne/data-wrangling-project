import streamlit as st
import pandas as pd

# --- Page Config (MUST be the first Streamlit command) ---                     
st.set_page_config(
      page_title="AWS SaaS Sales Analysis",                                       
      page_icon="☁️ ",
      layout="wide",
      initial_sidebar_state="expanded"                                            
  )
                                                                                  
# --- Custom CSS for pastel theme ---
st.markdown("""
  <style>
      /* Main background */
      .stApp {                                                                    
          background-color: #fafafa;
      }                                                                           
                  
      /* Metric cards */                                                          
      [data-testid="stMetric"] {
          background-color: #f0f4f8;                                              
          border-radius: 12px;
          padding: 16px;                                                          
          box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      }                                                                           
                  
      /* Sidebar */
      [data-testid="stSidebar"] {
          background-color: #f0f4f8;                                              
      }
                                                                                  
      /* Tabs */  
      .stTabs [data-baseweb="tab"] {
          border-radius: 8px 8px 0 0;                                             
      }
  </style>                                                                        
  """, unsafe_allow_html=True)
                                                                                  
                                                                                  
# --- Data Loading (cached, shared across all pages) ---                        
@st.cache_data                                                                  
def load_data():
    df = pd.read_csv("data/cleaned/saas_sales_clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df                                                                   
  
df = load_data()                                                                
                  

# --- Landing Page Content ---
st.markdown("<h1 style='text-align: center;'>☁️   AWS SaaS Sales Analysis</h1>",
  unsafe_allow_html=True)
st.markdown(                                                                    
      f"<h5 style='text-align: center;'>A data-driven deep dive into "          
      f"{len(df):,} SaaS transactions across {df['Region'].nunique()} global regions</h5>",                                                                  
      unsafe_allow_html=True                                                      
  )                                                                                           
                                                                                  
st.divider()    

# Hero metrics row — computed from data                                         
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transactions", f"{len(df):,}")                                     
col2.metric("Regions", df["Region"].nunique())                                  
col3.metric("Countries", df["Country"].nunique())
col4.metric("Products", df["Product"].nunique())                                
                                                                                  
st.divider()
                                                                                  
# Project intro 
st.markdown("""                                                                 
  <div style='text-align: center;'>                                               
  <h3>The Story</h3>                                                              
  <p>Every dataset tells a story. Ours is about <strong>{:,} AWS SaaS             
  transactions</strong>
  spanning EMEA, AMER, and APJ — and one critical question:</p>                   
  <blockquote><strong>Why are some regions profitable while others bleed        
  money?</strong></blockquote>                                                    
  <p>Navigate through the chapters using the sidebar:</p>
  <ol style='display: inline-block; text-align: left;'>                           
  <li><strong>The Protagonist</strong> — Who is the typical AWS SaaS              
  customer?</li>
  <li><strong>The Hero Stories</strong> — Five business questions, tested with    
  statistics</li>                                                                 
  <li><strong>Summary</strong> — Key findings and recommendations</li>
  </ol>                                                                           
  </div>                                                                        
  """.format(len(df)), unsafe_allow_html=True)
                                                                                  
# Sidebar info  
st.sidebar.markdown("---")                                                      
st.sidebar.caption("Data: AWS SaaS Sales (Kaggle) + World Bank API")
st.sidebar.caption("Built with Streamlit · 2026")                               
                                                                                  
  
                          