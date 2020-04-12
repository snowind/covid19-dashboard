import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

dash_link = 'https://plotly.com/dash/'
twitter_link = 'https://developer.twitter.com/en/docs/api-reference-index'
ln_link = 'https://www.linkedin.com/in/kevin-sukaria-23a155137/'

header = \
    html.Div([
        html.H1('COVID-19 Tweet Streamer', style={'text-align': 'center'}),
        html.P([
            "This is a simple ",
            html.A(html.Strong('Dash'), href=dash_link),
            " web application that streams today's tweets about COVID-19 through ",
            html.A(html.Strong('official Twitter API'), href=twitter_link),
            ", Timezone used : GMT+7"],
        ),
        html.P(
            ['Creator : ',
             html.A(html.Strong('Kevin Sukaria'), href=ln_link)],
        )],
        style={'background-color': 'black', 'margin': '0 0 1em 0', 'text-align': 'center',
               'padding': '0.5em 0'})

interval = \
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # in milliseconds
        n_intervals=0
    )


def news_cards_generator(news_feed):
    news_cards = \
        [
            dbc.Card([
                dbc.CardHeader(val['title']),
                dbc.CardBody(val['desc'])
            ])
            for val in news_feed]

    news_container = \
        dbc.Card([
            dbc.CardHeader(html.H3('Headline News Feed')),
            dbc.CardBody(news_cards)
        ])
    return news_container
