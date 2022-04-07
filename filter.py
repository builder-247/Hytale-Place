import pandas as pd
from multiprocessing import Pool

coord_to_tuple = lambda x: tuple(map(int, x.split(',')))

# [min, max] coordinates to read
Xrange = [323, 361]
Yrange = [614, 645]


# Filter to only include events inside specified region
def filter_region(chunk):
    filtered = chunk[chunk.apply(
        lambda row: (row['coordinate'][0] >= Xrange[0]) and (row['coordinate'][0] <= Xrange[1])
                    and (row['coordinate'][1] >= Yrange[0]) and (row['coordinate'][1] <= Yrange[1]), axis=1)]
    # print(len(filtered))
    return filtered


def read_file(path):
    result = None
    for chunk in pd.read_csv(path, compression='gzip', chunksize=10000,
                             converters={'coordinate': coord_to_tuple}):
        filtered_chunk = filter_region(chunk)
        if result is None:
            result = filtered_chunk
        else:
            result = pd.concat([result, filtered_chunk])

    return result


if __name__ == "__main__":
    files = []
    for i in range(0, 78):
        numeral = format(i, '012')
        files.append(f'./data/2022_place_canvas_history-{numeral}.csv.gzip')
    pool = Pool()
    a = pool.map(read_file, files)
    result = pd.concat(a).sort_values('timestamp')
    result.to_csv('./data/filtered.csv', index_label=False)
    print(result)
