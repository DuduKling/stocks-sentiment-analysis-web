import json
import pandas as pd
from flask import render_template

from scripts.dataSource import getDataFromSources
from scripts.dataPreprocess import preProcessData
from scripts.process import processData
from scripts.consolidate import consolidateData
from scripts.graphs import createProcessGraphs, createConsolidatedGraphs

def main(formData):
    dataSource = pd.DataFrame()

    dataSource = getDataFromSources(formData)
    if not isinstance(dataSource, pd.DataFrame):
        return render_template('sentiment.html', errorList = dataSource)

    dataPreProcess = preProcessData(formData, dataSource)
    if not isinstance(dataPreProcess, pd.DataFrame):
        return render_template('sentiment.html', errorList = dataPreProcess)

    dataProcess = processData(formData, dataPreProcess)
    if not isinstance(dataProcess, pd.DataFrame):
        return render_template('sentiment.html', errorList = dataProcess)

    dataProcessView = dataProcess[[col for col in dataProcess.columns if 'Score' in col or col == 'CleanText']]

    dataConsolidated = consolidateData(dataProcess)

    processedGraphs = createProcessGraphs(dataConsolidated)
    consolidatedGraphs = createConsolidatedGraphs(dataConsolidated)

    return render_template(
        'sentiment.html',
        formData = json.loads(json.dumps(formData)),

        dataSource = list(dataSource.values.tolist()),
        dataSourceSample = list(dataSource.head().values.tolist()),

        dataProcess = list(dataProcessView.values.tolist()),
        dataProcessSample = list(dataProcessView.head().values.tolist()),
        dataProcessColumnNames = dataProcessView.columns.values,
        dataProcessedGraphs = processedGraphs,
        zip = zip,

        dataConsolidated = list(dataConsolidated[['CleanText','finalScore']].values.tolist()),
        dataConsolidatedSample = list(dataConsolidated[['CleanText','finalScore']].head().values.tolist()),
        dataConsolidatedColumnNames = ['CleanText','finalScore'],
        dataConsolidatedGraphs = consolidatedGraphs
    )
