import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from function import refresh_data, generate_geo, generate_pie, generate_bar
from feeds import refresh_news, refresh_tweets
from layout_components import header, interval, update_cards, news_cards_generator

external_stylesheets = [dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# =============================================================================INITIAL STATE
query = 'corona virus'
source = ''
df, df_region, table, text = refresh_data()
news_feed = refresh_news(query, source)
tweets_feed = refresh_tweets()
# ====================================================================================LAYOUT

app.layout = html.Div([
    header,
    interval,
    dbc.Row([
        dbc.Col([
            update_cards(df),
            dcc.Graph(
                id='geo-chart',
                figure=generate_geo(),
            ),
            html.H3('Regional Information'),
            dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True),
        ], id="main-col-1", lg=7, md=12, ),

        dbc.Col([
            html.H3('Headline News', style={'margin-left': '0.5em'}),
            dbc.Row([
                dbc.Col(dbc.Input(type="search", placeholder="Search today's headline news",id="search"), width=10),
                dbc.Col(dbc.Button("Refresh", color="primary",id='news_refresh'), width=2),
            ],id='news_search'),
            news_cards_generator(news_feed),
        ], id="main-col-2", lg=5, md=12)
    ]),

], id='container')

if __name__ == '__main__':
    app.run_server(debug=True)
