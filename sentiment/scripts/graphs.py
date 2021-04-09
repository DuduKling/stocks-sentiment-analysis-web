import json
import plotly
import plotly.express as px

def createProcessGraphs(dataSource):
    graphs = []

    scores = [col for col in dataSource.columns if 'Score' in col and col != 'finalScore']
    for score in scores:
        graphs.append(plotHistogram(dataSource, score, f'Sentiment Analysis for {score}'))
        graphs.append(plotPie(dataSource, score, f'Distribution of Sentiments for {score}'))

    return graphs

def createConsolidatedGraphs(dataSource):
    graphs = []

    graphs.append(plotHistogram(dataSource, 'finalScore', 'Consolidated Sentiment Analysis'))
    graphs.append(plotPie(dataSource, 'finalScore', 'Consolidated Distribution of Sentiments'))

    return graphs

def plotHistogram(df, field, title):
    fig = px.histogram(
        df,
        x = field,
        title = title,
        labels = { field: 'Sentiment' },
        color = field,
        color_discrete_map = {
            'Negative':'red',
            'Neutral':'blue',
            'Positive':'green'
        },
        width = 600,
        height = 400
    )

    graphJSON = json.dumps({
        "type": f'{field}_Histogram',
        "data": json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    })

    return json.loads(graphJSON)

def plotPie(df, field, title):
    fig = px.pie(
        df,
        names = field,
        color = field,
        title = title,
        color_discrete_map = {
            'Negative':'red',
            'Neutral':'blue',
            'Positive':'green'
        },
        width = 600,
        height = 400
    )

    graphJSON = json.dumps({
        "type": f'{field}_Pie',
        "data": json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    })

    return json.loads(graphJSON)
