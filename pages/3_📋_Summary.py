import streamlit as st                                                          
import pandas as pd                                                           
# --- Page Config ---
st.set_page_config(
    page_title="Summary",
    page_icon="📋",                                                             
    layout="wide"
)                                                                               
                                                                                
# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/saas_sales_clean.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])                         
    return df
                                                                                  
df = load_data()                                                              

                                                                                  
# --- Page Header ---
st.title("📋 Summary")                                                          
st.markdown("##### Key findings and recommendations")                         

st.divider()

                                                                                  
# --- Results Overview Table ---
st.markdown("### Hypothesis Test Results")                                      
                                                                                
results = pd.DataFrame({                                                        
    "Business Question": [
        "BQ1: GDP → Profit?",                                                   
        "BQ2: Internet → Transactions?",                                      
        "BQ3: Discounts by Region?",
        "BQ4: Profit by Segment?",                                              
        "BQ5: Discounts → Losses?"
    ],                                                                          
    "Test": [                                                                 
        "Linear Regression",
        "Pearson Correlation",                                                  
        "Independent t-Test",
        "One-Way ANOVA",                                                        
        "Chi-Square Test"                                                     
    ],
    "Result": [
        "H₀ NOT rejected",
        "H₀ NOT rejected",
        "H₀ REJECTED ✓",                                                        
        "H₀ NOT rejected",
        "H₀ REJECTED ✓"                                                         
    ],                                                                        
    "Strength": [
        "No effect",
        "No effect",                                                            
        "Strong",
        "No effect",                                                            
        "Extremely strong"                                                    
    ]
})
                                                                                  
st.dataframe(
    results,                                                                    
    use_container_width=True,                                                 
    hide_index=True
)

st.divider()

                                                                                  
# --- Key Insights ---
st.markdown("### Key Insights")                                                 
                                                                                
col1, col2 = st.columns(2)

with col1:
    st.success(
        "**What does NOT drive profitability:**\n\n"
        "- GDP per capita (R² = 0.005)\n"                                       
        "- Internet penetration (r = 0.07)\n"                                   
        "- Customer segment (F = 1.57, p = 0.21)\n\n"                           
        "External factors and customer type have no significant impact.",       
        icon="📊"                                                               
    )                                                                           
                                                                                  
with col2:                                                                      
    st.error(
        "**What DOES drive profitability:**\n\n"                                
        "- Regional discount strategy (p < 0.001)\n"                          
        "- Discount → Loss association (χ² = 2,123)\n"                          
        "- 100% of losses came from discounted transactions\n\n"                
        "**Discounting is the sole driver of losses.**",                        
        icon="🔥"                                                               
    )                                                                           
   
st.divider()                                                                    
                                                                                

# --- Recommendations ---
st.markdown("### Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "**1. Review APJ Discounts**\n\n"
        "APJ averages 27% discount — nearly 3x AMER. "                          
        "This is the biggest profitability leak.",                              
        icon="🌏"                                                               
    )                                                                           
                                                                                
with col2:                                                                      
    st.info(
        "**2. Set Discount Caps**\n\n"                                          
        "Every single loss-making transaction had a discount. "               
        "Implement maximum discount thresholds per region.",                    
        icon="📉"
    )                                                                           
                                                                                
with col3:                                                                      
    st.info(                                                                  
        "**3. Focus on Internal Levers**\n\n"
        "External market conditions don't matter — pricing "
        "strategy and discount governance do.",                                 
        icon="🎯"                                                               
    )                                                                           
                                                                                  
st.divider()                                                                  


# --- Data Sources ---
st.markdown("### Data Sources")
st.markdown(
    "- **AWS SaaS Sales Dataset** — "
    "[Kaggle](https://www.kaggle.com/datasets/nnthanh101/aws-saas-sales) "      
    f"({len(df):,} transactions, 2020–2023)\n"                                  
    "- **GDP per Capita** — World Bank API (NY.GDP.PCAP.CD)\n"                  
    "- **Internet Penetration** — World Bank API (IT.NET.USER.ZS)"              
)