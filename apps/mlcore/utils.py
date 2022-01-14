import pandas as pd


def get_experiment_statistics(experiment):
    df = pd.read_csv(experiment.dataset.path)
    df.drop(df.filter(regex="Unnamed"), axis=1, inplace=True)
    df.loc[:, df.columns.isin(['timestamp', 'Datetime'])] = df.loc[
        :, df.columns.isin(['timestamp', 'Datetime'])
    ].apply(pd.to_datetime, infer_datetime_format=True, errors='coerce')
    rows, columns = df.shape
    data = {
        'total_size': experiment.dataset.size,
        'number_of_rows': rows,
        'number_of_columns': columns,
        'status': 'ok',
        'stats': describe(df, ['skew', 'mad', 'kurt', column_type]).to_json(
            date_format='iso', double_precision=2, orient='columns'
        ),
    }
    return data


def describe(df, stats):
    d = df.describe(include='all', datetime_is_numeric=True)
    return d.append(df.reindex(d.columns, axis=1).agg(stats))


def column_type(x):
    return x.dtype.name
