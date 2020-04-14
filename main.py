import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from function import refresh_data, generate_geo, generate_pie, generate_bar
from feeds import refresh_news, refresh_tweets
from layout_components import header, interval, update_cards, news_cards_generator

external_stylesheets = [dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# =============================================================================INITIAL STATE
query = 'COVID-19'
source = ''
df, df_region, table, text = refresh_data()
news_feed = refresh_news(query, source)
tweets_feed = refresh_tweets()
# ====================================================================================LAYOUT

app.layout = html.Div([
    header,
    interval,
    dbc.Row([
        dbc.Col(children=dbc.Row([
            html.H3(['Worldwide Cases : ', 'Loading...']),
            dbc.Button("Refresh", color="primary", id='data_refresh')
        ])
            , id="main-col-1", lg=7, md=12, ),

        dbc.Col([
            html.H3("Today's News", style={'margin-left': '0.5em'}),
            dbc.Row([
                dbc.Col(dbc.Input(type="search", placeholder="Search today's news", id="search_bar"),
                        width=10),
                dbc.Col(dbc.Button("Refresh", color="primary", id='news_refresh'), width=2),
            ], id='news_search'),

            html.Div('', id='news-feeds')

        ], id="main-col-2", lg=5, md=12)
    ]),

], id='container')


@app.callback(
    Output('news-feeds', 'children'),
    [Input('news_refresh', 'n_clicks')],
    state=[State('search_bar', 'value')]
)
def update_news_feed(n_clicks, input1):
    if input1 == None:
        input1 = query
    else:
        pass
    try:
        news_feed = refresh_news(input1, source)
        news_cards = news_cards_generator(news_feed)
    except:
        news_cards = html.H1('No headline news found from this API')
    return news_cards


@app.callback(
    Output('main-col-1', 'children'),
    [Input('data_refresh', 'n_clicks')]
)
def update_data(n_clicks):
    df, df_region, table, text = refresh_data()
    output = [
        update_cards(df),
        dcc.Graph(
            id='geo-chart',
            figure=generate_geo(df, text),
        ),
        html.H3('Regional Information'),
        dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True),
    ]
    return output


if __name__ == '__main__':
    app.run_server(debug=True)
