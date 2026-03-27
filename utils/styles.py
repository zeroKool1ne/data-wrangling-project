import streamlit as st                                   
                                                           
                                                           
def apply_styles():                                      
    # Load Google Font (DM Sans) + Bootstrap Icons       
    st.markdown("""
        <link rel="preconnect"                           
            href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?fam
            ily=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
        <link rel="stylesheet"                           
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
                                                           
        <style> 
            /* Font override */
            html, body, [class*="css"] {
                font-family: 'DM Sans', sans-serif;      
            }
                                                           
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

            /* Tab bar: space-between across full width */
            stTabs [data-baseweb="tab-list"] {          
                gap: 0;                                  
                display: flex;
                justify-content: space-between;          
            }   

            /* Individual tab */                         
            .stTabs [data-baseweb="tab"] {
                flex: 1;                                 
                text-align: center;
                border-radius: 8px 8px 0 0;
            }                                            
   
            /* Reduce divider margin inside tabs */      
            .stTabs hr {
                margin-top: 0.5rem;                      
                margin-bottom: 0.5rem;
            }
            /* Hide Streamlit footer and main menu */                                                                           
                footer {visibility: hidden;}
                #MainMenu {visibility: hidden;}                                                                                     
                header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
                                                           
   
def divider():                                           
        """Custom divider — replaces st.divider()"""
        st.markdown("""                                      
        <div style="
              border: none;                                
              border-top: 1.5px solid #e0e6ed;
              margin: 1.5rem 0;                            
              border-radius: 2px;
          "></div>                                         
        """, unsafe_allow_html=True)