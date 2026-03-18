# 🌏 ASEAN Data Dashboard

## Project Overview
The ASEAN Data Dashboard is an interactive web application built using **Python and Streamlit**.  
It visualizes important data related to ASEAN countries such as **population, economy, and job trends**.

This project applies **Object-Oriented Programming (OOP)** concepts to create reusable and maintainable chart components.

---

## Objectives
- Provide clear data visualization for ASEAN datasets  
- Help users explore trends easily  
- Apply OOP concepts in a real-world project  
- Build an interactive dashboard using Streamlit  

---

## Features
- Bar Chart visualization  
- Pie Chart visualization  
- Multiple pages (Economy, Population, Jobs)  
- Interactive data filtering  
- OOP-based design (BaseChart, BarChart, PieChart)

---

## Project Structure
project/
│
├── app.py
├── pages/
│ ├── economy.py
│ ├── population.py
│ └── jobs.py
├── charts/
│ ├── base_chart.py
│ ├── bar_chart.py
│ └── pie_chart.py
├── data/
│ └── dataset.csv
└── README.md

---

## OOP Design
This project uses Object-Oriented Programming:

- **BaseChart** → Parent class  
- **BarChart** → Inherits from BaseChart  
- **PieChart** → Inherits from BaseChart  

This improves:
- Code reusability  
- Maintainability  
- Scalability  

---

## Technologies Used
- Python  
- Streamlit  
- Pandas  
- Matplotlib / Plotly  

---

## How to Run the Project

### 1. Install dependencies
```bash
pip install streamlit pandas matplotlib
