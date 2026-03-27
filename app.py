import streamlit as st                                         
from utils.styles import apply_styles                                                                               

st.set_page_config(
    page_title="AWS SaaS Sales Analysis",
    page_icon="☁️ ",
    layout="wide",
    initial_sidebar_state="expanded"                                                                                
)                                                                                                     

pg = st.navigation([
    st.Page("pages/home.py",                    title="The Story",          icon=":material/home:"),
    st.Page("pages/1_📊_The_Protagonist.py",    title="The Protagonist",    icon=":material/person:"),        
    st.Page("pages/2_🔍_Business_Questions.py", title="The Hero Stories",   icon=":material/search:"),        
    st.Page("pages/3_📋_Summary.py",            title="Summary",            icon=":material/summarize:"),     
])                                                                                                                  
pg.run() 
                          