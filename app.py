import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

base_companies = [
    'ExxonMobil', 'Chevron', 'BP', 'Royal Dutch Shell', 'TotalEnergies', 
    'NextEra Energy', 'Duke Energy', 'Southern Company', 'Dominion Energy', 
    'National Grid', 'Iberdrola', 'Enel', 'Orsted', 'First Solar', 
    'Suncor Energy', 'Canadian Natural Resources', 'China Petroleum & Chemical', 
    'PetroChina', 'Saudi Aramco', 'Equinor', 'ConocoPhillips', 'Eni', 
    'Public Service Enterprise Group', 'Xcel Energy', 'EDP Renewables', 
    'ENGIE', 'Repsol', 'Vattenfall', 'RWE', 'Chesapeake Energy', 
    'SunPower', 'Pattern Energy', 'EDP-Energias de Portugal', 'Calpine Corporation', 
    'Covanta', 'Avangrid', 'AES Corporation', 'TransAlta', 'Pacific Gas and Electric', 
    'Fortis Inc.', 'Algonquin Power & Utilities', 'Noble Energy', 'Williams Companies'
]

prefixes = ['Global', 'Green', 'United', 'Pure', 'Future', 'NextGen', 'Eco', 'Blue', 'Red', 'Bright', 'Dynamic', 'Peak', 'Sustainable', 'Clean', 'Quantum', 'Synergy']
suffixes = ['Energy', 'Power', 'Corporation', 'Industries', 'Resources', 'Fuels', 'Group', 'Systems', 'Technologies', 'Utilities', 'Holdings', 'Solutions', 'Enterprises', 'Partners']

np.random.seed(42)
generated_companies = np.random.choice(base_companies, size=300).tolist()
generated_companies += [f"{np.random.choice(prefixes)} {np.random.choice(suffixes)}" for _ in range(700)]

num_records = 1000
data = pd.DataFrame({
    'Company_Name': generated_companies,
    'GHG_emissions_tCO2e': np.random.uniform(100, 1000, size=num_records),
    'Water_usage_m3': np.random.uniform(1000, 10000, size=num_records),
    'Waste_generation_tons': np.random.uniform(10, 100, size=num_records),
    'Energy_efficiency_score': np.random.uniform(0, 100, size=num_records),
    'Renewable_energy_usage_percentage': np.random.uniform(0, 100, size=num_records),
    'Labor_practices_and_human_rights': np.random.uniform(0, 100, size=num_records),
    'Health_and_safety_performance': np.random.uniform(0, 100, size=num_records),
    'Community_engagement_and_development': np.random.uniform(0, 100, size=num_records),
    'Board_composition_and_diversity': np.random.uniform(0, 100, size=num_records),
    'Executive_compensation_and_accountability': np.random.uniform(0, 100, size=num_records),  
    'Investment': np.random.uniform(100, 1000, size=num_records),
    'Income': np.random.uniform(200, 2000, size=num_records)
})

data['Profit'] = data['Income'] - data['Investment']

data.to_csv('esg_data.csv', index=False)


# Custom CSS to enhance the UI
st.markdown("""
    <style>
    body {
        background-color: #F5F5F5;
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #333;
        text-align: center;
    }
    .stSidebar {
        background-color: #0E1117;
        color: white;
    }
    .css-18e3th9 {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    .css-18ni7ap {
        background-color: #0E1117;
        color: white;
    }
    .esg-box {
        background-color: #1F1F1F;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: #E8E8E8;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title('🌿 ESG Score Calculator and Tax Estimator')
st.markdown("<h3 style='text-align: center;'>Easily calculate and rank companies based on their ESG scores, with tax estimation for energy companies</h3>", unsafe_allow_html=True)

# Define ESG parameters and weights
def get_default_esg_params():
    return {
        'Environmental': {
            'GHG_emissions_tCO2e': 0.3,
            'Water_usage_m3': 0.2,
            'Waste_generation_tons': 0.1,
            'Energy_efficiency_score': 0.1,
            'Renewable_energy_usage_percentage': 0.1
        },
        'Social': {
            'Labor_practices_and_human_rights': 0.2,
            'Health_and_safety_performance': 0.2,
            'Community_engagement_and_development': 0.1
        },
        'Governance': {
            'Board_composition_and_diversity': 0.2,
            'Executive_compensation_and_accountability': 0.2
        }
    }

# Function to calculate raw ESG score
def calculate_esg_score(row, esg_params):
    esg_score = 0
    for category, params in esg_params.items():
        for param, weight in params.items():
            esg_score += row[param] * weight
    return esg_score

# Function to calculate tax based on ESG score and income
def calculate_tax(company_esg_score, income):
    base_tax = income * 0.20
    if company_esg_score < 30:
        additional_tax = income * 0.10
    elif company_esg_score < 50:
        additional_tax = income * 0.07
    else:
        additional_tax = 0
    total_tax = base_tax + additional_tax
    return total_tax, additional_tax

# Sidebar: Customize ESG parameters
st.sidebar.title("⚙️ Customize ESG Parameters")
st.sidebar.markdown("**Adjust the weights for different ESG categories and parameters**")
esg_params = get_default_esg_params()
for category, params in esg_params.items():
    st.sidebar.subheader(f"{category} Parameters")
    for param, default_weight in params.items():
        esg_params[category][param] = st.sidebar.slider(f"{param.replace('_', ' ')}", 0.0, 1.0, default_weight, 0.05)

# File upload for the CSV file
st.markdown("<h2 style='text-align: center;'>Upload your ESG data file (CSV)</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Calculate raw and normalized ESG scores
    df['Raw ESG Score'] = df.apply(lambda row: calculate_esg_score(row, esg_params), axis=1)
    min_esg_score = df['Raw ESG Score'].min()
    max_esg_score = df['Raw ESG Score'].max()
    df['ESG Score'] = 100 * (df['Raw ESG Score'] - min_esg_score) / (max_esg_score - min_esg_score)

    # Apply tax calculation
    df[['Total Tax', 'Additional Tax']] = df.apply(
        lambda row: pd.Series(calculate_tax(row['ESG Score'], row['Income'])), axis=1
    )

    # Filtering options for results
    st.sidebar.subheader("Filter Companies")
    min_score, max_score = st.sidebar.slider("ESG Score Range", 0, 100, (0, 100))
    min_tax, max_tax = st.sidebar.slider("Total Tax Range", 0, int(df['Total Tax'].max()), (0, int(df['Total Tax'].max())))

    filtered_df = df[(df['ESG Score'] >= min_score) & (df['ESG Score'] <= max_score) & 
                     (df['Total Tax'] >= min_tax) & (df['Total Tax'] <= max_tax)]

    # Improved Histogram for ESG Score Distribution with Spacing and Borders
    st.subheader("ESG Score Distribution")
    fig = px.histogram(df, x='ESG Score', nbins=30, title='Distribution of ESG Scores',
                   labels={'ESG Score': 'ESG Score'},
                   color_discrete_sequence=['#1f77b4'])
    
    fig.update_layout(
    xaxis_title='ESG Score',  # Ensuring the x-axis has a title
    yaxis_title='Number of Companies',  # Ensuring the y-axis has a title
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    margin=dict(l=40, r=40, t=40, b=40),  # Margins for spacing
    xaxis=dict(
        tickmode='linear',
        dtick=10,  # Interval between ticks
        showgrid=True,
        gridwidth=1,
        gridcolor='#DDDDDD'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#DDDDDD'
    ),
    bargap=0.2  # Gap between bars
)

    # Add border to bars
    fig.update_traces(marker=dict(line=dict(width=1, color='#000000')))

    # Display the histogram
    st.plotly_chart(fig)

    # Search Box for Company
    st.sidebar.subheader("Search for a Company")
    company_search = st.sidebar.text_input("Enter company name")

    if company_search:
        # Filter dataframe for the searched company
        company_df = filtered_df[filtered_df['Company_Name'].str.contains(company_search, case=False)]
        
        if not company_df.empty:
            # Show details for the selected company
            st.subheader(f"Details for {company_search}")

            for index, row in company_df.iterrows():
                st.write(f"### {row['Company_Name']}")
                esg_score = row['ESG Score']
                st.write(f"**ESG Score:** {esg_score}")
                
                # Display ESG Score Components
                esg_score_components = {
                    'Raw ESG Score': row['Raw ESG Score'],
                    'Normalized ESG Score': esg_score
                }
                for param, value in esg_score_components.items():
                    st.write(f"**{param}:** {value}")
                
                # Detailed ESG Score vs Tax Plot
                tax_vs_esg_fig = px.scatter(company_df, x='ESG Score', y='Total Tax', 
                                           title=f"Tax Amount vs ESG Score for {row['Company_Name']}",
                                           labels={'Total Tax': 'Total Tax'},
                                           color_discrete_sequence=['#ff7f0e'])
                tax_vs_esg_fig.update_layout(plot_bgcolor='#F5F5F5')
                st.plotly_chart(tax_vs_esg_fig)
                
                # Plot for Company Income
                income_fig = px.bar(company_df, x='Company_Name', y='Income', 
                                   title=f"Income for {row['Company_Name']}",
                                   labels={'Income': 'Income'},
                                   color_discrete_sequence=['#2ca02c'])
                income_fig.update_layout(plot_bgcolor='#F5F5F5')
                st.plotly_chart(income_fig)
            
        else:
            st.write(f"No company found with the name {company_search}")

    # Display filtered data
    st.subheader("Ranked Companies by ESG Score (Filtered)")
    st.dataframe(filtered_df[['Company_Name', 'ESG Score', 'Income', 'Total Tax', 'Additional Tax']])

    # Visualization: Tax vs ESG Score
    st.subheader("Tax vs ESG Score")
    scatter_fig = px.scatter(df, x='ESG Score', y='Total Tax', hover_name='Company_Name', title="Tax Amount vs ESG Score")
    scatter_fig.update_layout(plot_bgcolor='#F5F5F5')
    st.plotly_chart(scatter_fig)

    # Download filtered data option
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download Filtered Data", data=csv, file_name="filtered_companies.csv", mime='text/csv')

else:
    st.info('Please upload a CSV file to proceed.')
