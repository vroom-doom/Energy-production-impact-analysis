# ESG Score Calculator and Tax Estimator

## Overview

The ESG Score Calculator and Tax Estimator is a web application built using Streamlit that allows users to calculate and rank energy production companies based on their ESG (Environmental, Social, and Governance) scores. It also provides tax estimation based on these scores. The app allows for customization of ESG parameters, filtering of results, and visualization of data through interactive plots.

## Features

- *ESG Score Calculation*: Calculate ESG scores based on customizable parameters.
- *Tax Estimation*: Estimate taxes for companies based on their ESG scores.
- *Interactive Filtering*: Filter companies by ESG score and total tax.
- *Visualizations*: Generate and view histograms and scatter plots of ESG scores and tax amounts.
- *Search Functionality*: Search for specific companies and view their details.
- *Data Upload and Download*: Upload your own CSV file for analysis and download filtered results.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.7 or later
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/esg-calculator.git
   cd esg-calculator

python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
