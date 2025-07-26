import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# DB & Data 
df = pd.read_csv(r"test_dataset.csv", sep=',')
df.dropna(inplace=True)


# Date Features 
df['Date'] = pd.to_datetime(df['Date'])
df['Point'] = df['Date'].dt.to_period('M').dt.to_timestamp() # month_start
df['month'] = df['Date'].dt.to_period('M').astype(str)

#  Init 
app = Dash(__name__)
unique_months = sorted(df['month'].unique())
unique_countries = sorted(df['Country'].unique())

# Layout 
app.layout = html.Div([
    html.H2("Country Charts", style={
        'backgroundColor': '#f0f0f0',
        'padding': '10px', 'fontWeight': 'normal', 'marginTop': '0px', 'textAlign': 'left'
    }),

    html.Div([
        html.Div([
            html.Label('Choose a month:', style={
                'fontSize': '16px', 'color': '#34495E', 'marginBottom': '5px'
            }),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': m, 'value': m} for m in unique_months],
                value=unique_months[0],
                clearable=False,
                style={'width': '120px'}
            ),
        ], style={'marginRight': '30px'}),

        html.Div([
            html.Label('Choose countries:', style={
                'fontSize': '16px', 'color': '#34495E', 'marginBottom': '5px'
            }),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in unique_countries],
                value=unique_countries,
                multi=True,
                clearable=False,
                style={'width': '350px'}
            ),
        ]),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='pie-chart', style={'width': '50%'}),
        dcc.Graph(id='line-chart', style={'width': '50%'})
    ], style={'display': 'flex', 'justifyContent': 'center'})
])



# Callback 
@app.callback(
    Output('pie-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('month-dropdown', 'value'),
    Input('country-dropdown', 'value')
)

def update_charts(selected_month, selected_countries):
    filtered = df[df['Country'].isin(selected_countries)]

    color_map = {
        'USA': '#474853',
        'Germany': '#86B3D1',
        'China': '#844D36',
        'Brazil': '#AAA0A0'
    }

    # Pie Chart 
    pie_data = filtered[filtered['month'] == selected_month]
    pie_counts = pie_data['Country'].value_counts().reset_index()
    pie_counts.columns = ['Country', 'Count']

    pie_fig = px.pie(
        pie_counts,
        names='Country',
        values='Count',
        color='Country',
        color_discrete_map=color_map
    )
    pie_fig.update_layout(
        title='Clients Distribution',
        title_x=0.5,
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=600,
        legend=dict(orientation='h', x=0.5, xanchor='center', yanchor='top', y=-0.1),
        transition=dict(duration=500, easing='cubic-in-out')
    )
    pie_fig.update_traces(
        textinfo='percent+label',
        pull=[0.011] * len(pie_counts),
        marker=dict(line=dict(color='black', width=0.5)),
        hovertemplate='%{label}<br>Clients: %{value} (%{percent})<extra></extra>'
    )


    # --- Line Chart ---
    line_data = filtered[filtered['month'] == selected_month]
    daily_counts = line_data.groupby(['Date', 'Country']).size().reset_index(name='Count')
    
    line_fig = px.line(
        daily_counts,
        x='Date',
        y='Count',
        color='Country',
        markers=True,
        color_discrete_map=color_map,
        line_shape='spline'  # сглаженные линии
    )

    line_fig.update_traces(
        mode='lines+markers',
        line=dict(width=4),
        marker=dict(size=7, line=dict(width=0.5, color='gray')),
        fill='tozeroy',    # заливка под линией
        fillcolor='rgba(0, 0, 0, 0.03)',
        opacity=0.9,
        hovertemplate='%{x|%Y-%m-%d}<br>%{y} clients<br>%{fullData.name}<extra></extra>'
    )

    line_fig.update_layout(
        title='Clients Count',
        title_x=0.5,
        xaxis_title='',
        yaxis_title='',
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=600,
        legend=dict(orientation='h', x=0.5, xanchor='center', yanchor='top', y=-0.15),
        margin=dict(t=50, b=40, l=40, r=40),
        transition=dict(duration=500, easing='cubic-in-out')
    )

    return pie_fig, line_fig
    
#  Run App 
if __name__ == '__main__':
    app.run(debug=True)
