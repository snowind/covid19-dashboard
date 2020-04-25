import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from util.function import refresh_data, generate_geo
from util.feeds import refresh_news
from layout.layout_components import header, interval, update_cards, news_cards_generator, country_filtering, create_dashboard, create_layout

df, df_region, table = refresh_data()
metas = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}
]
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=metas)
app.config['suppress_callback_exceptions'] = True
server = app.server

query = 'corona'
source = ''


app.layout = create_layout()


@app.callback(
    Output('news-feeds', 'children'),
    [Input('news_refresh', 'n_clicks')],
    state=[State('search_bar', 'value')]
)
def update_news_feed(n_clicks, input1):
    if input1 == None:
        input1 = query
    try:
        news_feed = refresh_news(input1, source)
        news_cards = news_cards_generator(news_feed)
    except:
        news_cards = html.H1('No news found')
    return news_cards


@app.callback(
    Output('main-col-1', 'children'),
    [
        Input('data_refresh', 'n_clicks'),
    ]
)
def update_data(n_clicks):
    global df
    global table
    df, df_region, table = refresh_data()
    output = [
        update_cards(df),
        dcc.Graph(
            id='geo-chart',
            figure=generate_geo(df),
            animate=False
        ),
        html.H3('Regional Information'),
        dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True),
    ]
    return output


@app.callback([
    Output('metric-title', 'children'),
    Output('metric', 'children'),
    Output('geo-chart', 'figure'),
],
    [Input('dropdown', 'value')])
def country_filter(value):
    if value == (None or 'Worldwide'):
        value = 'Worldwide'
        filtered_df = df
        filtered_region = df
    else:
        filtered_df = df[df.country == value]
        try:
            filtered_region = df[df['sub-region'] == filtered_df['sub-region'].values[0]]
        except:
            filtered_df = df
            filtered_region = df
    filtered_title, filtered_cards = country_filtering(filtered_df, value)
    filtered_figure = generate_geo(filtered_region)
    return filtered_title, filtered_cards,filtered_figure


if __name__ == '__main__':
    app.run_server(debug=True)
