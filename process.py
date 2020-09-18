import sys
import os
import pandas
import matplotlib
from matplotlib import pyplot
import numpy
import seaborn

def find_missing_data(df):
    # missing data
    print("MISSING DATA")
    missing_data = df.isnull()
    for column in missing_data.columns.values.tolist():
        if True in missing_data[column].value_counts().keys():
            print(column)
            print(missing_data[column].value_counts())
            print("")

for arg in [os.path.abspath(i) for i in sys.argv[1:]]:
    fname = "{0}.csv".format(os.path.basename(arg))
    df = pandas.read_csv(fname)
    df['basename'].replace(numpy.NaN, "", inplace=True)
    # reset index, because we droped rows
    df.reset_index(drop=True, inplace=True)
    
    df['path'].replace(numpy.NaN, "/", inplace=True)
    # reset index, because we droped rows
    df.reset_index(drop=True, inplace=True)

    df['softlink'].replace(numpy.NaN, "", inplace=True)
    # reset index, because we droped rows
    df.reset_index(drop=True, inplace=True)

    print(df.describe(include="all"))

    print(df.dtypes)

    # convert the update and modication time columns to date time
#    df['update'] = pandas.to_datetime(df['update'])
#    df['modification'] = pandas.to_datetime(df['modification'])
#    print(df.dtypes)


    print(df.corr())

    seaborn.boxplot(x="UID", y="bytes", data=df)
    matplotlib.pyplot.show();
    exit(0)
    bins = numpy.linspace(min(df["blocks"]), max(df["blocks"]), 4)
    print(bins)
    group_names = ['Low', 'Medium', 'High']
    df['blocks-binned'] = pandas.cut(df['blocks'], bins, labels=group_names, include_lowest=True )
    print(df[['blocks','blocks-binned']].head(20))
    print(df["blocks-binned"].value_counts())

    matplotlib.pyplot.hist(df["blocks"])

    # set x/y labels and plot title
    matplotlib.pyplot.xlabel("blocks")
    matplotlib.pyplot.ylabel("count")
    matplotlib.pyplot.title("blocks bins")

    pyplot.show()

    pyplot.bar(group_names, df["blocks-binned"].value_counts())

    # set x/y labels and plot title
    matplotlib.pyplot.xlabel("blocks")
    matplotlib.pyplot.ylabel("count")
    matplotlib.pyplot.title("blocks bins")

    pyplot.show()
