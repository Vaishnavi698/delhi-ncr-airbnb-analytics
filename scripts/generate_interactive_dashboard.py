import pandas as pd
import plotly.express as px

# 1. Load processed dataset
df = pd.read_csv('data/processed/delhi_ncr_airbnb_realistic.csv')

# 2. Chart 1: Interactive Box Plot for Price Distribution
fig1 = px.box(
    df,
    x='state',
    y='adjusted_price',
    color='state',
    points='outliers',
    title='1. Delhi-NCR Airbnb Nightly Price Distribution by State',
    labels={'adjusted_price': 'Nightly Price (₹)', 'state': 'State'},
    hover_data=['neighbourhood', 'room_type'],
)

# 3. Chart 2: Interactive Scatter Plot (Metro Distance vs Price)
fig2 = px.scatter(
    df,
    x='distance_to_metro_km',
    y='adjusted_price',
    color='room_type',
    size='review_scores_rating',
    hover_name='neighbourhood',
    title='2. Impact of Metro Distance on Pricing & Room Type',
    labels={
        'distance_to_metro_km': 'Distance to Metro (km)',
        'adjusted_price': 'Nightly Price (₹)',
    },
)

# 4. Generate standalone HTML Dashboard
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Delhi-NCR Airbnb Market Intelligence</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background-color: #f4f6f9; }}
        h1 {{ color: #1e293b; text-align: center; font-size: 28px; margin-bottom: 25px; }}
        .card {{ background: white; padding: 20px; margin-bottom: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    </style>
</head>
<body>
    <h1>Delhi-NCR Airbnb Market Intelligence Dashboard</h1>
    <div class="card">{fig1.to_html(full_html=False, include_plotlyjs='cdn')}</div>
    <div class="card">{fig2.to_html(full_html=False, include_plotlyjs='cdn')}</div>
</body>
</html>
"""

# 5. Save HTML dashboard
output_file = 'data/processed/interactive_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
  f.write(html_content)

print(
    f'Success! Interactive HTML dashboard generated at: {output_file}'
)