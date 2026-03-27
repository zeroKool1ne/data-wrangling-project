# BLOCK 1: Imports, Config & Data
import streamlit as st
import pandas as pd                                                             
import numpy as np
import plotly.express as px
import plotly.graph_objects as go                                               
from scipy import stats
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
                                                                                  
# --- Pastel palette used across all charts ---                                 
PASTEL = ["#a8d5e2", "#f9b4ab", "#fae3b0", "#b5ead7", "#d5b8ff"]
                                                                                  
# --- Page Header ---
st.markdown(                                                                                                        
    "<h1 style='text-align: center;'>"                                                                              
    "<i class='bi bi-search' style='margin-right: 10px;'></i>"
    "The Hero Stories</h1>",                                                                                        
    unsafe_allow_html=True                                                                                          
  )                                                                                                                   
st.markdown(                                                                                                        
    "<p style='font-size: 1.05rem; color: #555; text-align: center;'>"
    "Five business questions, tested with statistics</p>",            
      unsafe_allow_html=True                                                                                          
  )                     
                                                                                  
divider()    

# BLOCK 2: Create Tabs
# --- Tabs for each Business Question ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BQ1: GDP → Profit",                                                        
    "BQ2: Internet → Transactions",
    "BQ3: Discounts by Region",                                                 
    "BQ4: Profit by Segment",
    "BQ5: Discounts → Losses"                                                   
])  

# Block 3: BQ1 — GDP vs Profit (Linear Regression)
# --- BQ1: GDP per Capita vs Profit (Linear Regression) ---
with tab1:                                                                      
    st.markdown("### Does national wealth predict SaaS profitability?")
    st.markdown(                                                                
        "**H₀:** GDP per capita has no predictive power for profit  \n"
        "**H₁:** GDP per capita is a significant predictor of profit"           
    )           
                                                                                  
    # Aggregate by country — mean profit and GDP                                
    country_data = df.dropna(subset=["GDP_per_Capita"]).groupby("Country").agg(
        GDP=("GDP_per_Capita", "first"),                                        
        Profit=("Profit", "mean"),                                              
        Transactions=("Profit", "count")                                        
    ).reset_index()                                                             
                                                                                  
    # Run regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(country_data["GDP"], country_data["Profit"])                                                                           
   
    # Scatter plot with trendline                                               
    fig = px.scatter(
        country_data,
        x="GDP",
        y="Profit",
        size="Transactions",                                                    
        hover_name="Country",
        labels={"GDP": "GDP per Capita ($)", "Profit": "Avg Profit ($)"},       
        color_discrete_sequence=[PASTEL[0]]
    )                                                                              
   
    # Add regression line                                                       
    x_range = np.linspace(country_data["GDP"].min(), country_data["GDP"].max(), 100)                                                                            
    fig.add_trace(go.Scatter(
        x=x_range,                                                              
        y=intercept + slope * x_range,
        mode="lines",
        line=dict(color="#e07070"),
        name="Regression line",                                                 
        hovertemplate="Trend: $%{y:.2f}<extra></extra>"
    ))                                                                          
                  
    fig.update_layout(
        height=450,                                                                                                 
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",                                                                              
        font=dict(size=13)
    )                                                          
                                                                                                                                        
    st.plotly_chart(fig, use_container_width=True)

    # Results                                                                   
    col1, col2, col3 = st.columns(3)
    col1.metric("R²", f"{r_value**2:.4f}")                                      
    col2.metric("P-value", f"{p_value:.4f}")                                    
    col3.metric("Result", "H₀ NOT rejected")
                                                                                  
    st.markdown(
        "> **Conclusion:** GDP per capita explains only **0.5%** of profit "    
        "variance. National wealth does not predict SaaS profitability — "      
        "internal factors matter more."                                         
    )          

# Block 4: BQ2 — Internet Penetration vs Transactions (Pearson)
# --- BQ2: Internet Penetration vs Transactions (Pearson Correlation) ---
with tab2:                                                                      
    st.markdown("### Is SaaS adoption higher in connected countries?")
    st.markdown(                                                                
        "**H₀:** No relationship between internet penetration and transactions  \n"                                                                             
        "**H₁:** Higher internet penetration → more transactions"
    )                                                                           
                  
    # Aggregate by country
    internet_data =df.dropna(subset=["Internet_Penetration"]).groupby("Country").agg(              
                            Internet=("Internet_Penetration", "first"),
                            Transactions=("Profit", "count")                                        
                    ).reset_index()

    # Pearson correlation
    r, p_value = stats.pearsonr(internet_data["Internet"],internet_data["Transactions"])                                                  
   
     # Scatter plot                                                                                                  
    fig = px.scatter(                                                                                               
        internet_data,                                                                                              
        x="Internet",                                                                                               
        y="Transactions",
        hover_name="Country",                                                                                       
        size="Transactions",
        labels={                                                                                                    
            "Internet": "Internet Penetration (%)",
            "Transactions": "Number of Transactions"
        },
        color_discrete_sequence=[PASTEL[1]]
    )                                                                                                               
  
    # Add regression line (same as notebook's sns.regplot)                                                          
    slope, intercept, r_line, _, _ = stats.linregress(
        internet_data["Internet"], internet_data["Transactions"]                                                    
    )           
    x_range = np.linspace(internet_data["Internet"].min(), internet_data["Internet"].max(), 100)                    
    fig.add_trace(go.Scatter(                                                                                       
        x=x_range,
        y=intercept + slope * x_range,                                                                              
        mode="lines",
        line=dict(color="#e07070"),
        name="Regression line",                                                                                     
        hovertemplate="Trend: %{y:.0f}<extra></extra>"
    ))  

    fig.update_layout(
        height=450,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)                                                      
    )
                                                                                  
    st.plotly_chart(fig, use_container_width=True)

    # Results
    col1, col2, col3 = st.columns(3)
    col1.metric("Pearson r", f"{r:.4f}")                                        
    col2.metric("P-value", f"{p_value:.4f}")
    col3.metric("Result", "H₀ NOT rejected")                                    
                                                                                  
    st.markdown(
        "> **Conclusion:** Internet penetration shows almost no correlation "   
        "with transaction volume (r = {:.2f}). Major economies dominate "
        "regardless of internet access — market size and AWS presence "         
        "matter more than infrastructure.".format(r)                            
    )
    st.markdown("**Outlier Inspection — Countries outside the 95% CI:**")                                           
    outliers = pd.DataFrame({                                                                                       
          "Country":              ["United States", "United Kingdom", "Japan", "France", "Canada", "Australia",       
                                    "Mexico", "Germany"],                                                                                               
          "Transactions":         [2001, 1141, 985, 587, 506, 492, 469, 383],                                         
          "Internet Penetration": ["93.1%", "96.3%", "87.0%", "88.7%", "94.0%", "97.1%", "81.2%", "93.5%"]            
      })                                                                                                              
    st.dataframe(outliers, use_container_width=True, hide_index=True)                                               
    st.markdown(                                                                                                    
          "These 8 countries all exceed the 95% CI for transaction volume. "
          "Notice: **Australia (97% internet) has fewer transactions than Mexico (81%)** — "                          
          "market size and AWS presence drive volume, not connectivity."                                              
      )    

# Block 5: BQ3 — Discount EMEA vs AMER (t-Test)
# --- BQ3: Discount Rates EMEA vs AMER (Independent t-Test) ---
with tab3:                                                                      
    st.markdown("### Do discount strategies differ across regions?")
    st.markdown(                                                                
        "**H₀:** No difference in discount rates between EMEA and AMER  \n"
        "**H₁:** Discount rates differ significantly"                           
    )           
                                                                                  
    # Split data by region
    emea = df[df["Region"] == "EMEA"]["Discount"] * 100
    amer = df[df["Region"] == "AMER"]["Discount"] * 100                         
    apj = df[df["Region"] == "APJ"]["Discount"] * 100  # For context
                                                                                  
    # Independent samples t-test                                                
    t_stat, p_value = stats.ttest_ind(emea, amer)                               
                                                                                  
    # Box plot comparing all 3 regions for full context                         
    fig = px.box(
        df,                                                                     
        x="Region",
        y=df["Discount"] * 100,
        color="Region",                                                         
        color_discrete_sequence=PASTEL[:3],
        labels={"y": "Discount Rate (%)", "Region": "Region"},                  
        category_orders={"Region": ["AMER", "EMEA", "APJ"]}                     
    )                                                                           
                                                                                  
    fig.update_layout(                                                          
        height=450,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    ) 
    fig.update_traces(
        marker_line_color="#ccc", 
        marker_line_width=1
    )                                                                          
   
    st.plotly_chart(fig, use_container_width=True)                              
                  
    # Results
    col1, col2, col3 = st.columns(3)
    col1.metric("T-statistic", f"{t_stat:.4f}")
    col2.metric("P-value", f"{p_value:.6f}")                                    
    col3.metric("Result", "H₀ REJECTED ✓")
                                                                                  
    st.markdown(
        "> **Conclusion:** EMEA applies significantly higher discounts than "   
        "AMER ({:.1f}% vs {:.1f}%, p < 0.001). APJ discounts even more "
        "aggressively at {:.1f}% — a critical profitability risk.".format(emea.mean(), amer.mean(), apj.mean())                                                                       
    ) 

    st.markdown("**Regional discount means:**")                                                                     
    region_means = pd.DataFrame({                                                                                   
          "Region":          ["AMER", "EMEA", "APJ"],
          "Avg Discount":    ["10.9%", "14.1%", "27.0%"],                                                             
          "vs. AMER":        ["—", "+3.2pp", "+16.1pp"]                                                               
      })                                                                                                              
    st.dataframe(region_means, use_container_width=True, hide_index=True)                                           
    st.markdown(                                                                                                    
          "APJ is not included in the t-test (which compares EMEA vs. AMER), "                                        
          "but its 27% average discount — nearly **3x AMER** — makes it the "                                         
          "most critical profitability risk across all regions."                                                      
    )        

# Block 6: BQ4 — Profit by Segment (ANOVA)
# --- BQ4: Profit by Segment (One-Way ANOVA) ---
with tab4:                                                                      
    st.markdown("### Does customer segment affect profitability?")
    st.markdown(                                                                
        "**H₀:** No difference in profit across segments (SMB / Strategic / Enterprise)  \n"                                                                
        "**H₁:** Profit differs significantly across segments"
    )                                                                           
                  
    # Clip outliers to 5-95 percentile (same as notebook)                       
    lower_bound = df["Profit"].quantile(0.05)
    upper_bound = df["Profit"].quantile(0.95)                                   
    df_clipped = df[(df["Profit"] >= lower_bound) & (df["Profit"] <= upper_bound)]                                                                   
                  
    # ANOVA on clipped data                                                     
    segments = [
        group["Profit"].values                                                  
        for _, group in df_clipped.groupby("Segment")
    ]                                                                           
    f_stat, p_value = stats.f_oneway(*segments)
                                                                                  
    # Violin plot — shows distribution shape, not just quartiles                
    fig = px.violin(
        df_clipped,                                                             
        x="Segment",
        y="Profit",
        color="Segment",
        box=True,  # Adds a mini boxplot inside the violin
        color_discrete_sequence=PASTEL[:3],                                     
        labels={"Profit": "Profit ($)", "Segment": "Customer Segment"},         
        category_orders={"Segment": ["SMB", "Strategic", "Enterprise"]}         
    )                                                                           
                  
    fig.update_layout(                                                          
        height=450,
        showlegend=False,                                                       
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13)
    )

    st.plotly_chart(fig, use_container_width=True)                              
  
    # Results                                                                   
    col1, col2, col3 = st.columns(3)
    col1.metric("F-statistic", f"{f_stat:.4f}")
    col2.metric("P-value", f"{p_value:.4f}")
    col3.metric("Result", "H₀ NOT rejected")                                    
  
    # Show segment means                                                        
    st.markdown("**Segment means (clipped 5–95%):**")
    seg_means = df_clipped.groupby("Segment")["Profit"].mean()                  
    mcols = st.columns(3)                                                       
    for i, seg in enumerate(["SMB", "Strategic", "Enterprise"]):
        mcols[i].metric(seg, f"${seg_means[seg]:,.2f}")                         
                                                                                  
    st.markdown(
        "> **Conclusion:** Customer segment does **not** significantly affect " 
        "profit. All three segments average ~$19–20 per transaction. "
        "**Discounting is the real driver** — not customer type."               
    )                            

# Block 7: BQ5 — Discounts vs Losses (Chi² — der Climax!)
# --- BQ5: Discounts → Negative Profit (Chi-Square Test) — THE CLIMAX ---
with tab5:                                                                      
    st.markdown(                                                                                                        
      "<h3><i class='bi bi-graph-down-arrow' style='margin-right: 8px; color: #e07070;'></i>"                         
      "Do discounts eat into profit?</h3>",                                                                           
    unsafe_allow_html=True                                                                                          
    )                               
    st.markdown(
          "**H₀:** No association between discounts and negative profit  \n"      
          "**H₁:** Discounted transactions are more likely to result in losses"   
    )                                                                           
                                                                                  
    # Build contingency table                                                   
    df["Has_Discount"] = (df["Discount"] > 0).map({True: "Discount", False: "No Discount"})                                                                     
    df["Profit_Status"] = (df["Profit"] > 0).map({True: "Profit > 0", False: "Profit ≤ 0"})                                                                  
    contingency = pd.crosstab(df["Profit_Status"], df["Has_Discount"])
                                                                                  
    # Chi-square test
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)          
                  
    # --- Visualization: Stacked bar showing the 100% / 0% split ---            
    col_chart, col_table = st.columns([2, 1])
                                                                                  
    with col_chart:
        # Count transactions by discount and profit status                      
        plot_data = df.groupby(["Has_Discount", "Profit_Status"]).size().reset_index(name="Count")                              
                                                                                  
        fig = px.bar(                                                           
            plot_data,
            x="Has_Discount",
            y="Count",
            color="Profit_Status",
            barmode="group",
            color_discrete_map={
            "Profit > 0": PASTEL[3],   # Mint for profitable                
            "Profit ≤ 0": PASTEL[1]    # Salmon for losses                  
            },                                                                  
        labels={                                                            
            "Has_Discount": "",
            "Count": "Number of Transactions",
            "Profit_Status": ""                                             
            }
        )                                                                       

        fig.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=13),                                                 
            legend=dict(
            orientation="h",                                                
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1                                                             
            )
        )
        fig.update_traces(
            marker_line_color="#ccc", 
            marker_line_width=1
        )                                                                       
                  
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown("**Contingency Table:**")
        st.dataframe(                                                           
            contingency.style.format("{:,}"),
            use_container_width=True                                            
        )       
                                                                                  
        st.markdown(
            f"- **{contingency.loc['Profit ≤ 0', 'Discount']:,}** loss-making "
            "transactions had a discount  \n"                                   
            f"- **{contingency.loc['Profit ≤ 0', 'No Discount']:,}** loss-making"
            "transactions had no discount"
        )                                                                       
                  
    # Results
    divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chi² Statistic", f"{chi2:,.2f}")                               
    col2.metric("Degrees of Freedom", dof)
    col3.metric("P-value", f"{p_value:.6f}")                                    
    col4.metric("Result", "H₀ REJECTED ✓")
                                                                                  
    st.error(                                                                   
        "**100% of all 1,871 loss-making transactions had a discount applied. "
        "Zero non-discounted transactions resulted in a loss.** "               
        "Discounts are not just reducing profit — they are the sole driver of losses.",                                                                       
        icon=":material/warning:"
    ) 