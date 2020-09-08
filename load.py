#!/bin/python3
import sys
import os
import pandas
import matplotlib
from matplotlib import pyplot
import numpy

for arg in [os.path.abspath(i) for i in sys.argv[1:]]:
    fname = "{0}.csv".format(os.path.basename(arg))
    df = pandas.read_csv(fname)
    print(df)
    missing_data = df.isnull()
    print(missing_data)
    for column in missing_data.columns.values.tolist():
        print(column)
        print (missing_data[column].value_counts())
        print("")
    print(df.dtypes)
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

    pyplot.bar(group_names, df["blocks-binned"].value_counts())

    # set x/y labels and plot title
    matplotlib.pyplot.xlabel("blocks")
    matplotlib.pyplot.ylabel("count")
    matplotlib.pyplot.title("blocks bins")
