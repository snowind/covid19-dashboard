import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from function import refresh_data, generate_geo, generate_pie, generate_bar
from feeds import refresh_news, refresh_tweets
from layout_components import header, interval, news_carousel, update_cards

external_stylesheets = [dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# =============================================================================INITIAL STATE
query = 'corona virus'
source = 'bbc-news'
df, df_region = refresh_data()
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
                animate=True
            ),
        ], id="main-col-1", lg=7, xs=12, ),
        dbc.Col([
            news_carousel(news_feed),
        ], id="main-col-2", lg=5, xs=12)
    ]),

])
if __name__ == '__main__':
    app.run_server(debug=True)
