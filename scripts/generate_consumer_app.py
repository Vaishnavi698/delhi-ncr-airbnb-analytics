import json
import os
import numpy as np
import pandas as pd

# Load dataset
csv_path = 'data/processed/delhi_ncr_airbnb_realistic.csv'
if not os.path.exists(csv_path):
  raise FileNotFoundError(f'Missing {csv_path}. Run Phase 2 first.')

df = pd.read_csv(csv_path)

# Inject Greenery/Surroundings Score if missing
if 'greenery_score' not in df.columns:
  np.random.seed(42)
  df['greenery_score'] = np.round(np.random.uniform(5.5, 9.8, size=len(df)), 1)
  df.to_csv(csv_path, index=False)

listings_data = df.to_dict(orient='records')
neighbourhoods = sorted(df['neighbourhood'].dropna().unique().tolist())
room_types = sorted(df['room_type'].dropna().unique().tolist())

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delhi-NCR Airbnb Consumer Market & Surroundings Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .navbar {{ background: linear-gradient(135deg, #ff385c, #e00b41) !important; }}
        .card-custom {{ border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); background: white; }}
        .metric-value {{ font-size: 22px; font-weight: 700; color: #0f172a; }}
        .badge-green {{ background-color: #10b981; color: white; padding: 4px 8px; border-radius: 6px; font-size: 11px; }}
        .badge-superhost {{ background-color: #ff385c; color: white; padding: 4px 8px; border-radius: 6px; font-size: 11px; }}
        .badge-instant {{ background-color: #3b82f6; color: white; padding: 4px 8px; border-radius: 6px; font-size: 11px; }}
    </style>
</head>
<body>

    <nav class="navbar navbar-dark mb-4 shadow-sm">
        <div class="container">
            <span class="navbar-brand mb-0 h1 fw-bold">🏡 Delhi-NCR Consumer Intelligence: Area, Greenery & Deals</span>
        </div>
    </nav>

    <div class="container pb-5">
        
        <!-- MULTI-FACTOR FILTERS -->
        <div class="card card-custom p-4 mb-4">
            <h5 class="card-title fw-bold text-dark mb-3">🔍 Consumer Decision & Filter Panel</h5>
            <div class="row g-3">
                <div class="col-md-3">
                    <label class="form-label fw-semibold">Locality / Micro-Market</label>
                    <select id="selectArea" class="form-select" onchange="updateDashboard()">
                        <option value="ALL">All Delhi-NCR Localities</option>
                        {''.join([f'<option value="{n}">{n}</option>' for n in neighbourhoods])}
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-semibold">Property / Room Type</label>
                    <select id="selectRoom" class="form-select" onchange="updateDashboard()">
                        <option value="ALL">All Property Types</option>
                        {''.join([f'<option value="{r}">{r}</option>' for r in room_types])}
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-semibold">Max Nightly Price (₹): <span id="budgetValue" class="text-primary">10000</span></label>
                    <input type="range" class="form-range" id="inputBudget" min="500" max="10000" step="250" value="10000" oninput="document.getElementById('budgetValue').innerText=this.value; updateDashboard();">
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-semibold">Min Greenery Score (🌳): <span id="greenValue" class="text-success">5.0</span>/10</label>
                    <input type="range" class="form-range" id="inputGreen" min="5.0" max="9.5" step="0.5" value="5.0" oninput="document.getElementById('greenValue').innerText=this.value; updateDashboard();">
                </div>
            </div>
        </div>

        <!-- 6 DYNAMIC CONSUMER METRIC CARDS -->
        <div class="row g-3 mb-4">
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Normal Price Range</div>
                    <div class="metric-value text-primary" id="metricRange">₹0 - ₹0</div>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Avg Nightly Rate</div>
                    <div class="metric-value" id="metricAvg">₹0</div>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Greenery Score</div>
                    <div class="metric-value text-success" id="metricGreen">0.0 / 10</div>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Metro Proximity</div>
                    <div class="metric-value text-warning" id="metricMetro">0.0 km</div>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Avg Guest Rating</div>
                    <div class="metric-value text-info" id="metricRating">0.0 ⭐</div>
                </div>
            </div>
            <div class="col-md-2">
                <div class="card card-custom p-3 text-center">
                    <div class="text-muted small">Available Stays</div>
                    <div class="metric-value text-secondary" id="metricCount">0</div>
                </div>
            </div>
        </div>

        <!-- COMPARISON CHARTS & ADVICE -->
        <div class="row g-3 mb-4">
            <div class="col-md-7">
                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="fw-bold m-0">📊 Surrounding Locality Comparison</h6>
                        <select id="chartMetricSelect" class="form-select form-select-sm w-auto" onchange="updateDashboard()">
                            <option value="price">Compare Prices (₹)</option>
                            <option value="greenery">Compare Greenery / Surroundings Score (🌳)</option>
                            <option value="metro">Compare Distance to Metro (km)</option>
                        </select>
                    </div>
                    <canvas id="comparisonChart" height="190"></canvas>
                </div>
            </div>
            <div class="col-md-5">
                <div class="card card-custom p-3">
                    <h6 class="fw-bold mb-2">💡 Locality & Surroundings Consumer Insights</h6>
                    <div id="consumerInsight" class="small text-secondary lh-lg">Select an area above to view locality insights.</div>
                </div>
            </div>
        </div>

        <!-- COMPLETE MULTI-FACTOR LISTINGS TABLE -->
        <div class="card card-custom p-4 mb-4">
            <h5 class="fw-bold mb-3">🏷️ Best Matching Stays (Ranked by Value & Factors)</h5>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>Listing Name</th>
                            <th>Locality & State</th>
                            <th>Property Type</th>
                            <th>Nightly Price</th>
                            <th>Greenery Score</th>
                            <th>Metro Dist.</th>
                            <th>Rating</th>
                            <th>Amenities</th>
                            <th>Badges</th>
                        </tr>
                    </thead>
                    <tbody id="dealsTableBody">
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <script>
        const allData = {json.dumps(listings_data)};
        let chartInstance = null;

        function updateDashboard() {{
            const selectedArea = document.getElementById('selectArea').value;
            const selectedRoom = document.getElementById('selectRoom').value;
            const maxBudget = parseFloat(document.getElementById('inputBudget').value);
            const minGreen = parseFloat(document.getElementById('inputGreen').value);
            const chartMetric = document.getElementById('chartMetricSelect').value;

            let filtered = allData.filter(d => {{
                let matchArea = (selectedArea === 'ALL' || d.neighbourhood === selectedArea);
                let matchRoom = (selectedRoom === 'ALL' || d.room_type === selectedRoom);
                let matchPrice = (d.adjusted_price <= maxBudget);
                let matchGreen = ((d.greenery_score || 7.0) >= minGreen);
                return matchArea && matchRoom && matchPrice && matchGreen;
            }});

            if (filtered.length > 0) {{
                const prices = filtered.map(d => d.adjusted_price).sort((a,b) => a-b);
                const avgPrice = Math.round(prices.reduce((a,b)=>a+b, 0) / prices.length);
                const q1 = prices[Math.floor(prices.length * 0.25)];
                const q3 = prices[Math.floor(prices.length * 0.75)];
                
                const avgGreen = (filtered.reduce((a,b)=>a + (b.greenery_score || 7.0), 0) / filtered.length).toFixed(1);
                const avgMetro = (filtered.reduce((a,b)=>a + (b.distance_to_metro_km || 1.0), 0) / filtered.length).toFixed(1);
                const avgRating = (filtered.reduce((a,b)=>a + (b.review_scores_rating || 4.5), 0) / filtered.length).toFixed(2);

                document.getElementById('metricRange').innerText = `₹${{q1}} - ₹${{q3}}`;
                document.getElementById('metricAvg').innerText = `₹${{avgPrice}}`;
                document.getElementById('metricGreen').innerText = `${{avgGreen}} / 10`;
                document.getElementById('metricMetro').innerText = `${{avgMetro}} km`;
                document.getElementById('metricRating').innerText = `${{avgRating}} ⭐`;
                document.getElementById('metricCount').innerText = filtered.length;

                document.getElementById('consumerInsight').innerHTML = `
                    <p class="mb-1">💰 <b>Normal Price Range:</b> 50% of stays in this selection range from <b>₹${{q1}}</b> to <b>₹${{q3}}</b>/night.</p>
                    <p class="mb-1">🌳 <b>Environment & Surroundings:</b> Average greenery rating is <b>${{avgGreen}}/10</b>.</p>
                    <p class="mb-1">🚇 <b>Transit Access:</b> Average distance to nearest metro station is <b>${{avgMetro}} km</b>.</p>
                    <p class="mb-0">⭐ <b>Guest Experience:</b> Average rating across available listings is <b>${{avgRating}}</b>.</p>
                `;
            }} else {{
                document.getElementById('metricRange').innerText = '₹0 - ₹0';
                document.getElementById('metricAvg').innerText = '₹0';
                document.getElementById('metricGreen').innerText = '0.0 / 10';
                document.getElementById('metricMetro').innerText = '0.0 km';
                document.getElementById('metricRating').innerText = '0.0 ⭐';
                document.getElementById('metricCount').innerText = '0';
                document.getElementById('consumerInsight').innerText = 'No listings match all chosen factors. Adjust your sliders or filter settings.';
            }}

            const sorted = [...filtered].sort((a,b) => a.adjusted_price - b.adjusted_price).slice(0, 10);
            const tbody = document.getElementById('dealsTableBody');
            tbody.innerHTML = '';
            sorted.forEach(item => {{
                tbody.innerHTML += `
                    <tr>
                        <td><b>${{item.name || 'Cozy NCR Listing'}}</b></td>
                        <td>${{item.neighbourhood}} <small class="text-muted">(${{item.state}})</small></td>
                        <td>${{item.room_type}}</td>
                        <td><span class="fw-bold text-success">₹${{item.adjusted_price}}</span>/night</td>
                        <td>🌳 <span class="fw-semibold">${{item.greenery_score || 7.5}}</span>/10</td>
                        <td>${{item.distance_to_metro_km || 1.0}} km</td>
                        <td>⭐ ${{item.review_scores_rating || 4.5}}</td>
                        <td>${{item.amenities_count || 12}} items</td>
                        <td>
                            ${{item.host_is_superhost === 't' ? '<span class="badge-superhost">Superhost</span> ' : ''}}
                            ${{item.instant_bookable === 't' ? '<span class="badge-instant">Instant Book</span>' : ''}}
                        </td>
                    </tr>
                `;
            }});

            renderComparisonChart(selectedArea, chartMetric);
        }}

        function renderComparisonChart(selectedArea, metric) {{
            const areaGroups = {{}};
            allData.forEach(d => {{
                if (!areaGroups[d.neighbourhood]) areaGroups[d.neighbourhood] = [];
                let val = d.adjusted_price;
                if (metric === 'greenery') val = d.greenery_score || 7.0;
                if (metric === 'metro') val = d.distance_to_metro_km || 1.0;
                areaGroups[d.neighbourhood].push(val);
            }});

            const labels = Object.keys(areaGroups).slice(0, 10);
            const dataValues = labels.map(l => {{
                const arr = areaGroups[l];
                return (arr.reduce((a,b)=>a+b,0)/arr.length).toFixed(1);
            }});

            const ctx = document.getElementById('comparisonChart').getContext('2d');
            if (chartInstance) chartInstance.destroy();

            chartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: metric.toUpperCase(),
                        data: dataValues,
                        backgroundColor: labels.map(l => l === selectedArea ? '#ff385c' : '#cbd5e1'),
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{ y: {{ beginAtZero: true }} }}
                }}
            }});
        }}

        window.onload = updateDashboard;
    </script>
</body>
</html>
"""

output_path = 'data/processed/consumer_app.html'
with open(output_path, 'w', encoding='utf-8') as f:
  f.write(html_template)

print(
    f' Success! Multi-Factor Consumer App generated at: {output_path}'
)