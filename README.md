# Cybersecurity Risk Assessment Tool

An interactive cybersecurity risk assessment platform built with Streamlit.  
This tool evaluates an organization's security posture using weighted risk scoring and visualizes risk exposure across multiple cybersecurity domains.

The system collects assessment responses, calculates risk levels, and generates category-based risk insights inspired by industry cybersecurity frameworks such as NIST and CIS.

---

## Features

• Interactive cybersecurity questionnaire  
• Risk scoring using weighted security controls  
• Industry-based risk multipliers  
• Radar chart visualization of security risk categories  
• Secure account system with hashed passwords  
• SQLite database for storing assessment results  
• Data consent system for optional anonymized analytics  
• Clean modern UI with custom CSS styling  

---

## Tech Stack

Python  
Streamlit  
SQLite  
Plotly  
HTML/CSS

---

## How It Works

1. User consents to anonymized data usage.
2. Company selects its industry sector.
3. The system asks a series of cybersecurity control questions.
4. Responses are scored using weighted risk calculations.
5. Risk results are displayed with category breakdowns and visual charts.

The goal is to provide organizations with a quick overview of potential cybersecurity exposure areas.

---

## Installation

1. Clone the repository

2. Run the folder in Command Prompt or Terminal 

3. Enter: "streamlit run app.py"

## Note:

You must provide a Groq LLaMA API Key inside of .streamlit/secrets.toml to
be able to use the AI-Generated Advice

Link: https://console.groq.com/keys


## License

MIT License

Copyright (c) 2026 David Zilberman
