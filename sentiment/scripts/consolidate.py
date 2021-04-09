def consolidateData(dataSource):
    scoresToConsolidate = [col for col in dataSource.columns if 'Score' in col and col != 'finalScore']

    mode = dataSource[scoresToConsolidate].mode(axis = 1)
    mode = mode.iloc[:, 0].where(mode.iloc[:, 1:].isna().all(axis=1))
    mode = mode.fillna('Neutral')

    dataSource['finalScore'] = mode

    return dataSource