from flask import Flask, render_template,request,jsonify, g

import json
import plotly

import pandas as pd
import numpy as np

import datetime

# import simplejson as json

from pandas import Series, DataFrame


app = Flask(__name__)
app.debug = True



def get_df():
    df = getattr(g, '_df', None)
    if df is None:
        df = pd.read_excel('./sales_dummy_data.xlsx', sheet_name='Sales Data')
        df = g._df = df.set_index(pd.DatetimeIndex(df['Transaction_Date']))
        # df = g._df = df.resample(frequency).agg([np.sum, np.mean]).fillna(0).reset_index()
    return df

def load_data(freq):
    df = get_df()
    res_df = df.drop(df.columns[[0,1,2]], axis =1 )
    # res_df = res_df.resample(freq).agg([np.sum, np.mean]).fillna(0)
    res_df = res_df.resample(freq).sum().fillna(0)

    # quant_df = df['Quantity '].resample(freq).agg([np.sum, np.mean]).fillna(0).reset_index()

    return res_df


@app.route('/',  methods = ['GET'])
def index():
    freq = request.args.get('freq')
    if freq:
        # return jsonify(load_data(mode))
        return load_data(freq).to_json()
    else:
        return render_template('index.html', rows = (load_data('W').to_json()))
    


@app.route('/getReturned',  methods = ['GET'])
def getReturned():
    start = request.args.get('start')
    end =  request.args.get('end')
    print('start')
    print(start)
    print(end)
    if start and end:
        df = pd.read_excel('./sales_dummy_data.xlsx', sheet_name='Sales Data')
        df = df.set_index(pd.DatetimeIndex(df['Transaction_Date']))
        res = df.loc[(df['Quantity '] < 0) 
                & (df.index > datetime.datetime.strptime(start, '%Y-%m-%d')) 
                & (df.index < datetime.datetime.strptime(end, '%Y-%m-%d')) ]
        return jsonify(res.to_html(index=False, classes=["table-bordered", "table-striped", "table-hover"]))
    else:
        print("xxxxx")
        return jsonify([start, end])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
