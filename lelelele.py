# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown for Launch Sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),

    # TASK 2: Pie Chart for Success Rate
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # TASK 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
                     title="Total Success Launches by Site")
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']
        fig = px.pie(class_counts, values='count', names='class',
                     title=f"Success vs. Failure for {selected_site}",
                     color='class', color_discrete_map={0: 'red', 1: 'blue'})
    return fig

# TASK 4: Callback for Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), 
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version', 
                     title="Correlation between Payload and Success",
                     hover_data=['Launch Site'])
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
