import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd

import plotly.express as px
import plotly

# Import data
sales = pd.read_csv('sales.csv')
product_info = pd.read_csv('product_info.csv')

# Merge tables into one
orders = pd.merge(sales, product_info)
# Create pie chart
bar_chart = px.bar(
    data_frame=sales,
    x="Region",
    y="Units",
    title="Number of units by region",
    orientation="v",
    barmode="relative"
)
# Create an app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
# Create app layout
app.layout = html.Div([
    dbc.Row([

        dbc.Col(children=[
            html.H1("Filters"),
            dcc.Dropdown(id="dropdown",
                         options=[
                             {"label": "Pen", "value": "Item"},
                             {"label": "Pencil", "value": "Item"},
                             {"label": "Pen Set", "value": "Item"}
                         ]),
            html.Div(id='dd-output-container'),
            html.Br(),
            dcc.Slider(id='slider',
                       min=0,
                       max=100,
                       step=1,
                       marks={
                                0: '0 units',
                                10: '10 units',

                                30: '30 units',

                                50: '50 units',

                                70: '70 units',

                                90: '90 units',

                            },
                       value=10,
                       ),
            html.Div(id='slider-output-container'),
            dcc.Graph(id="pie-chart",
                      figure=bar_chart)

        ], width=4),

        dbc.Col(html.Div(children=[
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in orders.columns],
                data=orders.to_dict("records"),  # content of the table
                editable=True,

                filter_action="native",  # allows to filter data
                sort_action="native",  # allows sorting
                column_selectable="single",  # multi column selection
                row_selectable="multi",  # multi row selection
                selected_columns=[],
                selected_rows=[],

                page_action="native",
                page_current=0,
                page_size=10,

                style_cell={
                    "minWidth": 95, "maxWidth": 95, "width": 95, 'textAlign': 'left', 'padding': '3px'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                })]))
    ])])


@app.callback(dash.dependencies.Output('dd-output-container', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(dash.dependencies.Output('slider-output-container', 'children'),
              [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True)
