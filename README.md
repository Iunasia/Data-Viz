# ASEAN Data Dashboard

An interactive web dashboard built with **Python and Streamlit** that visualizes ASEAN country data across economy, population, and job trends.

Uses **Object-Oriented Programming** for reusable, maintainable chart components.

---

## Features

- Bar and Pie chart visualizations
- Multiple pages: Economy, Population, Jobs
- Interactive data filtering
- OOP-based chart design (BaseChart → BarChart, PieChart)

---

## Project Structure

```
project/
├── app.py
├── pages/
│   ├── economy.py
│   ├── population.py
│   └── jobs.py
├── charts/
│   ├── base_chart.py
│   ├── bar_chart.py
│   └── pie_chart.py
├── data/
│   └── dataset.csv
└── README.md
```

---

## OOP Design

| Class | Role |
|-------|------|
| `BaseChart` | Parent class with shared logic |
| `BarChart` | Inherits from BaseChart |
| `PieChart` | Inherits from BaseChart |

---

## Technologies

- Python
- Streamlit
- Pandas
- Matplotlib / Plotly

---

## How to Run

1. Install dependencies:

```bash
pip install streamlit pandas matplotlib plotly
```

2. Run the app:

```bash
streamlit run app.py
```
