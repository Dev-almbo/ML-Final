{
 "cells": [
  {
   "cell_type": "markdown",
   "source": [
    "# Predicting Stock Prices using Machine Learning\n",
    "\n",
    "### Data Mining, Machine Learning, and Deep Learning\n",
    "\n",
    "Kitti Kresznai (141359) <br>\n",
    "Almut Bohnhoff (141021) <br>\n",
    "Anastasiya Vitaliyivna Strohonova (142820) <br>\n",
    "Natalie Schober (141354)\n",
    "\n"
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00000-070a00e1-f408-4a4c-b4ea-a79ec046758e",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00000-a019039d-0a21-4549-9b6b-8458aba963d3",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "ba15b259",
    "execution_start": 1621954328308,
    "execution_millis": 4441483,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#!pip install yahoo_fin==0.8.8 --ignore-installed\n",
    "#!pip install pmdarima==1.8.2 --ignore-installed\n",
    "#!pip install tensorflow==2.5.0 --ignore-installed\n",
    "\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')"
   ],
   "execution_count": 1,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Data Collection"
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00002-c145bb2c-b537-48f5-a180-88b240ec4216",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00000-3abc8af6-a309-4da5-b894-538765a950e4",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "5ff1489",
    "execution_start": 1621954328318,
    "execution_millis": 2634,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from yahoo_fin.stock_info import get_data\n",
    "import yahoo_fin.stock_info as si\n",
    "import pandas as pd\n",
    "\n",
    "# BAC - Bank of America Coporation - financial\n",
    "# BA - Boeing Company - industrial manufactoring\n",
    "# MDLZ - Mondelez International Inc. - consumer goods\n",
    "# PFE - Pfizer - health care \n",
    "# GOOG -  Tech industry\n",
    "ticker_list = ['BAC', 'BA', 'GOOG', 'MDLZ', 'PFE']\n",
    "\n",
    "\n",
    "# get historical time series data for stocks \n",
    "historical_datas = {}\n",
    "\n",
    "for ticker in ticker_list:\n",
    "    historical_datas[ticker] = get_data(ticker)\n",
    "\n",
    "stock_data = pd.concat(historical_datas)\n",
    "\n",
    "# get data for american indices \n",
    "sp = get_data('^GSPC')\n",
    "dow = get_data('^DJI')\n",
    "\n",
    "# clean stock data\n",
    "stock_data.reset_index(inplace = True)\n",
    "stock_data = stock_data.rename(columns = {'level_1': 'Date'})\n",
    "stock_data = stock_data.drop(columns = ['level_0'])\n",
    "stock_data['Date']= stock_data['Date'].dt.date\n",
    "\n",
    "# clean sp500 and dow jones\n",
    "sp.reset_index(inplace = True)\n",
    "dow.reset_index(inplace = True)\n",
    "sp = sp.rename(columns = {'index': 'Date'})\n",
    "dow = dow.rename(columns = {'index': 'Date'})\n",
    "sp['Date']= sp['Date'].dt.date\n",
    "dow['Date']= dow['Date'].dt.date\n",
    "\n",
    "sp = sp.rename( columns = {'high':'S&P500'})\n",
    "dow = dow.rename(columns = {'high': 'DowJones'})\n",
    "sp = sp[['Date', 'S&P500']]\n",
    "dow = dow[['Date', 'DowJones']]\n",
    "\n",
    "\n",
    "# filter out data from before 2017\n",
    "stock_data['Year']=stock_data['Date'].apply(lambda x: x.year)\n",
    "sp['Year']=sp['Date'].apply(lambda x: x.year)\n",
    "dow['Year']=dow['Date'].apply(lambda x: x.year)\n",
    "\n",
    "stock_data = stock_data[stock_data['Year']>=2017]\n",
    "sp = sp[sp['Year']>=2017]\n",
    "dow = dow[dow['Year']>=2017]\n",
    "stock_data = stock_data.drop(columns = ['Year'])\n",
    "sp = sp.drop(columns = ['Year'])\n",
    "dow = dow.drop(columns = ['Year'])\n",
    "\n",
    "data = stock_data.merge(sp, how ='left', on = 'Date')\n",
    "data = data.merge(dow, how = 'left', on = 'Date')\n",
    "\n",
    "data"
   ],
   "execution_count": 2,
   "outputs": [
    {
     "output_type": "execute_result",
     "execution_count": 2,
     "data": {
      "application/vnd.deepnote.dataframe.v2+json": {
       "row_count": 5530,
       "column_count": 10,
       "columns": [
        {
         "name": "Date",
         "dtype": "object",
         "stats": {
          "unique_count": 1106,
          "nan_count": 0,
          "categories": [
           {
            "name": "2017-01-03",
            "count": 5
           },
           {
            "name": "2017-01-04",
            "count": 5
           },
           {
            "name": "1104 others",
            "count": 5520
           }
          ]
         }
        },
        {
         "name": "open",
         "dtype": "float64",
         "stats": {
          "unique_count": 4405,
          "nan_count": 0,
          "min": "19.260000228881836",
          "max": "2420.0",
          "histogram": [
           {
            "bin_start": 19.260000228881836,
            "bin_end": 259.3340002059937,
            "count": 3824
           },
           {
            "bin_start": 259.3340002059937,
            "bin_end": 499.40800018310546,
            "count": 600
           },
           {
            "bin_start": 499.40800018310546,
            "bin_end": 739.4820001602172,
            "count": 0
           },
           {
            "bin_start": 739.4820001602172,
            "bin_end": 979.5560001373291,
            "count": 193
           },
           {
            "bin_start": 979.5560001373291,
            "bin_end": 1219.630000114441,
            "count": 479
           },
           {
            "bin_start": 1219.630000114441,
            "bin_end": 1459.7040000915526,
            "count": 195
           },
           {
            "bin_start": 1459.7040000915526,
            "bin_end": 1699.7780000686646,
            "count": 99
           },
           {
            "bin_start": 1699.7780000686646,
            "bin_end": 1939.8520000457763,
            "count": 62
           },
           {
            "bin_start": 1939.8520000457763,
            "bin_end": 2179.9260000228883,
            "count": 42
           },
           {
            "bin_start": 2179.9260000228883,
            "bin_end": 2420,
            "count": 36
           }
          ]
         }
        },
        {
         "name": "high",
         "dtype": "float64",
         "stats": {
          "unique_count": 4461,
          "nan_count": 0,
          "min": "19.670000076293945",
          "max": "2452.3779296875",
          "histogram": [
           {
            "bin_start": 19.670000076293945,
            "bin_end": 262.94079303741455,
            "count": 3827
           },
           {
            "bin_start": 262.94079303741455,
            "bin_end": 506.21158599853516,
            "count": 597
           },
           {
            "bin_start": 506.21158599853516,
            "bin_end": 749.4823789596558,
            "count": 0
           },
           {
            "bin_start": 749.4823789596558,
            "bin_end": 992.7531719207764,
            "count": 202
           },
           {
            "bin_start": 992.7531719207764,
            "bin_end": 1236.023964881897,
            "count": 485
           },
           {
            "bin_start": 1236.023964881897,
            "bin_end": 1479.2947578430176,
            "count": 184
           },
           {
            "bin_start": 1479.2947578430176,
            "bin_end": 1722.5655508041382,
            "count": 95
           },
           {
            "bin_start": 1722.5655508041382,
            "bin_end": 1965.8363437652588,
            "count": 62
           },
           {
            "bin_start": 1965.8363437652588,
            "bin_end": 2209.1071367263794,
            "count": 41
           },
           {
            "bin_start": 2209.1071367263794,
            "bin_end": 2452.3779296875,
            "count": 37
           }
          ]
         }
        },
        {
         "name": "low",
         "dtype": "float64",
         "stats": {
          "unique_count": 4431,
          "nan_count": 0,
          "min": "17.950000762939453",
          "max": "2406.360107421875",
          "histogram": [
           {
            "bin_start": 17.950000762939453,
            "bin_end": 256.79101142883303,
            "count": 3824
           },
           {
            "bin_start": 256.79101142883303,
            "bin_end": 495.63202209472655,
            "count": 600
           },
           {
            "bin_start": 495.63202209472655,
            "bin_end": 734.4730327606201,
            "count": 0
           },
           {
            "bin_start": 734.4730327606201,
            "bin_end": 973.3140434265136,
            "count": 196
           },
           {
            "bin_start": 973.3140434265136,
            "bin_end": 1212.1550540924072,
            "count": 488
           },
           {
            "bin_start": 1212.1550540924072,
            "bin_end": 1450.9960647583007,
            "count": 190
           },
           {
            "bin_start": 1450.9960647583007,
            "bin_end": 1689.8370754241944,
            "count": 93
           },
           {
            "bin_start": 1689.8370754241944,
            "bin_end": 1928.6780860900878,
            "count": 61
           },
           {
            "bin_start": 1928.6780860900878,
            "bin_end": 2167.5190967559815,
            "count": 42
           },
           {
            "bin_start": 2167.5190967559815,
            "bin_end": 2406.360107421875,
            "count": 36
           }
          ]
         }
        },
        {
         "name": "close",
         "dtype": "float64",
         "stats": {
          "unique_count": 4425,
          "nan_count": 0,
          "min": "18.079999923706055",
          "max": "2429.889892578125",
          "histogram": [
           {
            "bin_start": 18.079999923706055,
            "bin_end": 259.26098918914795,
            "count": 3822
           },
           {
            "bin_start": 259.26098918914795,
            "bin_end": 500.44197845458984,
            "count": 602
           },
           {
            "bin_start": 500.44197845458984,
            "bin_end": 741.6229677200317,
            "count": 0
           },
           {
            "bin_start": 741.6229677200317,
            "bin_end": 982.8039569854736,
            "count": 199
           },
           {
            "bin_start": 982.8039569854736,
            "bin_end": 1223.9849462509155,
            "count": 486
           },
           {
            "bin_start": 1223.9849462509155,
            "bin_end": 1465.1659355163574,
            "count": 188
           },
           {
            "bin_start": 1465.1659355163574,
            "bin_end": 1706.3469247817993,
            "count": 93
           },
           {
            "bin_start": 1706.3469247817993,
            "bin_end": 1947.5279140472412,
            "count": 62
           },
           {
            "bin_start": 1947.5279140472412,
            "bin_end": 2188.708903312683,
            "count": 41
           },
           {
            "bin_start": 2188.708903312683,
            "bin_end": 2429.889892578125,
            "count": 37
           }
          ]
         }
        },
        {
         "name": "adjclose",
         "dtype": "float64",
         "stats": {
          "unique_count": 5214,
          "nan_count": 0,
          "min": "17.632553100585938",
          "max": "2429.889892578125",
          "histogram": [
           {
            "bin_start": 17.632553100585938,
            "bin_end": 258.85828704833983,
            "count": 3852
           },
           {
            "bin_start": 258.85828704833983,
            "bin_end": 500.0840209960937,
            "count": 572
           },
           {
            "bin_start": 500.0840209960937,
            "bin_end": 741.3097549438476,
            "count": 0
           },
           {
            "bin_start": 741.3097549438476,
            "bin_end": 982.5354888916015,
            "count": 199
           },
           {
            "bin_start": 982.5354888916015,
            "bin_end": 1223.7612228393555,
            "count": 485
           },
           {
            "bin_start": 1223.7612228393555,
            "bin_end": 1464.9869567871092,
            "count": 189
           },
           {
            "bin_start": 1464.9869567871092,
            "bin_end": 1706.2126907348631,
            "count": 93
           },
           {
            "bin_start": 1706.2126907348631,
            "bin_end": 1947.438424682617,
            "count": 62
           },
           {
            "bin_start": 1947.438424682617,
            "bin_end": 2188.664158630371,
            "count": 41
           },
           {
            "bin_start": 2188.664158630371,
            "bin_end": 2429.889892578125,
            "count": 37
           }
          ]
         }
        },
        {
         "name": "volume",
         "dtype": "int64",
         "stats": {
          "unique_count": 5458,
          "nan_count": 0,
          "min": "323167",
          "max": "259545800",
          "histogram": [
           {
            "bin_start": 323167,
            "bin_end": 26245430.3,
            "count": 3908
           },
           {
            "bin_start": 26245430.3,
            "bin_end": 52167693.6,
            "count": 834
           },
           {
            "bin_start": 52167693.6,
            "bin_end": 78089956.9,
            "count": 496
           },
           {
            "bin_start": 78089956.9,
            "bin_end": 104012220.2,
            "count": 192
           },
           {
            "bin_start": 104012220.2,
            "bin_end": 129934483.5,
            "count": 63
           },
           {
            "bin_start": 129934483.5,
            "bin_end": 155856746.8,
            "count": 24
           },
           {
            "bin_start": 155856746.8,
            "bin_end": 181779010.1,
            "count": 9
           },
           {
            "bin_start": 181779010.1,
            "bin_end": 207701273.4,
            "count": 2
           },
           {
            "bin_start": 207701273.4,
            "bin_end": 233623536.70000002,
            "count": 1
           },
           {
            "bin_start": 233623536.70000002,
            "bin_end": 259545800,
            "count": 1
           }
          ]
         }
        },
        {
         "name": "ticker",
         "dtype": "object",
         "stats": {
          "unique_count": 5,
          "nan_count": 0,
          "categories": [
           {
            "name": "BAC",
            "count": 1106
           },
           {
            "name": "BA",
            "count": 1106
           },
           {
            "name": "3 others",
            "count": 3318
           }
          ]
         }
        },
        {
         "name": "S&P500",
         "dtype": "float64",
         "stats": {
          "unique_count": 1100,
          "nan_count": 0,
          "min": "2263.8798828125",
          "max": "4238.0400390625",
          "histogram": [
           {
            "bin_start": 2263.8798828125,
            "bin_end": 2461.2958984375,
            "count": 745
           },
           {
            "bin_start": 2461.2958984375,
            "bin_end": 2658.7119140625,
            "count": 715
           },
           {
            "bin_start": 2658.7119140625,
            "bin_end": 2856.1279296875,
            "count": 1365
           },
           {
            "bin_start": 2856.1279296875,
            "bin_end": 3053.5439453125,
            "count": 1035
           },
           {
            "bin_start": 3053.5439453125,
            "bin_end": 3250.9599609375,
            "count": 450
           },
           {
            "bin_start": 3250.9599609375,
            "bin_end": 3448.3759765625,
            "count": 430
           },
           {
            "bin_start": 3448.3759765625,
            "bin_end": 3645.7919921875,
            "count": 180
           },
           {
            "bin_start": 3645.7919921875,
            "bin_end": 3843.2080078125,
            "count": 195
           },
           {
            "bin_start": 3843.2080078125,
            "bin_end": 4040.6240234375,
            "count": 230
           },
           {
            "bin_start": 4040.6240234375,
            "bin_end": 4238.0400390625,
            "count": 185
           }
          ]
         }
        },
        {
         "name": "DowJones",
         "dtype": "float64",
         "stats": {
          "unique_count": 1106,
          "nan_count": 0,
          "min": "19121.009765625",
          "max": "35091.55859375",
          "histogram": [
           {
            "bin_start": 19121.009765625,
            "bin_end": 20718.0646484375,
            "count": 250
           },
           {
            "bin_start": 20718.0646484375,
            "bin_end": 22315.11953125,
            "count": 695
           },
           {
            "bin_start": 22315.11953125,
            "bin_end": 23912.1744140625,
            "count": 415
           },
           {
            "bin_start": 23912.1744140625,
            "bin_end": 25509.229296875,
            "count": 1205
           },
           {
            "bin_start": 25509.229296875,
            "bin_end": 27106.2841796875,
            "count": 1415
           },
           {
            "bin_start": 27106.2841796875,
            "bin_end": 28703.3390625,
            "count": 670
           },
           {
            "bin_start": 28703.3390625,
            "bin_end": 30300.3939453125,
            "count": 340
           },
           {
            "bin_start": 30300.3939453125,
            "bin_end": 31897.448828125,
            "count": 250
           },
           {
            "bin_start": 31897.448828125,
            "bin_end": 33494.5037109375,
            "count": 105
           },
           {
            "bin_start": 33494.5037109375,
            "bin_end": 35091.55859375,
            "count": 185
           }
          ]
         }
        },
        {
         "name": "_deepnote_index_column",
         "dtype": "int64"
        }
       ],
       "rows_top": [
        {
         "Date": "2017-01-03",
         "open": 22.600000381469727,
         "high": 22.68000030517578,
         "low": 22.200000762939453,
         "close": 22.530000686645508,
         "adjclose": 20.63599967956543,
         "volume": 99298100,
         "ticker": "BAC",
         "S&P500": 2263.8798828125,
         "DowJones": 19938.529296875,
         "_deepnote_index_column": 0
        },
        {
         "Date": "2017-01-04",
         "open": 22.719999313354492,
         "high": 22.959999084472656,
         "low": 22.600000381469727,
         "close": 22.950000762939453,
         "adjclose": 21.02069664001465,
         "volume": 76875100,
         "ticker": "BAC",
         "S&P500": 2272.820068359375,
         "DowJones": 19956.140625,
         "_deepnote_index_column": 1
        },
        {
         "Date": "2017-01-05",
         "open": 22.81999969482422,
         "high": 22.93000030517578,
         "low": 22.350000381469727,
         "close": 22.68000030517578,
         "adjclose": 20.773387908935547,
         "volume": 86826400,
         "ticker": "BAC",
         "S&P500": 2271.5,
         "DowJones": 19948.599609375,
         "_deepnote_index_column": 2
        },
        {
         "Date": "2017-01-06",
         "open": 22.780000686645508,
         "high": 22.850000381469727,
         "low": 22.559999465942383,
         "close": 22.68000030517578,
         "adjclose": 20.773387908935547,
         "volume": 66281500,
         "ticker": "BAC",
         "S&P500": 2282.10009765625,
         "DowJones": 19999.630859375,
         "_deepnote_index_column": 3
        },
        {
         "Date": "2017-01-09",
         "open": 22.510000228881836,
         "high": 22.709999084472656,
         "low": 22.399999618530273,
         "close": 22.549999237060547,
         "adjclose": 20.65431785583496,
         "volume": 75901500,
         "ticker": "BAC",
         "S&P500": 2275.489990234375,
         "DowJones": 19943.779296875,
         "_deepnote_index_column": 4
        },
        {
         "Date": "2017-01-10",
         "open": 22.59000015258789,
         "high": 23.139999389648438,
         "low": 22.540000915527344,
         "close": 22.940000534057617,
         "adjclose": 21.011533737182617,
         "volume": 100977700,
         "ticker": "BAC",
         "S&P500": 2279.27001953125,
         "DowJones": 19957.119140625,
         "_deepnote_index_column": 5
        },
        {
         "Date": "2017-01-11",
         "open": 22.940000534057617,
         "high": 23.06999969482422,
         "low": 22.719999313354492,
         "close": 23.06999969482422,
         "adjclose": 21.130605697631836,
         "volume": 92385600,
         "ticker": "BAC",
         "S&P500": 2275.320068359375,
         "DowJones": 19973.419921875,
         "_deepnote_index_column": 6
        },
        {
         "Date": "2017-01-12",
         "open": 23.010000228881836,
         "high": 23.1200008392334,
         "low": 22.610000610351562,
         "close": 22.920000076293945,
         "adjclose": 20.993213653564453,
         "volume": 120474200,
         "ticker": "BAC",
         "S&P500": 2271.780029296875,
         "DowJones": 19929.2890625,
         "_deepnote_index_column": 7
        },
        {
         "Date": "2017-01-13",
         "open": 23.209999084472656,
         "high": 23.40999984741211,
         "low": 22.799999237060547,
         "close": 23.010000228881836,
         "adjclose": 21.07564926147461,
         "volume": 161930900,
         "ticker": "BAC",
         "S&P500": 2278.679931640625,
         "DowJones": 19952.029296875,
         "_deepnote_index_column": 8
        },
        {
         "Date": "2017-01-17",
         "open": 22.68000030517578,
         "high": 22.790000915527344,
         "low": 22.010000228881836,
         "close": 22.049999237060547,
         "adjclose": 20.196352005004883,
         "volume": 152495900,
         "ticker": "BAC",
         "S&P500": 2272.080078125,
         "DowJones": 19882.990234375,
         "_deepnote_index_column": 9
        },
        {
         "Date": "2017-01-18",
         "open": 22.299999237060547,
         "high": 22.649999618530273,
         "low": 22.100000381469727,
         "close": 22.6299991607666,
         "adjclose": 20.727588653564453,
         "volume": 124366000,
         "ticker": "BAC",
         "S&P500": 2272.010009765625,
         "DowJones": 19828.19921875,
         "_deepnote_index_column": 10
        },
        {
         "Date": "2017-01-19",
         "open": 22.729999542236328,
         "high": 22.809999465942383,
         "low": 22.40999984741211,
         "close": 22.530000686645508,
         "adjclose": 20.63599967956543,
         "volume": 75990800,
         "ticker": "BAC",
         "S&P500": 2274.330078125,
         "DowJones": 19824.140625,
         "_deepnote_index_column": 11
        },
        {
         "Date": "2017-01-20",
         "open": 22.65999984741211,
         "high": 22.93000030517578,
         "low": 22.520000457763672,
         "close": 22.639999389648438,
         "adjclose": 20.736751556396484,
         "volume": 102564900,
         "ticker": "BAC",
         "S&P500": 2276.9599609375,
         "DowJones": 19843.939453125,
         "_deepnote_index_column": 12
        },
        {
         "Date": "2017-01-23",
         "open": 22.6200008392334,
         "high": 22.760000228881836,
         "low": 22.420000076293945,
         "close": 22.559999465942383,
         "adjclose": 20.663476943969727,
         "volume": 61385600,
         "ticker": "BAC",
         "S&P500": 2271.780029296875,
         "DowJones": 19833.98046875,
         "_deepnote_index_column": 13
        },
        {
         "Date": "2017-01-24",
         "open": 22.610000610351562,
         "high": 23.100000381469727,
         "low": 22.479999542236328,
         "close": 22.950000762939453,
         "adjclose": 21.02069664001465,
         "volume": 98508700,
         "ticker": "BAC",
         "S&P500": 2284.6298828125,
         "DowJones": 19949.240234375,
         "_deepnote_index_column": 14
        },
        {
         "Date": "2017-01-25",
         "open": 23.31999969482422,
         "high": 23.420000076293945,
         "low": 23.100000381469727,
         "close": 23.3700008392334,
         "adjclose": 21.40538787841797,
         "volume": 99753300,
         "ticker": "BAC",
         "S&P500": 2299.550048828125,
         "DowJones": 20082,
         "_deepnote_index_column": 15
        },
        {
         "Date": "2017-01-26",
         "open": 23.40999984741211,
         "high": 23.549999237060547,
         "low": 23.280000686645508,
         "close": 23.440000534057617,
         "adjclose": 21.469499588012695,
         "volume": 84146400,
         "ticker": "BAC",
         "S&P500": 2300.989990234375,
         "DowJones": 20125.580078125,
         "_deepnote_index_column": 16
        },
        {
         "Date": "2017-01-27",
         "open": 23.43000030517578,
         "high": 23.450000762939453,
         "low": 23.280000686645508,
         "close": 23.360000610351562,
         "adjclose": 21.396224975585938,
         "volume": 54590200,
         "ticker": "BAC",
         "S&P500": 2299.02001953125,
         "DowJones": 20115.970703125,
         "_deepnote_index_column": 17
        },
        {
         "Date": "2017-01-30",
         "open": 23.200000762939453,
         "high": 23.200000762939453,
         "low": 22.709999084472656,
         "close": 22.950000762939453,
         "adjclose": 21.02069664001465,
         "volume": 91561200,
         "ticker": "BAC",
         "S&P500": 2286.010009765625,
         "DowJones": 20028.619140625,
         "_deepnote_index_column": 18
        },
        {
         "Date": "2017-01-31",
         "open": 22.770000457763672,
         "high": 23.030000686645508,
         "low": 22.5,
         "close": 22.639999389648438,
         "adjclose": 20.736751556396484,
         "volume": 91044300,
         "ticker": "BAC",
         "S&P500": 2279.090087890625,
         "DowJones": 19918.169921875,
         "_deepnote_index_column": 19
        },
        {
         "Date": "2017-02-01",
         "open": 22.969999313354492,
         "high": 23.219999313354492,
         "low": 22.81999969482422,
         "close": 22.889999389648438,
         "adjclose": 20.965736389160156,
         "volume": 103630900,
         "ticker": "BAC",
         "S&P500": 2289.139892578125,
         "DowJones": 19967.73046875,
         "_deepnote_index_column": 20
        },
        {
         "Date": "2017-02-02",
         "open": 22.739999771118164,
         "high": 22.790000915527344,
         "low": 22.510000228881836,
         "close": 22.719999313354492,
         "adjclose": 20.810028076171875,
         "volume": 88679100,
         "ticker": "BAC",
         "S&P500": 2283.969970703125,
         "DowJones": 19922.75,
         "_deepnote_index_column": 21
        },
        {
         "Date": "2017-02-03",
         "open": 23.149999618530273,
         "high": 23.350000381469727,
         "low": 22.950000762939453,
         "close": 23.290000915527344,
         "adjclose": 21.332111358642578,
         "volume": 116035100,
         "ticker": "BAC",
         "S&P500": 2298.31005859375,
         "DowJones": 20081.48046875,
         "_deepnote_index_column": 22
        },
        {
         "Date": "2017-02-06",
         "open": 23.149999618530273,
         "high": 23.3799991607666,
         "low": 23.06999969482422,
         "close": 23.1200008392334,
         "adjclose": 21.17640495300293,
         "volume": 92228400,
         "ticker": "BAC",
         "S&P500": 2296.179931640625,
         "DowJones": 20094.94921875,
         "_deepnote_index_column": 23
        },
        {
         "Date": "2017-02-07",
         "open": 23.280000686645508,
         "high": 23.290000915527344,
         "low": 22.860000610351562,
         "close": 22.899999618530273,
         "adjclose": 20.974895477294922,
         "volume": 87982900,
         "ticker": "BAC",
         "S&P500": 2299.39990234375,
         "DowJones": 20155.349609375,
         "_deepnote_index_column": 24
        },
        {
         "Date": "2017-02-08",
         "open": 22.729999542236328,
         "high": 22.729999542236328,
         "low": 22.450000762939453,
         "close": 22.670000076293945,
         "adjclose": 20.764230728149414,
         "volume": 102264500,
         "ticker": "BAC",
         "S&P500": 2295.909912109375,
         "DowJones": 20068.279296875,
         "_deepnote_index_column": 25
        },
        {
         "Date": "2017-02-09",
         "open": 22.760000228881836,
         "high": 23.149999618530273,
         "low": 22.639999389648438,
         "close": 23.1200008392334,
         "adjclose": 21.17640495300293,
         "volume": 102634200,
         "ticker": "BAC",
         "S&P500": 2311.080078125,
         "DowJones": 20206.359375,
         "_deepnote_index_column": 26
        },
        {
         "Date": "2017-02-10",
         "open": 23.190000534057617,
         "high": 23.239999771118164,
         "low": 22.959999084472656,
         "close": 23.079999923706055,
         "adjclose": 21.1397647857666,
         "volume": 90548300,
         "ticker": "BAC",
         "S&P500": 2319.22998046875,
         "DowJones": 20298.2109375,
         "_deepnote_index_column": 27
        },
        {
         "Date": "2017-02-13",
         "open": 23.170000076293945,
         "high": 23.540000915527344,
         "low": 23.170000076293945,
         "close": 23.399999618530273,
         "adjclose": 21.432863235473633,
         "volume": 105342500,
         "ticker": "BAC",
         "S&P500": 2331.580078125,
         "DowJones": 20441.48046875,
         "_deepnote_index_column": 28
        },
        {
         "Date": "2017-02-14",
         "open": 23.399999618530273,
         "high": 24.170000076293945,
         "low": 23.329999923706055,
         "close": 24.059999465942383,
         "adjclose": 22.037378311157227,
         "volume": 139711400,
         "ticker": "BAC",
         "S&P500": 2337.580078125,
         "DowJones": 20504.41015625,
         "_deepnote_index_column": 29
        },
        {
         "Date": "2017-02-15",
         "open": 24.34000015258789,
         "high": 24.770000457763672,
         "low": 24.110000610351562,
         "close": 24.579999923706055,
         "adjclose": 22.51366424560547,
         "volume": 151233300,
         "ticker": "BAC",
         "S&P500": 2351.300048828125,
         "DowJones": 20620.44921875,
         "_deepnote_index_column": 30
        },
        {
         "Date": "2017-02-16",
         "open": 24.540000915527344,
         "high": 24.6200008392334,
         "low": 24.299999237060547,
         "close": 24.579999923706055,
         "adjclose": 22.51366424560547,
         "volume": 98144500,
         "ticker": "BAC",
         "S&P500": 2351.31005859375,
         "DowJones": 20639.869140625,
         "_deepnote_index_column": 31
        },
        {
         "Date": "2017-02-17",
         "open": 24.280000686645508,
         "high": 24.579999923706055,
         "low": 24.200000762939453,
         "close": 24.520000457763672,
         "adjclose": 22.458709716796875,
         "volume": 85789200,
         "ticker": "BAC",
         "S&P500": 2351.159912109375,
         "DowJones": 20624.05078125,
         "_deepnote_index_column": 32
        },
        {
         "Date": "2017-02-21",
         "open": 24.59000015258789,
         "high": 24.799999237060547,
         "low": 24.579999923706055,
         "close": 24.780000686645508,
         "adjclose": 22.696857452392578,
         "volume": 78571500,
         "ticker": "BAC",
         "S&P500": 2366.7099609375,
         "DowJones": 20757.640625,
         "_deepnote_index_column": 33
        },
        {
         "Date": "2017-02-22",
         "open": 24.610000610351562,
         "high": 24.950000762939453,
         "low": 24.540000915527344,
         "close": 24.790000915527344,
         "adjclose": 22.706010818481445,
         "volume": 81531900,
         "ticker": "BAC",
         "S&P500": 2365.1298828125,
         "DowJones": 20781.58984375,
         "_deepnote_index_column": 34
        },
        {
         "Date": "2017-02-23",
         "open": 24.790000915527344,
         "high": 24.889999389648438,
         "low": 24.510000228881836,
         "close": 24.579999923706055,
         "adjclose": 22.51366424560547,
         "volume": 85846000,
         "ticker": "BAC",
         "S&P500": 2368.260009765625,
         "DowJones": 20840.69921875,
         "_deepnote_index_column": 35
        },
        {
         "Date": "2017-02-24",
         "open": 24.1200008392334,
         "high": 24.350000381469727,
         "low": 24.020000457763672,
         "close": 24.229999542236328,
         "adjclose": 22.193090438842773,
         "volume": 97074400,
         "ticker": "BAC",
         "S&P500": 2367.340087890625,
         "DowJones": 20821.759765625,
         "_deepnote_index_column": 36
        },
        {
         "Date": "2017-02-27",
         "open": 24.200000762939453,
         "high": 24.65999984741211,
         "low": 24.190000534057617,
         "close": 24.56999969482422,
         "adjclose": 22.504505157470703,
         "volume": 69129100,
         "ticker": "BAC",
         "S&P500": 2371.5400390625,
         "DowJones": 20851.330078125,
         "_deepnote_index_column": 37
        },
        {
         "Date": "2017-02-28",
         "open": 24.479999542236328,
         "high": 24.700000762939453,
         "low": 24.420000076293945,
         "close": 24.68000030517578,
         "adjclose": 22.605260848999023,
         "volume": 90242000,
         "ticker": "BAC",
         "S&P500": 2367.7900390625,
         "DowJones": 20841.240234375,
         "_deepnote_index_column": 38
        },
        {
         "Date": "2017-03-01",
         "open": 25.3700008392334,
         "high": 25.610000610351562,
         "low": 25.219999313354492,
         "close": 25.5,
         "adjclose": 23.427518844604492,
         "volume": 143947500,
         "ticker": "BAC",
         "S&P500": 2400.97998046875,
         "DowJones": 21169.109375,
         "_deepnote_index_column": 39
        },
        {
         "Date": "2017-03-02",
         "open": 25.68000030517578,
         "high": 25.799999237060547,
         "low": 25.200000762939453,
         "close": 25.229999542236328,
         "adjclose": 23.179460525512695,
         "volume": 99824600,
         "ticker": "BAC",
         "S&P500": 2394.75,
         "DowJones": 21129.19921875,
         "_deepnote_index_column": 40
        },
        {
         "Date": "2017-03-03",
         "open": 25.299999237060547,
         "high": 25.649999618530273,
         "low": 25.299999237060547,
         "close": 25.440000534057617,
         "adjclose": 23.372394561767578,
         "volume": 92456100,
         "ticker": "BAC",
         "S&P500": 2383.889892578125,
         "DowJones": 21039.9609375,
         "_deepnote_index_column": 41
        },
        {
         "Date": "2017-03-06",
         "open": 25.329999923706055,
         "high": 25.350000381469727,
         "low": 25.079999923706055,
         "close": 25.25,
         "adjclose": 23.19783592224121,
         "volume": 75660400,
         "ticker": "BAC",
         "S&P500": 2378.800048828125,
         "DowJones": 20986.4296875,
         "_deepnote_index_column": 42
        },
        {
         "Date": "2017-03-07",
         "open": 25.219999313354492,
         "high": 25.360000610351562,
         "low": 25.100000381469727,
         "close": 25.209999084472656,
         "adjclose": 23.16108512878418,
         "volume": 64053700,
         "ticker": "BAC",
         "S&P500": 2375.1201171875,
         "DowJones": 20970.5390625,
         "_deepnote_index_column": 43
        },
        {
         "Date": "2017-03-08",
         "open": 25.600000381469727,
         "high": 25.770000457763672,
         "low": 25.219999313354492,
         "close": 25.260000228881836,
         "adjclose": 23.2070255279541,
         "volume": 105314600,
         "ticker": "BAC",
         "S&P500": 2373.090087890625,
         "DowJones": 20951.439453125,
         "_deepnote_index_column": 44
        },
        {
         "Date": "2017-03-09",
         "open": 25.350000381469727,
         "high": 25.530000686645508,
         "low": 25.229999542236328,
         "close": 25.350000381469727,
         "adjclose": 23.289709091186523,
         "volume": 78984600,
         "ticker": "BAC",
         "S&P500": 2369.080078125,
         "DowJones": 20900.5703125,
         "_deepnote_index_column": 45
        },
        {
         "Date": "2017-03-10",
         "open": 25.6200008392334,
         "high": 25.6200008392334,
         "low": 25.09000015258789,
         "close": 25.309999465942383,
         "adjclose": 23.252960205078125,
         "volume": 86998800,
         "ticker": "BAC",
         "S&P500": 2376.860107421875,
         "DowJones": 20940.2890625,
         "_deepnote_index_column": 46
        },
        {
         "Date": "2017-03-13",
         "open": 25.299999237060547,
         "high": 25.40999984741211,
         "low": 25.1299991607666,
         "close": 25.299999237060547,
         "adjclose": 23.243772506713867,
         "volume": 56886200,
         "ticker": "BAC",
         "S&P500": 2374.419921875,
         "DowJones": 20926.060546875,
         "_deepnote_index_column": 47
        },
        {
         "Date": "2017-03-14",
         "open": 25.190000534057617,
         "high": 25.34000015258789,
         "low": 25.049999237060547,
         "close": 25.31999969482422,
         "adjclose": 23.26215171813965,
         "volume": 63182700,
         "ticker": "BAC",
         "S&P500": 2368.550048828125,
         "DowJones": 20874,
         "_deepnote_index_column": 48
        },
        {
         "Date": "2017-03-15",
         "open": 25.389999389648438,
         "high": 25.549999237060547,
         "low": 24.959999084472656,
         "close": 25.18000030517578,
         "adjclose": 23.133525848388672,
         "volume": 114662700,
         "ticker": "BAC",
         "S&P500": 2390.010009765625,
         "DowJones": 20977.470703125,
         "_deepnote_index_column": 49
        }
       ],
       "rows_bottom": [
        {
         "Date": "2021-03-16",
         "open": 35.470001220703125,
         "high": 35.86000061035156,
         "low": 35.310001373291016,
         "close": 35.83000183105469,
         "adjclose": 35.48039627075195,
         "volume": 25022400,
         "ticker": "PFE",
         "S&P500": 3981.0400390625,
         "DowJones": 32966.75,
         "_deepnote_index_column": 5480
        },
        {
         "Date": "2021-03-17",
         "open": 35.83000183105469,
         "high": 35.959999084472656,
         "low": 35.119998931884766,
         "close": 35.790000915527344,
         "adjclose": 35.4407844543457,
         "volume": 42540100,
         "ticker": "PFE",
         "S&P500": 3983.8701171875,
         "DowJones": 33047.578125,
         "_deepnote_index_column": 5481
        },
        {
         "Date": "2021-03-18",
         "open": 35.529998779296875,
         "high": 35.970001220703125,
         "low": 35.52000045776367,
         "close": 35.77000045776367,
         "adjclose": 35.42097854614258,
         "volume": 24729800,
         "ticker": "PFE",
         "S&P500": 3969.6201171875,
         "DowJones": 33227.78125,
         "_deepnote_index_column": 5482
        },
        {
         "Date": "2021-03-19",
         "open": 35.75,
         "high": 35.81999969482422,
         "low": 35.470001220703125,
         "close": 35.529998779296875,
         "adjclose": 35.183319091796875,
         "volume": 48348900,
         "ticker": "PFE",
         "S&P500": 3930.1201171875,
         "DowJones": 32858.359375,
         "_deepnote_index_column": 5483
        },
        {
         "Date": "2021-03-22",
         "open": 35.47999954223633,
         "high": 36.0099983215332,
         "low": 35.36000061035156,
         "close": 36,
         "adjclose": 35.64873504638672,
         "volume": 25427500,
         "ticker": "PFE",
         "S&P500": 3955.31005859375,
         "DowJones": 32810.3515625,
         "_deepnote_index_column": 5484
        },
        {
         "Date": "2021-03-23",
         "open": 35.81999969482422,
         "high": 35.93000030517578,
         "low": 35.31999969482422,
         "close": 35.36000061035156,
         "adjclose": 35.01498031616211,
         "volume": 27970500,
         "ticker": "PFE",
         "S&P500": 3949.1298828125,
         "DowJones": 32753.76953125,
         "_deepnote_index_column": 5485
        },
        {
         "Date": "2021-03-24",
         "open": 35.47999954223633,
         "high": 35.93000030517578,
         "low": 35.369998931884766,
         "close": 35.61000061035156,
         "adjclose": 35.262542724609375,
         "volume": 22883400,
         "ticker": "PFE",
         "S&P500": 3942.080078125,
         "DowJones": 32787.98828125,
         "_deepnote_index_column": 5486
        },
        {
         "Date": "2021-03-25",
         "open": 35.650001525878906,
         "high": 35.790000915527344,
         "low": 35.25,
         "close": 35.66999816894531,
         "adjclose": 35.32195281982422,
         "volume": 24875300,
         "ticker": "PFE",
         "S&P500": 3919.5400390625,
         "DowJones": 32672.689453125,
         "_deepnote_index_column": 5487
        },
        {
         "Date": "2021-03-26",
         "open": 35.68000030517578,
         "high": 36.290000915527344,
         "low": 35.63999938964844,
         "close": 36.25,
         "adjclose": 35.896297454833984,
         "volume": 27944500,
         "ticker": "PFE",
         "S&P500": 3978.18994140625,
         "DowJones": 33098.828125,
         "_deepnote_index_column": 5488
        },
        {
         "Date": "2021-03-29",
         "open": 36.029998779296875,
         "high": 36.7400016784668,
         "low": 35.900001525878906,
         "close": 36.619998931884766,
         "adjclose": 36.2626838684082,
         "volume": 27004800,
         "ticker": "PFE",
         "S&P500": 3981.830078125,
         "DowJones": 33259,
         "_deepnote_index_column": 5489
        },
        {
         "Date": "2021-03-30",
         "open": 36.59000015258789,
         "high": 36.630001068115234,
         "low": 36.02000045776367,
         "close": 36.11000061035156,
         "adjclose": 35.75766372680664,
         "volume": 26303300,
         "ticker": "PFE",
         "S&P500": 3968.010009765625,
         "DowJones": 33170.9296875,
         "_deepnote_index_column": 5490
        },
        {
         "Date": "2021-03-31",
         "open": 36.150001525878906,
         "high": 36.43000030517578,
         "low": 36.040000915527344,
         "close": 36.22999954223633,
         "adjclose": 35.87649154663086,
         "volume": 26582700,
         "ticker": "PFE",
         "S&P500": 3994.409912109375,
         "DowJones": 33173.76953125,
         "_deepnote_index_column": 5491
        },
        {
         "Date": "2021-04-01",
         "open": 36.29999923706055,
         "high": 36.45000076293945,
         "low": 36.02000045776367,
         "close": 36.29999923706055,
         "adjclose": 35.94580841064453,
         "volume": 21319900,
         "ticker": "PFE",
         "S&P500": 4020.6298828125,
         "DowJones": 33167.171875,
         "_deepnote_index_column": 5492
        },
        {
         "Date": "2021-04-05",
         "open": 36.439998626708984,
         "high": 36.56999969482422,
         "low": 36.099998474121094,
         "close": 36.279998779296875,
         "adjclose": 35.926002502441406,
         "volume": 22096900,
         "ticker": "PFE",
         "S&P500": 4083.419921875,
         "DowJones": 33617.94921875,
         "_deepnote_index_column": 5493
        },
        {
         "Date": "2021-04-06",
         "open": 36.2599983215332,
         "high": 36.400001525878906,
         "low": 36,
         "close": 36.04999923706055,
         "adjclose": 35.698246002197266,
         "volume": 20722900,
         "ticker": "PFE",
         "S&P500": 4086.22998046875,
         "DowJones": 33544.7890625,
         "_deepnote_index_column": 5494
        },
        {
         "Date": "2021-04-07",
         "open": 36.029998779296875,
         "high": 36.2400016784668,
         "low": 35.7599983215332,
         "close": 35.90999984741211,
         "adjclose": 35.55961227416992,
         "volume": 21933800,
         "ticker": "PFE",
         "S&P500": 4083.1298828125,
         "DowJones": 33521.76171875,
         "_deepnote_index_column": 5495
        },
        {
         "Date": "2021-04-08",
         "open": 35.959999084472656,
         "high": 36.150001525878906,
         "low": 35.869998931884766,
         "close": 35.959999084472656,
         "adjclose": 35.609127044677734,
         "volume": 18129400,
         "ticker": "PFE",
         "S&P500": 4098.18994140625,
         "DowJones": 33506.80078125,
         "_deepnote_index_column": 5496
        },
        {
         "Date": "2021-04-09",
         "open": 35.900001525878906,
         "high": 36.810001373291016,
         "low": 35.900001525878906,
         "close": 36.599998474121094,
         "adjclose": 36.24287796020508,
         "volume": 31686700,
         "ticker": "PFE",
         "S&P500": 4129.47998046875,
         "DowJones": 33810.87109375,
         "_deepnote_index_column": 5497
        },
        {
         "Date": "2021-04-12",
         "open": 36.47999954223633,
         "high": 37.029998779296875,
         "low": 36.33000183105469,
         "close": 36.970001220703125,
         "adjclose": 36.60927200317383,
         "volume": 29944900,
         "ticker": "PFE",
         "S&P500": 4131.759765625,
         "DowJones": 33786.19140625,
         "_deepnote_index_column": 5498
        },
        {
         "Date": "2021-04-13",
         "open": 37.40999984741211,
         "high": 37.650001525878906,
         "low": 36.88999938964844,
         "close": 37.15999984741211,
         "adjclose": 36.79741668701172,
         "volume": 33967400,
         "ticker": "PFE",
         "S&P500": 4148,
         "DowJones": 33741.640625,
         "_deepnote_index_column": 5499
        },
        {
         "Date": "2021-04-14",
         "open": 37.16999816894531,
         "high": 37.380001068115234,
         "low": 36.959999084472656,
         "close": 37.16999816894531,
         "adjclose": 36.80731964111328,
         "volume": 23842900,
         "ticker": "PFE",
         "S&P500": 4151.68994140625,
         "DowJones": 33911.25,
         "_deepnote_index_column": 5500
        },
        {
         "Date": "2021-04-15",
         "open": 37.2599983215332,
         "high": 37.7400016784668,
         "low": 37.2599983215332,
         "close": 37.599998474121094,
         "adjclose": 37.233123779296875,
         "volume": 24945800,
         "ticker": "PFE",
         "S&P500": 4173.490234375,
         "DowJones": 34068.73046875,
         "_deepnote_index_column": 5501
        },
        {
         "Date": "2021-04-16",
         "open": 37.869998931884766,
         "high": 38.70000076293945,
         "low": 37.810001373291016,
         "close": 38.56999969482422,
         "adjclose": 38.193660736083984,
         "volume": 52829500,
         "ticker": "PFE",
         "S&P500": 4191.31005859375,
         "DowJones": 34256.75,
         "_deepnote_index_column": 5502
        },
        {
         "Date": "2021-04-19",
         "open": 38.599998474121094,
         "high": 38.959999084472656,
         "low": 38.33000183105469,
         "close": 38.93000030517578,
         "adjclose": 38.550148010253906,
         "volume": 30905100,
         "ticker": "PFE",
         "S&P500": 4180.81005859375,
         "DowJones": 34182.37890625,
         "_deepnote_index_column": 5503
        },
        {
         "Date": "2021-04-20",
         "open": 38.75,
         "high": 39.2400016784668,
         "low": 38.75,
         "close": 39.029998779296875,
         "adjclose": 38.649169921875,
         "volume": 26459400,
         "ticker": "PFE",
         "S&P500": 4159.18017578125,
         "DowJones": 34034.1796875,
         "_deepnote_index_column": 5504
        },
        {
         "Date": "2021-04-21",
         "open": 39.13999938964844,
         "high": 39.66999816894531,
         "low": 39.130001068115234,
         "close": 39.529998779296875,
         "adjclose": 39.144290924072266,
         "volume": 29365000,
         "ticker": "PFE",
         "S&P500": 4175.02001953125,
         "DowJones": 34160.33984375,
         "_deepnote_index_column": 5505
        },
        {
         "Date": "2021-04-22",
         "open": 39.47999954223633,
         "high": 39.5,
         "low": 38.52000045776367,
         "close": 38.63999938964844,
         "adjclose": 38.262977600097656,
         "volume": 33373600,
         "ticker": "PFE",
         "S&P500": 4179.56982421875,
         "DowJones": 34126.5703125,
         "_deepnote_index_column": 5506
        },
        {
         "Date": "2021-04-23",
         "open": 38.630001068115234,
         "high": 38.83000183105469,
         "low": 38.43000030517578,
         "close": 38.65999984741211,
         "adjclose": 38.282779693603516,
         "volume": 24375000,
         "ticker": "PFE",
         "S&P500": 4194.169921875,
         "DowJones": 34157.5703125,
         "_deepnote_index_column": 5507
        },
        {
         "Date": "2021-04-26",
         "open": 38.72999954223633,
         "high": 38.7400016784668,
         "low": 38.4900016784668,
         "close": 38.68000030517578,
         "adjclose": 38.30258560180664,
         "volume": 19773400,
         "ticker": "PFE",
         "S&P500": 4194.18994140625,
         "DowJones": 34148.94140625,
         "_deepnote_index_column": 5508
        },
        {
         "Date": "2021-04-27",
         "open": 38.5099983215332,
         "high": 38.61000061035156,
         "low": 38.349998474121094,
         "close": 38.45000076293945,
         "adjclose": 38.074832916259766,
         "volume": 19061500,
         "ticker": "PFE",
         "S&P500": 4193.35009765625,
         "DowJones": 34043.98046875,
         "_deepnote_index_column": 5509
        },
        {
         "Date": "2021-04-28",
         "open": 38.540000915527344,
         "high": 38.939998626708984,
         "low": 38.52000045776367,
         "close": 38.810001373291016,
         "adjclose": 38.43132019042969,
         "volume": 21963300,
         "ticker": "PFE",
         "S&P500": 4201.52978515625,
         "DowJones": 33946.6015625,
         "_deepnote_index_column": 5510
        },
        {
         "Date": "2021-04-29",
         "open": 38.9900016784668,
         "high": 39,
         "low": 38.310001373291016,
         "close": 38.599998474121094,
         "adjclose": 38.223365783691406,
         "volume": 23569400,
         "ticker": "PFE",
         "S&P500": 4218.77978515625,
         "DowJones": 34087.2109375,
         "_deepnote_index_column": 5511
        },
        {
         "Date": "2021-04-30",
         "open": 38.5,
         "high": 38.900001525878906,
         "low": 38.4900016784668,
         "close": 38.650001525878906,
         "adjclose": 38.27288055419922,
         "volume": 28403900,
         "ticker": "PFE",
         "S&P500": 4198.10009765625,
         "DowJones": 33988.75,
         "_deepnote_index_column": 5512
        },
        {
         "Date": "2021-05-03",
         "open": 39.040000915527344,
         "high": 39.84000015258789,
         "low": 38.959999084472656,
         "close": 39.83000183105469,
         "adjclose": 39.441368103027344,
         "volume": 46638600,
         "ticker": "PFE",
         "S&P500": 4209.39013671875,
         "DowJones": 34221.05859375,
         "_deepnote_index_column": 5513
        },
        {
         "Date": "2021-05-04",
         "open": 40,
         "high": 40.16999816894531,
         "low": 39.43000030517578,
         "close": 39.95000076293945,
         "adjclose": 39.56019592285156,
         "volume": 52802200,
         "ticker": "PFE",
         "S&P500": 4179.0400390625,
         "DowJones": 34147.78125,
         "_deepnote_index_column": 5514
        },
        {
         "Date": "2021-05-05",
         "open": 40.18000030517578,
         "high": 41.09000015258789,
         "low": 38.93000030517578,
         "close": 39.970001220703125,
         "adjclose": 39.58000183105469,
         "volume": 54348400,
         "ticker": "PFE",
         "S&P500": 4187.72021484375,
         "DowJones": 34331.19921875,
         "_deepnote_index_column": 5515
        },
        {
         "Date": "2021-05-06",
         "open": 38.47999954223633,
         "high": 39.22999954223633,
         "low": 37.959999084472656,
         "close": 39.189998626708984,
         "adjclose": 39.189998626708984,
         "volume": 54944900,
         "ticker": "PFE",
         "S&P500": 4202.7001953125,
         "DowJones": 34561.2890625,
         "_deepnote_index_column": 5516
        },
        {
         "Date": "2021-05-07",
         "open": 39.04999923706055,
         "high": 39.869998931884766,
         "low": 39.04999923706055,
         "close": 39.58000183105469,
         "adjclose": 39.58000183105469,
         "volume": 33795200,
         "ticker": "PFE",
         "S&P500": 4238.0400390625,
         "DowJones": 34811.390625,
         "_deepnote_index_column": 5517
        },
        {
         "Date": "2021-05-10",
         "open": 39.83000183105469,
         "high": 40.279998779296875,
         "low": 39.779998779296875,
         "close": 39.86000061035156,
         "adjclose": 39.86000061035156,
         "volume": 30831900,
         "ticker": "PFE",
         "S&P500": 4236.39013671875,
         "DowJones": 35091.55859375,
         "_deepnote_index_column": 5518
        },
        {
         "Date": "2021-05-11",
         "open": 39.68000030517578,
         "high": 40.06999969482422,
         "low": 39.22999954223633,
         "close": 39.349998474121094,
         "adjclose": 39.349998474121094,
         "volume": 30568600,
         "ticker": "PFE",
         "S&P500": 4162.0400390625,
         "DowJones": 34572.73828125,
         "_deepnote_index_column": 5519
        },
        {
         "Date": "2021-05-12",
         "open": 39.439998626708984,
         "high": 39.91999816894531,
         "low": 39.310001373291016,
         "close": 39.689998626708984,
         "adjclose": 39.689998626708984,
         "volume": 26208600,
         "ticker": "PFE",
         "S&P500": 4134.72998046875,
         "DowJones": 34207.87109375,
         "_deepnote_index_column": 5520
        },
        {
         "Date": "2021-05-13",
         "open": 39.5,
         "high": 40.279998779296875,
         "low": 39.5,
         "close": 40.099998474121094,
         "adjclose": 40.099998474121094,
         "volume": 25415000,
         "ticker": "PFE",
         "S&P500": 4131.580078125,
         "DowJones": 34181.76953125,
         "_deepnote_index_column": 5521
        },
        {
         "Date": "2021-05-14",
         "open": 40.2400016784668,
         "high": 40.31999969482422,
         "low": 39.91999816894531,
         "close": 40.02000045776367,
         "adjclose": 40.02000045776367,
         "volume": 18005400,
         "ticker": "PFE",
         "S&P500": 4183.1298828125,
         "DowJones": 34454.05078125,
         "_deepnote_index_column": 5522
        },
        {
         "Date": "2021-05-17",
         "open": 40.06999969482422,
         "high": 40.400001525878906,
         "low": 40.0099983215332,
         "close": 40.11000061035156,
         "adjclose": 40.11000061035156,
         "volume": 18095000,
         "ticker": "PFE",
         "S&P500": 4171.919921875,
         "DowJones": 34383.83984375,
         "_deepnote_index_column": 5523
        },
        {
         "Date": "2021-05-18",
         "open": 40.18000030517578,
         "high": 40.349998474121094,
         "low": 39.83000183105469,
         "close": 40.04999923706055,
         "adjclose": 40.04999923706055,
         "volume": 15805500,
         "ticker": "PFE",
         "S&P500": 4169.14990234375,
         "DowJones": 34408.98828125,
         "_deepnote_index_column": 5524
        },
        {
         "Date": "2021-05-19",
         "open": 39.900001525878906,
         "high": 39.900001525878906,
         "low": 39.43000030517578,
         "close": 39.83000183105469,
         "adjclose": 39.83000183105469,
         "volume": 20209500,
         "ticker": "PFE",
         "S&P500": 4116.93017578125,
         "DowJones": 33945.80859375,
         "_deepnote_index_column": 5525
        },
        {
         "Date": "2021-05-20",
         "open": 39.72999954223633,
         "high": 40.25,
         "low": 39.720001220703125,
         "close": 40.119998931884766,
         "adjclose": 40.119998931884766,
         "volume": 18621100,
         "ticker": "PFE",
         "S&P500": 4172.7998046875,
         "DowJones": 34233.3984375,
         "_deepnote_index_column": 5526
        },
        {
         "Date": "2021-05-21",
         "open": 40.209999084472656,
         "high": 40.599998474121094,
         "low": 39.90999984741211,
         "close": 39.95000076293945,
         "adjclose": 39.95000076293945,
         "volume": 21132100,
         "ticker": "PFE",
         "S&P500": 4188.72021484375,
         "DowJones": 34415.48046875,
         "_deepnote_index_column": 5527
        },
        {
         "Date": "2021-05-24",
         "open": 40.08000183105469,
         "high": 40.13999938964844,
         "low": 39.779998779296875,
         "close": 39.810001373291016,
         "adjclose": 39.810001373291016,
         "volume": 16911300,
         "ticker": "PFE",
         "S&P500": 4209.52001953125,
         "DowJones": 34472.51171875,
         "_deepnote_index_column": 5528
        },
        {
         "Date": "2021-05-25",
         "open": 39.81999969482422,
         "high": 39.85639953613281,
         "low": 39.42499923706055,
         "close": 39.435001373291016,
         "adjclose": 39.435001373291016,
         "volume": 10742274,
         "ticker": "PFE",
         "S&P500": 4213.419921875,
         "DowJones": 34511.3984375,
         "_deepnote_index_column": 5529
        }
       ]
      },
      "text/plain": "            Date       open       high        low      close   adjclose  \\\n0     2017-01-03  22.600000  22.680000  22.200001  22.530001  20.636000   \n1     2017-01-04  22.719999  22.959999  22.600000  22.950001  21.020697   \n2     2017-01-05  22.820000  22.930000  22.350000  22.680000  20.773388   \n3     2017-01-06  22.780001  22.850000  22.559999  22.680000  20.773388   \n4     2017-01-09  22.510000  22.709999  22.400000  22.549999  20.654318   \n...          ...        ...        ...        ...        ...        ...   \n5525  2021-05-19  39.900002  39.900002  39.430000  39.830002  39.830002   \n5526  2021-05-20  39.730000  40.250000  39.720001  40.119999  40.119999   \n5527  2021-05-21  40.209999  40.599998  39.910000  39.950001  39.950001   \n5528  2021-05-24  40.080002  40.139999  39.779999  39.810001  39.810001   \n5529  2021-05-25  39.820000  39.856400  39.424999  39.435001  39.435001   \n\n        volume ticker       S&P500      DowJones  \n0     99298100    BAC  2263.879883  19938.529297  \n1     76875100    BAC  2272.820068  19956.140625  \n2     86826400    BAC  2271.500000  19948.599609  \n3     66281500    BAC  2282.100098  19999.630859  \n4     75901500    BAC  2275.489990  19943.779297  \n...        ...    ...          ...           ...  \n5525  20209500    PFE  4116.930176  33945.808594  \n5526  18621100    PFE  4172.799805  34233.398438  \n5527  21132100    PFE  4188.720215  34415.480469  \n5528  16911300    PFE  4209.520020  34472.511719  \n5529  10742274    PFE  4213.419922  34511.398438  \n\n[5530 rows x 10 columns]",
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>Date</th>\n      <th>open</th>\n      <th>high</th>\n      <th>low</th>\n      <th>close</th>\n      <th>adjclose</th>\n      <th>volume</th>\n      <th>ticker</th>\n      <th>S&amp;P500</th>\n      <th>DowJones</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>2017-01-03</td>\n      <td>22.600000</td>\n      <td>22.680000</td>\n      <td>22.200001</td>\n      <td>22.530001</td>\n      <td>20.636000</td>\n      <td>99298100</td>\n      <td>BAC</td>\n      <td>2263.879883</td>\n      <td>19938.529297</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2017-01-04</td>\n      <td>22.719999</td>\n      <td>22.959999</td>\n      <td>22.600000</td>\n      <td>22.950001</td>\n      <td>21.020697</td>\n      <td>76875100</td>\n      <td>BAC</td>\n      <td>2272.820068</td>\n      <td>19956.140625</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2017-01-05</td>\n      <td>22.820000</td>\n      <td>22.930000</td>\n      <td>22.350000</td>\n      <td>22.680000</td>\n      <td>20.773388</td>\n      <td>86826400</td>\n      <td>BAC</td>\n      <td>2271.500000</td>\n      <td>19948.599609</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>2017-01-06</td>\n      <td>22.780001</td>\n      <td>22.850000</td>\n      <td>22.559999</td>\n      <td>22.680000</td>\n      <td>20.773388</td>\n      <td>66281500</td>\n      <td>BAC</td>\n      <td>2282.100098</td>\n      <td>19999.630859</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>2017-01-09</td>\n      <td>22.510000</td>\n      <td>22.709999</td>\n      <td>22.400000</td>\n      <td>22.549999</td>\n      <td>20.654318</td>\n      <td>75901500</td>\n      <td>BAC</td>\n      <td>2275.489990</td>\n      <td>19943.779297</td>\n    </tr>\n    <tr>\n      <th>...</th>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <th>5525</th>\n      <td>2021-05-19</td>\n      <td>39.900002</td>\n      <td>39.900002</td>\n      <td>39.430000</td>\n      <td>39.830002</td>\n      <td>39.830002</td>\n      <td>20209500</td>\n      <td>PFE</td>\n      <td>4116.930176</td>\n      <td>33945.808594</td>\n    </tr>\n    <tr>\n      <th>5526</th>\n      <td>2021-05-20</td>\n      <td>39.730000</td>\n      <td>40.250000</td>\n      <td>39.720001</td>\n      <td>40.119999</td>\n      <td>40.119999</td>\n      <td>18621100</td>\n      <td>PFE</td>\n      <td>4172.799805</td>\n      <td>34233.398438</td>\n    </tr>\n    <tr>\n      <th>5527</th>\n      <td>2021-05-21</td>\n      <td>40.209999</td>\n      <td>40.599998</td>\n      <td>39.910000</td>\n      <td>39.950001</td>\n      <td>39.950001</td>\n      <td>21132100</td>\n      <td>PFE</td>\n      <td>4188.720215</td>\n      <td>34415.480469</td>\n    </tr>\n    <tr>\n      <th>5528</th>\n      <td>2021-05-24</td>\n      <td>40.080002</td>\n      <td>40.139999</td>\n      <td>39.779999</td>\n      <td>39.810001</td>\n      <td>39.810001</td>\n      <td>16911300</td>\n      <td>PFE</td>\n      <td>4209.520020</td>\n      <td>34472.511719</td>\n    </tr>\n    <tr>\n      <th>5529</th>\n      <td>2021-05-25</td>\n      <td>39.820000</td>\n      <td>39.856400</td>\n      <td>39.424999</td>\n      <td>39.435001</td>\n      <td>39.435001</td>\n      <td>10742274</td>\n      <td>PFE</td>\n      <td>4213.419922</td>\n      <td>34511.398438</td>\n    </tr>\n  </tbody>\n</table>\n<p>5530 rows × 10 columns</p>\n</div>"
     },
     "metadata": {}
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00000-5d30f703-9ffc-4771-9199-8fd6a7e53401",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "4f1c8fa7",
    "execution_start": 1621954330948,
    "execution_millis": 1582,
    "deepnote_cell_type": "code"
   },
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import numpy as np \n",
    "\n",
    "# read the data\n",
    "data = pd.read_csv(\"dataset 5-22-21.csv\")\n",
    "\n",
    "# get an overview of the data \n",
    "data.head()\n",
    "data.info()\n",
    "data.describe()\n",
    "\n",
    "# see if there are any NA's \n",
    "missings = pd.DataFrame(data.isna().sum())\n",
    "missings\n",
    "\n",
    "# We found no more missings."
   ],
   "execution_count": 3,
   "outputs": [
    {
     "name": "stdout",
     "text": "<class 'pandas.core.frame.DataFrame'>\nRangeIndex: 5520 entries, 0 to 5519\nData columns (total 11 columns):\n #   Column      Non-Null Count  Dtype  \n---  ------      --------------  -----  \n 0   Unnamed: 0  5520 non-null   int64  \n 1   Date        5520 non-null   object \n 2   open        5520 non-null   float64\n 3   high        5520 non-null   float64\n 4   low         5520 non-null   float64\n 5   close       5520 non-null   float64\n 6   adjclose    5520 non-null   float64\n 7   volume      5520 non-null   int64  \n 8   ticker      5520 non-null   object \n 9   S&P500      5520 non-null   float64\n 10  DowJones    5520 non-null   float64\ndtypes: float64(7), int64(2), object(2)\nmemory usage: 474.5+ KB\n",
     "output_type": "stream"
    },
    {
     "output_type": "execute_result",
     "execution_count": 3,
     "data": {
      "application/vnd.deepnote.dataframe.v2+json": {
       "row_count": 11,
       "column_count": 1,
       "columns": [
        {
         "name": 0,
         "dtype": "int64",
         "stats": {
          "unique_count": 1,
          "nan_count": 0,
          "min": "0",
          "max": "0",
          "histogram": [
           {
            "bin_start": -0.5,
            "bin_end": -0.4,
            "count": 0
           },
           {
            "bin_start": -0.4,
            "bin_end": -0.3,
            "count": 0
           },
           {
            "bin_start": -0.3,
            "bin_end": -0.19999999999999996,
            "count": 0
           },
           {
            "bin_start": -0.19999999999999996,
            "bin_end": -0.09999999999999998,
            "count": 0
           },
           {
            "bin_start": -0.09999999999999998,
            "bin_end": 0,
            "count": 0
           },
           {
            "bin_start": 0,
            "bin_end": 0.10000000000000009,
            "count": 11
           },
           {
            "bin_start": 0.10000000000000009,
            "bin_end": 0.20000000000000007,
            "count": 0
           },
           {
            "bin_start": 0.20000000000000007,
            "bin_end": 0.30000000000000004,
            "count": 0
           },
           {
            "bin_start": 0.30000000000000004,
            "bin_end": 0.4,
            "count": 0
           },
           {
            "bin_start": 0.4,
            "bin_end": 0.5,
            "count": 0
           }
          ]
         }
        },
        {
         "name": "_deepnote_index_column",
         "dtype": "object"
        }
       ],
       "rows_top": [
        {
         "0": 0,
         "_deepnote_index_column": "Unnamed: 0"
        },
        {
         "0": 0,
         "_deepnote_index_column": "Date"
        },
        {
         "0": 0,
         "_deepnote_index_column": "open"
        },
        {
         "0": 0,
         "_deepnote_index_column": "high"
        },
        {
         "0": 0,
         "_deepnote_index_column": "low"
        },
        {
         "0": 0,
         "_deepnote_index_column": "close"
        },
        {
         "0": 0,
         "_deepnote_index_column": "adjclose"
        },
        {
         "0": 0,
         "_deepnote_index_column": "volume"
        },
        {
         "0": 0,
         "_deepnote_index_column": "ticker"
        },
        {
         "0": 0,
         "_deepnote_index_column": "S&P500"
        },
        {
         "0": 0,
         "_deepnote_index_column": "DowJones"
        }
       ],
       "rows_bottom": null
      },
      "text/plain": "            0\nUnnamed: 0  0\nDate        0\nopen        0\nhigh        0\nlow         0\nclose       0\nadjclose    0\nvolume      0\nticker      0\nS&P500      0\nDowJones    0",
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>0</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Unnamed: 0</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>Date</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>open</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>high</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>low</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>close</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>adjclose</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>volume</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>ticker</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>S&amp;P500</th>\n      <td>0</td>\n    </tr>\n    <tr>\n      <th>DowJones</th>\n      <td>0</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {}
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Exploratory Data Analysis and Data Preprocessing (e.g. Scaling)"
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00005-11161a39-8596-470f-8251-e4cb78ac98fe",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00001-18f6e7eb-1770-414b-9b21-088e91732534",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "86a20ad3",
    "execution_start": 1621954332569,
    "execution_millis": 858,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# Visualize the original data\n",
    "stocks = data[['Date', 'open', 'high', 'low', 'close', 'ticker']]\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# reset the index\n",
    "stocks['Date'] = pd.to_datetime(stocks['Date'])\n",
    "stocks.set_index('Date')\n",
    "# sort the values by Date\n",
    "stocks.sort_values('Date', inplace=True)\n",
    "# set the color palette for the stocks\n",
    "palette ={\"BAC\": \"C0\", \"MDLZ\": \"C1\", \"GOOG\": \"C2\", \"BA\": \"k\", \"PFE\": \"r\"}\n",
    "# create the figure\n",
    "plt.figure(figsize=(8,4))\n",
    "sns.lineplot(x = 'Date', y = 'close', data = stocks, hue = 'ticker', palette = palette)"
   ],
   "execution_count": 4,
   "outputs": [
    {
     "output_type": "execute_result",
     "execution_count": 4,
     "data": {
      "text/plain": "<AxesSubplot:xlabel='Date', ylabel='close'>"
     },
     "metadata": {}
    },
    {
     "data": {
      "text/plain": "<Figure size 576x288 with 1 Axes>",
      "image/png": "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ww8/6KioKH3HHXfoTp06FUuAMjIy9Isvvugr69mzZ5nXW9HWrFmjV69e7Ve2Y8cOPX/+/HIvy+12608//dS3XY0bN/a9v+yyy8r1i71QTk6O7tGjh77iiiv0n3/+qbdv316m+fLz83Xr1q1L3Q9tNpu+++67da9evXTv3r195QcOHNC//fabHjhwoA4ODtYJCQnljl2cHSQpkKTgjPX6669rQPfu3bvEA3hqaqrfL92SeDweffToUf3BBx/4qplbtGihL7nkEn3DDTfo119/3VfFnpqaqvPy8vSbb755Sg3Eynsir2zJycm6Xr16vhPLvHnz9OLFi/Ull1zidyKKj4/3G05OTg506BWucD/o06ePXrly5Wkv61SkpKToH374QR88eFCnpaXpmTNn6i1btmitjQaP8+bNKzFReO2113zLSE1N1eHh4bpBgwantQ3izFURSYF0cywCat++fXz55ZesWrWKWrVqYTabOXr0KLNnzyY8PJx169bRqlWrQIdZIx05coSPPvqICy+8kF69evnK3W43y5YtY8CAAQCMHj2aSy+9FLfbzfXXXx+ocM96K1asYMKECTz11FO0bNmS5ORk2rdvj8l0rDuZCy64gGXLlrFjxw75XohiKqKbY0kKRJXTWnP48GHGjRvH119/DUBERITvb3h4OGFhYXz66ad07tw5gJGe2aZPn86jjz7KokWLaNOmTaDDEWXw559/0qdPHwDuvvtuPvjggwBHJKoTSQpOQJKCwPB4POTn5xMWFgYYPeEBBAUF4fF42Lx5Mx6Ph169evnG1apVi7lz59KvX7+AxX0201qXudMgEXgulwur1eobPhOP39XdH3/8QUhICF27dg10KMVURFIgPRqKMvF4PKxYsYK0tDRq166N2+3m999/Z+vWraSmppKTk+Prue6KK65g165d7N69G4/HQ7169Th06BAFBQV+y5w1axbXXHNNALZGFJKEoGaxWCx8/vnnfPnll/z2228sXbqUCy64INBhnTUcDgfnn3++bzg3N5fQ0FBWr17Nb7/9RlRUFLfddhvBwcF+yVtNIknBWSgnJ4fdu3fTunVrbDZbidNkZWURHh6OUopVq1Zx2223sW3btmLT1a5dm5YtW5KVleUrmzt3LhaLhZtvvpn09HRCQ0OJiIigdu3atG/fns6dO9OpU6dK2z4hzmSjRo2iR48etG/fnlmzZklSUIXWr1/vNxwWFkbr1q3ZsWOHr+y+++4jLi6OV155hVtvvZXExMQa1f5DLh+cZXJycmjXrh379+/HZrNhMplo1qwZtWvXxuVysXnzZiIiIjh48CC1atUiKysLj8dD/fr1eeqpp+jUqROpqalERkbSpk0bGjVq5Ld8rTV2u52QkJAAbaEQZ4chQ4bw66+/UlBQQFBQUIUvf+fOneV6hkSgORwOLrnkEjZu3EirVq34+OOPizXUPBU5OTmEhobi8Xh45plneO2110hISOCvv/7izjvvBGDs2LHceOONfPPNNyQnJ7Ny5Uq/h5f1798fj8fDeeedx5gxY4iKimLcuHE8/vjjFfoDSS4fiHL7448/2L9/P7feeitWq5U1a9awa9cugoODyc/PRylFixYtGDFiBPv372ffvn2MHDmS4cOH07hx41KXr5SShECIKtCtWzd+/fVXpkyZwrhx4yp02V988QU333wzv/32G4MGDarQZVc0t9vN+vXrSUlJYcmSJQCsWrWKjh07Mnz4cK699lr69u1LkyZNynW5LDs7m/T0dJo1a+ZXXlhL065dOywWCx07dqRLly4AvrZRubm5dOvWDYC0tDT++usvCgoKWLZsGa+++qpvWffdd99pbXtlkKTgDKe1ZuPGjaxYsYItW7awaNEiACZOnEjdunUDHJ0Q4lTdf//9jB8/ntTU1Apf9qeffgrA8uXLq21S4HQ6GT9+PElJSXz88ce+8iNHjrBt2zbef/99pk2bxrfffgtAZGQkjRo1on79+vTu3Zv09HSsVit9+vThuuuuw+128+yzz/L999/jdDrZuXNnsXW2b9+e8ePHA8YPoFGjRpUYW1hYmN/lVofDwTfffMOhQ4d49tlnGTRoEB07dqR3794V+ZFUCLl8cIbYs2cPn3zyCUuXLuXgwYN06dIFl8vF77//TkZGhm+6Tp06cd555/H+++9LIzMharioqChGjRrF22+/XWHLzM/PJyoqCqfTyYABAxg0aBB33XUXMTEx7Nq1i7i4OCIjIytsfafq7bff5oEHHgCgfv36dOzYkY4dOzJx4kTfNAcPHmT37t2sXbuWhQsXMnfu3BMu7/zzz2f58uUAxMTEYLPZOHDgAKGhoQwbNozp06cTHBx82nFX5h0/ckviCVSXpGDPnj38+eefNGvWjPj4eGJiYnA4HISG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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 517,
       "height": 262
      }
     },
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00003-d616f9bb-000c-4a05-a517-a5223d87f6df",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "eed5d174",
    "execution_start": 1621954333428,
    "execution_millis": 30,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# EDA to see likelyhood of stock price rising, falling, or remaining the same \n",
    "# over the course of a day within our dataset\n",
    "\n",
    "# count the stocks that increased/decreased&/didn't change\n",
    "rise = stocks.query('close > open').count()\n",
    "print(\"Stocks that rose in price: \", rise['ticker'])\n",
    "\n",
    "fall = stocks.query('open > close').count()\n",
    "print(\"Stocks that fell in price: \", fall['ticker'])\n",
    "\n",
    "steady = stocks.query('open == close').count()\n",
    "print(\"Stocks that didn't change in price: \", steady['ticker'])\n",
    "\n",
    "# see an average of how much stock prices rise/fall and the min and max\n",
    "difference = []\n",
    "difference = stocks['open'].sub(stocks['close'], axis = 0)\n",
    "print(\"Average of stock price differences between openning and close of day: \", difference.mean())\n",
    "print(\"Largest decrease in stock price in a day: \", min(difference))\n",
    "print(\"Largest increase in stock price in a day: \", max(difference))\n"
   ],
   "execution_count": 5,
   "outputs": [
    {
     "name": "stdout",
     "text": "Stocks that rose in price:  2799\nStocks that fell in price:  2674\nStocks that didn't change in price:  47\nAverage of stock price differences between openning and close of day:  -0.1993289273718129\nLargest decrease in stock price in a day:  -72.610107421875\nLargest increase in stock price in a day:  76.9598388671875\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00003-214f9a16-3173-493e-bf89-9303257e86b5",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "fca5f65d",
    "execution_start": 1621954333455,
    "execution_millis": 36,
    "output_cleared": false,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#FEATURE SELECTION: S&P500, DowJones, volume, previous 3 days, previous 5 days, weekday (,high, low, open)\n",
    "\n",
    "# calculate the previous 3 days (moving average)\n",
    "data[\"mv_avg_3\"]= data[\"close\"].rolling(min_periods=1,window=3).mean().shift(1)\n",
    "\n",
    "# calculate previous 5 days (moving average)\n",
    "data[\"mv_avg_5\"]= data[\"close\"].rolling(min_periods=1,window=5).mean().shift(1)\n",
    "\n",
    "#Drop the first row of the dataset as it has NANs after computing the previous x days\n",
    "#IMPORTANT: ONLY RUN THE FOLLOWING STEP ONCE, SO IT DOES NOT REMOVE THE FIRST ROW EACH TIME RUNNINNG IT\n",
    "data = data.iloc[1:] \n",
    "\n",
    "# extract weekday from Date column\n",
    "data['Date'] = pd.to_datetime(data['Date'])\n",
    "data['week_day'] = data.Date.apply(lambda x: x.weekday())\n"
   ],
   "execution_count": 6,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00003-8219e0a5-e9e7-4efd-8bd7-a71f0984b7f5",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "a005e19e",
    "execution_start": 1621954333494,
    "execution_millis": 583,
    "output_cleared": false,
    "deepnote_cell_type": "code"
   },
   "source": [
    "stocks3 = data[['Date', 'close', 'ticker']]\n",
    "# reset index and sort values by Date\n",
    "stocks3['Date'] = pd.to_datetime(stocks3['Date'])\n",
    "stocks3.set_index('Date')\n",
    "stocks3.sort_values('Date', inplace=True)\n",
    "\n",
    "# create the figure\n",
    "fig, ax = plt.subplots(1,2, figsize = (8, 4))\n",
    "sns.boxplot(x= stocks3[\"close\"], ax = ax[0])\n",
    "ax[0].set_title(\"Boxplot for all stocks\")\n",
    "sns.distplot(stocks3['close'], ax = ax[1])\n",
    "ax[1].set_title(\"Distribution plot for all stocks\")\n",
    "plt.tight_layout()"
   ],
   "execution_count": 7,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 576x288 with 2 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 568,
       "height": 280
      }
     },
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00006-e52f19f2-8e02-46ae-9140-29a7a83211da",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "aee24173",
    "execution_start": 1621954334074,
    "execution_millis": 2660,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from statsmodels.tsa.stattools import adfuller\n",
    "# check for stationarity\n",
    "\n",
    "dataframes = []\n",
    "tickers = ['BAC', 'BA', 'GOOG', 'MDLZ', 'PFE']\n",
    "# for each ticker, test the time series, difference it and test again for stationarity\n",
    "# new (differenced) data is appended to a list to replace the original column\n",
    "for ticker in tickers: \n",
    "    print(ticker)\n",
    "    temp = data[data['ticker']== ticker]\n",
    "    # check for stationarity \n",
    "    test = adfuller(temp['close'])\n",
    "    print('p-value: {}'.format(test[1]))\n",
    "    # difference to make series stationary \n",
    "    temp['close'] = temp['close'].diff()\n",
    "    #replace infinite values with null \n",
    "    temp.replace([np.inf, -np.inf, np.nan], 0, inplace = True)\n",
    "    test2 = adfuller(temp['close'])\n",
    "    print('p-value: {}'.format(test2[1]))\n",
    "    dataframes.append(temp)\n",
    "\n",
    "# concat all five data frames together\n",
    "data = pd.concat(dataframes)"
   ],
   "execution_count": 8,
   "outputs": [
    {
     "name": "stdout",
     "text": "BAC\np-value: 0.5922909540627093\np-value: 8.639030968330125e-18\nBA\np-value: 0.3790269378974299\np-value: 0.0\nGOOG\np-value: 0.9960941578346153\np-value: 9.829176703739381e-11\nMDLZ\np-value: 0.8906323349973715\np-value: 3.1895879651697307e-18\nPFE\np-value: 0.049013573520872517\np-value: 1.7279344875653528e-10\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Scaling \n",
    "\n",
    "We normalize the data using sklearn's MinMaxScaler to ensure the features have a normal distribution. \n",
    "\n"
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00011-39785f29-5907-45dc-aa0c-6ff3cbde424d",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00006-53aa8a5f-054c-4f09-9f4d-512743eb5a5f",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "2da78163",
    "execution_start": 1621954336826,
    "execution_millis": 1152,
    "output_cleared": false,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from sklearn.preprocessing import MinMaxScaler\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "# sort values and reset index \n",
    "data = data.sort_values(by = 'Date')\n",
    "data = data.reset_index(drop = True)\n",
    "\n",
    "# create the X and y dataframes to scale\n",
    "temp = data.drop(columns = ['Date', 'ticker', 'close'])\n",
    "y = data[['close']]\n",
    "temp = temp.replace(np.inf,0)\n",
    "col_list = temp.columns\n",
    "\n",
    "# instantiate the scaler, fit and transform the feature columns\n",
    "ss = MinMaxScaler(feature_range=(-1,1))\n",
    "ss.fit(temp)\n",
    "scaled = ss.transform(temp)\n",
    "\n",
    "# instantiate the scaler, fit and transform the target column\n",
    "t_transformer = MinMaxScaler(feature_range=(-1,1))\n",
    "t_transformer.fit(y)\n",
    "y_trans = t_transformer.transform(y)\n",
    "\n",
    "# replace the nan's within the scaled data with zero\n",
    "nan_indices = np.where(np.isnan(scaled))\n",
    "scaled[nan_indices] = 0\n",
    "\n",
    "# create new dataframe of scaled data\n",
    "scaled = pd.DataFrame(scaled, columns = col_list)\n",
    "scaled['Date'] = data['Date']\n",
    "scaled['ticker'] = data['ticker']\n",
    "scaled['close'] = y_trans\n",
    "\n",
    "# prepapre the data for the split\n",
    "scaled['Date'] = pd.to_datetime(scaled['Date'])\n",
    "scaled.set_index('Date')\n",
    "X = scaled.drop(columns = ['close', 'high', 'low', 'adjclose','Unnamed: 0'], axis = 1)\n",
    "y = scaled['close'].values.reshape(-1, 1)\n",
    "\n",
    "#Split dataset into training set, validation and test set\n",
    "# 80% training, 10% validation, and 10% test\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=42, shuffle = False)\n",
    "# split again \n",
    "X_valid, X_test, y_valid, y_test = train_test_split(X_test, y_test, test_size = 0.5, train_size = 0.5, random_state = 42, shuffle = False)\n"
   ],
   "execution_count": 9,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00008-1020cee5-e386-4810-bdce-9f7a3d61b19c",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "7c8cec71",
    "execution_start": 1621954337983,
    "execution_millis": 793,
    "deepnote_cell_type": "code"
   },
   "source": [
    "stocks4 = data[['Date', 'close', 'ticker']]\n",
    "# prepare the data for visualization. \n",
    "stocks4['Date'] = pd.to_datetime(stocks4['Date'])\n",
    "stocks4.set_index('Date')\n",
    "stocks4.sort_values('Date', inplace=True)\n",
    "\n",
    "# create the distribution and box plot for the scaled data \n",
    "fig, ax = plt.subplots(1,2, figsize = (8, 4))\n",
    "sns.boxplot(x= stocks4[\"close\"], ax = ax[0])\n",
    "ax[0].set_title(\"Boxplot for all stocks\")\n",
    "sns.distplot(stocks4['close'], ax = ax[1])\n",
    "ax[1].set_title(\"Distribution plot for all stocks\")\n",
    "plt.tight_layout()"
   ],
   "execution_count": 10,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 576x288 with 2 Axes>",
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjgAAAEYCAYAAABRMYxdAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjQuMSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/Z1A+gAAAACXBIWXMAAAsTAAALEwEAmpwYAAAx3UlEQVR4nO3deZxddX3/8dd7lixkg4SwhYQJBi2xuGBE61ZbERMV0qpUcCFYfj/oQ4H+XEpjjZAAXbQVFaStKFSWKipFG5RFUlzrAgEFDIgOGCBhCwlZSTJz7/38/jjnzJy5uXcyM5m5y8z7+XjMY+7ZP/fcc773c7/f7zlHEYGZmZnZaNJS7wDMzMzMhpsTHDMzMxt1nOCYmZnZqOMEx8zMzEYdJzhmZmY26jjBMTMzs1HHCU4DkxSS5g3Tug6W9CNJ2yR9ZjjWuZftrZV0fPp6uaTrRnqb/cRyuqSf1Gv7ZoMl6d8lfXKY1jVH0nZJrenwDyT9n+FYd7q+WyQtGa71DWK7Lh+HJ5ZRWz46wRmA9GDcmRYSz0n6rqTZ9Y4rM8AD9EzgWWBqRHy0BmHts3whYDZa5MqTbZI2S/qppL+S1FMeR8RfRcRFA1xXv+dIRDwWEZMjojgMse/xZRwRiyLi6n1d90hx+Th2OcEZuBMjYjJwKPA0cFmd4xmsI4AHYgh3dpTUNgLxmI1lJ0bEFJLz8p+AvwWuHO6N+NwdMJePo5ATnEGKiF3ADcD8bJykaZKukbRB0qOSlklqkTRd0jpJJ6bzTZbUKem0dPgraVX07emvuR9KOqLSdvvZxtHAvwN/lNYwba6w7FeAJcB56TzHSxov6XOSnkj/PidpfDr/G9O4/1bSU8B/VFjnCyTdIWmjpGcl/aek/Qe7PyUdKOk76S/ZTZJ+nL6va4E5wE1pzOel858kaU06/w/S95+ta7akG9N9tFHSF6ps858l/STdp/PS/b4lfR9fH+x7MBuqiNgSESuBdwNLJP0h9JQNF6evB3yOSOpQ0nRzhqTHgDty4/JfxC+QdKekrZL+W9L0dFtvlLQuH2NWUyBpIfB3wLvT7d2bTu9p8krjWpaWUc+kZda0dFoWxxJJj6Xn2yeq7RuXjy4f95UTnEGStB9JYfTz3OjLgGnAkcAfA6cBH4iITcBfAl+SdBDwWeBXEXFNbtn3AhcBBwK/Av6zyqarbeNB4K+An6XV0PuXLxgRp6fr/XQ6zyrgE8CrgZcBLwWOA5blFjsEmE7yy+bMSrsC+EfgMOBoYDawvErs/fkosA6YCRxMUoBGRLwfeIy05iwiPi3phcDXgP+Xzn8zyQk+Tkn/gu8AjwIdwCzg+j4BJwXDl4CXACdExBaSff894ADgcJqvZs5GgYi4k+Q8eH2FyQM+R3LL/DHJefmWKps8jaRsOhQoAJcOIMZbgX8Avp5u76UVZjs9/fsTkrJqMlD+Rfo64EXAm4Dz81/CFbh8dPk4ZE5wBu7bafa/BXgz8M8A6YFzCvDxiNgWEWuBzwDvB4iI7wHfBP4HeCtwVtl6vxsRP4qI3SQn1R+prH/P3rYxRO8FLoyIZyJiA7CibH0l4IKI2B0RO8sXjojOiLg9nb4BuISkYBmsbpJC9oiI6I6IH/dTTfxukv11e0R0A/8CTAReQ1IAHQb8TUTsiIhdEZFvd28nOfmnkxQKz+e2fwRwWIVlzGrpCZLjs9xgzpHM8vQ82OPcTV0bEb+OiB3AJ4G/SMuZffVe4JKIeCQitgMfB04pqz1aERE7I+Je4F6SBKIal48uH4fMCc7A/Vma/U8AzgZ+KOkQkl8W7SSZceZRkgw5cwXwh8BXImJj2Xofz16kBcImkgMxbyDbGKzDKqwvv90NaXNcRUquOrhe0npJW4Hr0jgH65+BTuB7kh6RtHSgMUdEiWT/zSL5hfRoRBSqLDsPWExSuHblxp9H8mvrzrRq9y+H8B7MhsMskvO/3GDOkczjg5j+KEn5MpTzt1ylcqWNpPYh81Tu9fMktTzVuHx0+ThkTnAGKSKKEXEjUCSpan2W3iw3MwdYDz2/Lq4ArgE+qD0va+z5NSJpMkkG/UTZPP1uAxjKI+GfqLC+/Hb3ts5/SOc5JiKmAu8jOREGJf3F9dGIOBI4CfiIpDdViaFPzJJEsv/Wk5zIc1S9w9+DwAeAWyS9KLf9pyLi/0bEYSS1a/9a4TMyG1GSXknyRbTHL+RBniPsZXwmXwsyh6R8eRbYAeyXi6uVpLljoOutVK4USC7MGAqXjy4fh8wJziApsZikTfLBSC69/Abw95KmpJ3gPkKSsUPaZkrS3v3PwDVlVcFvlfQ6SeNI2jt/HhF9fn0NYBtPA4en6xiorwHLJM2UdCBwfm59AzEF2A5skTQL+JtBLNtD0tvTjmwiaf4rklT/QvK+jszN/g3gbZLeJKmdpH16N/BT4E7gSeCfJE2SNEHSa/PbioivkXweqyS9IN3+yZIOT2d5juSzKmFWA5KmSno7SX+I6yLi/grzDOYcGaj3SZqf9im8ELghLWd+C0yQ9Lb0HFsGjM8t9zTQodwl7WW+BnxY0tw0Icn67FSrOdgbl48uH4fMCc7A3SRpO7AV+HtgSUSsSaedQ/LL5xGSX2BfBa6S9AqSE+209CT8FMkBkq9m/CpwAUnV6ytIMv1KKm4jnXYHsAZ4StKzA3w/FwOrgfuA+4F70nEDtQI4luSk+y5w4yCWzTsKWEVSGPwM+NeI+H467R9JCpnNkj4WEQ+R7J/LSH61nUjSXtyV7t8TSapaHyPpmPfu8o1Fcr+OC0mvLgFeCfwi/WxXAn8dEY8M8b2YDdRNkraR/LL+BEkfjQ9UmXfA58ggtn8t8BWS5qIJwLmQXNUFfBD4Mskv/x0k51Lmm+n/jZLuqbDeq9J1/wj4PbCLpOwaKpePLh+HTHvvq2YjRcnliesiYtne5jUzG0tcPtq+cg2OmZmZjTpOcMzMzGzUcROVmZmZjTquwTEzM7NRZ1APCTvwwAOjo6NjhEIxs3q6++67n42ImXufs7m43DIb3aqVXYNKcDo6Oli9evXwRWVmDUPSo3ufq/m43DIb3aqVXW6iMjMzs1HHCY6ZmZmNOk5wzMzMbNRxgmNmZmajjhMcMzMzG3Wc4JiZmdmo4wTHzMzMRh0nOGZmZjbqOMExM7Omtfn5Lt7xr//L45uer3co1mCc4JhZzUlaKOkhSZ2SllaY/gZJ90gqSHpXhelTJa2T9IXaRGyN6pFnd3DPY5tZ88SWeodiDcYJjpnVlKRW4HJgETAfOFXS/LLZHgNOB75aZTUXAT8aqRiteXQXSgDsTv+bZZzgmFmtHQd0RsQjEdEFXA8szs8QEWsj4j5gj28tSa8ADga+V4tgrbF1FwNwgmN7coJjZrU2C3g8N7wuHbdXklqAzwAf28t8Z0paLWn1hg0bhhyoNb6uYjH57wTHyjjBMbNm8kHg5ohY199MEXFFRCyIiAUzZ86sUWhWD10F1+BYZW31DsDMxpz1wOzc8OHpuIH4I+D1kj4ITAbGSdoeEXt0VLaxobuYJDauwbFyTnDMrNbuAo6SNJcksTkFeM9AFoyI92avJZ0OLHByM7ZliY0THCvnJiozq6mIKABnA7cBDwLfiIg1ki6UdBKApFdKWgecDHxR0pr6RWyNLKvB2V0o1jkSazSuwTGzmouIm4Gby8adn3t9F0nTVX/r+ArwlREIz5qIm6isGtfgmJlZ0+ryZeJWhRMc63HZZZdx2WWX1TsMM7MBcx8cq8YJjvW49dZbufXWW+sdhpnZgLkPjlXjBMfMzJpWTx+comtwrC8nOGZm1rSypqnd3U5wrC8nOGZm1rS6XINjVTjBMTOzptXbB8cJjvXlBMfMzJpWt59FZVU4wTEzs6bV5Rv9WRVOcMzMrGl1PrMdgA3bdvPVXzxW52iskTjBMTOzplUsRfrfNTjWlxMcMzNrWlmCU0gf2WCWcYJjZmZNq5DW3BRKTnCsLyc4ZmbWtHpqcNxEZWWc4JiZWdNyE5VV4wTHzMyaVtY0FfQmO2bgBMfMzJpYPqlxM5XlOcExM7OmlU9wim6mshwnOGZm1rTyCU63m6gsxwmOmZk1rUIpaGsR4D441pcTHDMza1rFUjC+vRXofbK4GTjBMbM6kLRQ0kOSOiUtrTD9DZLukVSQ9K7c+JdJ+pmkNZLuk/Tu2kZujaZYCsa3tfS8Nss4wTGzmpLUClwOLALmA6dKml8222PA6cBXy8Y/D5wWES8GFgKfk7T/iAZsDa1QKjEhTXAKrsGxnLZ6B2BmY85xQGdEPAIg6XpgMfBANkNErE2n9fnGiojf5l4/IekZYCawecSjtoZTKgWloKeJyo9rsDzX4JhZrc0CHs8Nr0vHDYqk44BxwMMVpp0pabWk1Rs2bBhyoNbYutP73mRNVE5wLM8Jjpk1HUmHAtcCH4iIPdolIuKKiFgQEQtmzpxZ+wCtJrrT+970JDi+D47lOMExs1pbD8zODR+ejhsQSVOB7wKfiIifD3Ns1kS6CmkNTk8TlfvgWC8nOGZWa3cBR0maK2kccAqwciALpvN/C7gmIm4YwRitCWSXhU9wE5VV4ATHzGoqIgrA2cBtwIPANyJijaQLJZ0EIOmVktYBJwNflLQmXfwvgDcAp0v6Vfr3stq/C2sEWQ3OuLakBseParA8X0VlZjUXETcDN5eNOz/3+i6Spqvy5a4DrhvxAK0pdGU1OO3Jb/VuN1FZjmtwzMysKWVNVONak68yt1BZnhMcMzNrSt2FJKNpT/vglJzhWI4THDMza0pZE1V7S1aD4wTHejnBMTOzppR1Mm5vS54m7gocy3OCY2ZmTWnPPjjOcKyXExwzM2tKWYLT2iKEExzrywmOmZk1pXyC09IifJW45TnBMTOzptSV3tivVaJFEK7BsRwnOGZm1pSKaZVNS4tokdxEZX04wTEzs6aUtlDRoiTB8ZMaLM8JjpmZNaWeGhzhJirbgxMcMzNrStnTw1uUdjJ2gmM5TnDMzKwpZY9m6OmD46uoLMcJjpmZNaXeGpzkzzU4lucEx8zMmlIx30Tlq6isTFu9A7D6u+yyyyoOn3POOfUIx8xsQPJ9cCT5WVTWhxMco7Ozs99hM7NGVHQTlfXDTVRmZtaUirlOxq0trsGxvpzgmJlZU8qaqATpVVTOcKyXExwzM2tKxVKJFoEk5CYqK+MEx8xqTtJCSQ9J6pS0tML0N0i6R1JB0rvKpi2R9Lv0b0ntorZGUywlNTeQ/Hd+Y3lOcMyspiS1ApcDi4D5wKmS5pfN9hhwOvDVsmWnAxcArwKOAy6QdMBIx2yNKanB6U1wis5wLMcJjpnV2nFAZ0Q8EhFdwPXA4vwMEbE2Iu4Dyu9N+xbg9ojYFBHPAbcDC2sRtDWeQilI8xtfRWV7cIJjZrU2C3g8N7wuHTdsy0o6U9JqSas3bNgw5ECtsZVK0VuD0+JOxtaXExwzG3Ui4oqIWBARC2bOnFnvcGyEFEpBS0vWRAVObyzPCY6Z1dp6YHZu+PB03Egva6NMsRS09DRRuQbH+nKCY2a1dhdwlKS5ksYBpwArB7jsbcAJkg5IOxefkI6zMaiQb6LyoxqsjBMcM6upiCgAZ5MkJg8C34iINZIulHQSgKRXSloHnAx8UdKadNlNwEUkSdJdwIXpOBuDSn1qcNzJ2Prys6jMrOYi4mbg5rJx5+de30XS/FRp2auAq0Y0QGsKhfJOxk5wLMc1OGZm1pSKbqKyfjjBMTOzplQsBS3pt5ibqKycExwzM2tKe3QydhWO5TjBMTOzppR/VIPcRGVlnOCYmVlTKvgqKuuHExwzM2tKpfBVVFadExwzM2tKhWLvoxpa3URlZZzgmJlZUyrmniYu4U7G1ocTHDMza0rFCFpzV1G5hcrynOCYmVlT2vNGf85wrJcTHDMza0qFYt+rqAI3U1kvJzhmZtaUkj44vVdRQXLpuBk4wTEzsyZVjN6rqLKmKjdTWcYJjpmZNaVi2Y3+wDU41ssJjpmZNaVC7lEN2f9i0QmOJZzgmNmQSbpR0tskuSyxmiuVyCU4ybiim6gs5ULJzPbFvwLvAX4n6Z8kvajeAdnYkdTgJK97OxmX6hiRNRInOGY2ZBGxKiLeCxwLrAVWSfqppA9Iaq9vdDbaFUu5TsaoZ5wZOMExs30kaQZwOvB/gF8CnydJeG6vY1g2BvR5mnj6beYExzJt9Q7AzJqXpG8BLwKuBU6MiCfTSV+XtLp+kdlYUH4n42ycGbgGx8z2zZciYn5E/GOW3EgaDxARC6otJGmhpIckdUpaWmH6eElfT6f/QlJHOr5d0tWS7pf0oKSPj9D7siZQKcHxZeKWcYJjZvvi4grjftbfApJagcuBRcB84FRJ88tmOwN4LiLmAZ8FPpWOPxkYHxHHAK8AzsqSHxt78k1U2VPFXYNjGTdRmdmgSToEmAVMlPRySHt4wlRgv70sfhzQGRGPpOu6HlgMPJCbZzGwPH19A/AFJffkD2CSpDZgItAFbN3nN2RNyU1U1h8nOGY2FG8h6Vh8OHBJbvw24O/2suws4PHc8DrgVdXmiYiCpC3ADJJkZzHwJEki9eGI2FS+AUlnAmcCzJkzZ0BvyJpLRPS5iqq1xQmO9eUEx8wGLSKuBq6W9M6I+K8abvo4oAgcBhwA/FjSqqw2KBffFcAVAAsWLPA33iiU5THlTVTug2MZJzhmNmiS3hcR1wEdkj5SPj0iLqmwWGY9MDs3fHg6rtI869LmqGnARpKbCt4aEd3AM5L+F1gAPIKNKdkN/dxEZdW4k7GZDcWk9P9kYEqFv/7cBRwlaa6kccApwMqyeVYCS9LX7wLuiIgAHgP+FEDSJODVwG/27a1YM8puWOwEx6oZkRqcjRs3smLFCi644AJmzJgxEpvYY3uf/OQniQguvvjifre5ceNGli5dyuOPP86cOXM477zz+MxnPoMkLrroop5ly99DNrxkyRLOP/98VqxYwRe/+EXWrVvHxRdfzNVXX825557LJZdcwrZt21i3bh0RwVlnncUVV1zBAQccwKZNm5g+fTqbNm1i9uzZfO5znwPg3HPPZf369UjisMMOY9OmTbzzne/kuuuuG/F9V27SpEnce++9ALzxjW+s6bbnzp3Lhz70IZYtWwbAtGnTePrpp3v22Uc/+lH+67/+i0cffZSI4B3veAc33ngjH/3oRznxxBPp7OzknHPOYfbs2Zx33nlceumlnHbaaVxwwQVceOGFfPnLX+75nIGKn2+1Y7a/Yyxb9txzz+XSSy/ts478esu3WWkbw3nejOR5GBFfTP+vGMKyBUlnA7cBrcBVEbFG0oXA6ohYCVwJXCupE9hEkgRBcvXVf0haQ9Kx+T8i4r59f0fWbHprcOjz349qsIxiEA8mW7BgQaxevfd7d11yySXcdNNNnHTSSXz4wx/el/gG5JJLLmHlyuQH4OLFi/vdZn5egI6ODtauXbvHsuXvIRueNGkS27dvZ/LkyWzfvh2AyZMns2PHDo444oiedQ3E4sWLiYg+8dTbpEmT2LFjR922n9+v5SRR6XiVxPe//31OP/30nv3f0dHBo48+WvHzyvZ7pc+32jHb3zGWLXvEEUfw6KOP9llHfr3l26y0jeE8bwa7Pkl393fvmirLfJrkUvGdwK3AS0g6/tY+O69ioOWWNZfNz3fxsgtv523HHMpr5x3I2md3cMWPH+HaM47j9UfNrHd4VkPVyq5hb6LauHEjt956KxHBrbfeysaNG4d7ExW3l7nllluqbnPjxo3ccsstfcblE5Js2fL30NnZ2TOcfUnmv4S3b99ORAwquQG46aab+M53vjOoZUZaPZMboGpyA1RMbrLxV155ZZ/9v3bt2qqf180331z18610zPZ3jOWPlWyb2Try02655ZYBbWO4zpsanocnRMRW4O0kz6KaB/zNSG3MLJN1Ju55FpWvorIyw57gXH311ZTSKsJiscg111wz3JvYY3vd3d09w93d3VW3WT5vuWzZ8vdw8cUX9wwPp1KpNCLrHYuuvfbaAc/b3d3dcxyUf76Vjtn+jrH8sZLJ1pGfVr7NStsYzvOmhudh1sz9NuCbEbFlpDZkllfKEpyyJionOJbZa4Ij6UxJqyWt3rBhw15XuGrVKgqFAgCFQoHbbx/Z5+2tWrWqzy/7iKi6zVWrVvW7rmzZ8vewdu3anmEbHbJjpvzzrXTM9neM5Y+VTLaO/LSI6LPNStsYzvOmhufhdyT9huSuwv8jaSawa6Q2ZpbJanBa/agGq2KvCU5EXBERCyJiwcyZe2/XPP7442lrS37UtbW18eY3v3nfo9zL9pTdAIGkP0a1bR5//PH9ritbtvw9dHR09Azb6JAdM+Wfb6Vjtr9jLH+sZLJ15KdJ6rPNStsYzvOmVudhRCwFXgMsSC/d3kFyIz6zEZXV1KgswSk5wbHUsDdRLVmyhJb0ufWtra2cdtppw72JPbbX3t7eM9ze3l51m+XzlsuWLX8Py5Yt6xkeTi0tLSOy3rHo/e9//4DnbW9v7zkOyj/fSsdsf8dY/ljJZOvITyvfZqVtDOd5U+Pz8A+Ad0s6jeSS7hNGcmNm0Jvg7HkVlRMcSwz7t+uMGTNYuHAhkli4cOGIXyaebS+zaNGiqtucMWMGixYt6jOuo6Njj2XL38O8efN6hidPngzQ8z97LanPugbixBNP5O1vf/uglhlpkyZN2vtMIyi/X8vla1HKx59xxhl99n9HR0fVz+utb31r1c+30jHb3zGWP1aybWbryE9btGjRgLYxXOdNrc5DSdcC/wK8Dnhl+jeoK7HMhmKPTsa+D46VGZHqgyVLlnDMMceMeO1Nfnvz58/n6KOP3us2lyxZwlFHHcWECRN44QtfyLJlyzj66KOZP39+n2XL30M2vGLFCiZNmsTy5cs56qijmDhxIitWrOCYY45h2bJlzJ8/n9mzZ/d8GZ911llIYvr06QA9/2fPnt3zK3/WrFlA8kU9a9YsJk6cyPve975h30+Nbu7cuSxfvpwJEyYwYcIEDj74YKB3n33kIx/pSSIA3vGOd/SMB1i2bBkTJ07s+VyPOeYYli9fzqRJk1ixYkWfz7na59tf7V+1YyxbNttmteNoINsYzvOmRufhAuC1EfHBiDgn/Tt3JDdoBvkanL5XUbkGxzIjch8cay5//dd/DUBnZycA8+bNA+Dzn/983WKy2hvifXC+CZwbEU+OUFj7zOXW6LTmiS287dKf8N5XzeHFh01j8/NdfPq2h/j0O1/CX7xy9t5XYKNGtbLLPWfNbF8cCDwg6U5gdzYyIk6qX0g2FlR7VINrcCzjBMfM9sXyegdgY1P5wzbVcx8c31vMEk5wzGzIIuKHko4AjoqIVZL2I3m+lNmIKr+KqtWdjK2Mr1E2syGT9H+BG4AvpqNmAd+uW0A2ZhSrPKrBTVSWcYJjZvviQ8Brga0AEfE74KC6RmRjQvlVVPKjGqyMExwz2xe7I6IrG5DUBvgbxkZcYY8b/aVNVIO4MthGNyc4ZrYvfijp74CJkt4MfBO4qc4x2Riwx31wsgSn6ATHEk5wzGxfLAU2APcDZwE3A8vqGpGNCXsmOMl498GxjK+iMrMhi4iSpG8D346IDfWOx8aO3kc1JMOSEO6DY71cg2Nmg6bEcknPAg8BD0naIOn8esdmY0P508QhuZLKfXAs4wTHzIbiwyRXT70yIqZHxHTgVcBrJX24vqHZWJAlMi25Z/C2yDU41ssJjpkNxfuBUyPi99mIiHgEeB9Qm6fs2piW3bG4NV+DI1FwJ2NLOcExs6Foj4hny0em/XDa6xCPjTFZItNSluD4UQ2WcYJjZkPRNcRpAEhaKOkhSZ2SllaYPl7S19Ppv5DUkZv2Ekk/k7RG0v2SJgztLVgz6+2D0zuutUV0u4nKUr6KysyG4qWStlYYL6DfhENSK3A58GZgHXCXpJUR8UButjOA5yJinqRTgE8B705vJHgd8P6IuFfSDKB7GN6PNZmePji5TjitLaK74BocSzjBMbNBi4h9eaDmcUBn2mcHSdcDi4F8grOY3ieV3wB8QcnlMicA90XEvWkcG/chDmti5ffBgTTBKTrBsYSbqMys1mYBj+eG16XjKs4TEQVgCzADeCEQkm6TdI+k8yptQNKZklZLWr1hg2/PMxr19sHpHdcqN1FZLyc4ZtZM2oDXAe9N//+5pDeVzxQRV0TEgohYMHPmzFrHaDVQtQbHTVSWcoJjZrW2HpidGz48HVdxnrTfzTRgI0ltz48i4tmIeJ7k0RDHjnjE1nB674PjJiqrzAmOmdXaXcBRkuZKGgecAqwsm2clsCR9/S7gjogI4DbgGEn7pYnPH9O3746NEYU0kWnJfYu1tsjPorIe7mRsZjUVEQVJZ5MkK63AVRGxRtKFwOqIWAlcCVwrqRPYRJIEERHPSbqEJEkK4OaI+G5d3ojVVVfaB6e1rAany01UlnKCY2Y1FxE3kzQv5cedn3u9Czi5yrLXkVwqbmNYd7FEe6v6PIuqVW6isl5uojIzs6bTXSgxrrXvV5ibqCzPCY6ZmTWd7mKJ9ra+X2EtbqKyHCc4ZmbWdLqKQbtrcKwfTnDMzKzpdBf3bKJq82XiluMEx8zMmk7WyTivRb7Rn/VygmNmZk0nSXD2bKLyoxos4wTHzMyaTlehch8cN1FZxgmOmZk1nUpXUbUKN1FZDyc4ZmbWdJJOxn374LS2tLiJyno4wTEzs6ZTtQ9OsUSEkxxzgmNmZk2o8n1wIAKKrsUxnOCYmVkT6i5UqsFJhn2zPwMnOGZm1oS6iyXGtZX3wUmGu3wlleEEx8zMmlDFPjhpvlMougbHnOCYmVkT6q7YB6clneYaHHOCY2ZmTairylVUgJ8obgC01TsAq7958+YB0NnZ2WfYzKxRVb4PTvLfnYwNnOAYcM455wBw66239hk2M2tU/V1F5SYqAzdRmZlZE+ouRoVHNbiJyno5wTEzs6YSEVX64CT/3URl4ATHzOpA0kJJD0nqlLS0wvTxkr6eTv+FpI6y6XMkbZf0sZoFbQ0jS2AqPYsK3ERlCSc4ZlZTklqBy4FFwHzgVEnzy2Y7A3guIuYBnwU+VTb9EuCWkY7VGlOWwJTX4KT5jRMcA5zgmFntHQd0RsQjEdEFXA8sLptnMXB1+voG4E1S0sFC0p8BvwfW1CZcazTdhaQGpzzBaUv74HT7Rn+GExwzq71ZwOO54XXpuIrzREQB2ALMkDQZ+FtgRX8bkHSmpNWSVm/YsGHYArfGkD2KYY9OxlkTlTsZG05wzKy5LAc+GxHb+5spIq6IiAURsWDmzJm1icxqJmuCKu+D09LTydgJjvk+OGZWe+uB2bnhw9NxleZZJ6kNmAZsBF4FvEvSp4H9gZKkXRHxhRGP2hpGvg9OMZfM9D5s001U5gTHzGrvLuAoSXNJEplTgPeUzbMSWAL8DHgXcEdEBPD6bAZJy4HtTm7GnnyCs6u7N8FpcxOV5TjBMbOaioiCpLOB24BW4KqIWCPpQmB1RKwErgSuldQJbCJJgswA6KrSybgle5q4m6gMJzhmVgcRcTNwc9m483OvdwEn72Udy0ckOGt4PX1w2srvg+MmKuvlTsZmZtZUqt0Hx01UlucEx8zMmkrXXm705yYqAyc4ZmbWZLIb+e35LCrf6M96OcExM7OmkjVBjStPcHruZOwaHHOCY2ZmTaanD05ZJ2NJtLXICY4BTnDMzKzJVOuDk41zE5WBExwzM2syWQJT3kQF0N7qGhxLOMExM7OmUu0y8WycExwDJzhmZtZkehMc7TGtvbWF7oKbqMwJjpmZNZmuQtbJuEINTpvo9n1wDCc4ZmbWZLJOxhX74LS4k7ElnOCYmVlT6a7ysM1snB/VYOAEx8zMmkx3sUSLeu9cnNfe5quoLOEEx8zMmkp3sVSx9gZgv/Y2dnQVahyRNSInOGZm1lS6iqWK/W8Apk5sY9suJzjmBMfMzJpMd7FU8QoqgCkT2tm6q7vGEVkjcoJjZmZNpatQvQZnygTX4FjCCY6ZmTWVbbsKTJnQVnHa1AntbNtVIMKXio91TnDMzKypbN3VzdSJ7RWnTZnQRrEUPN9VrHFU1mic4JiZWVPZurPA1Co1OFMmJImPm6nMCY6Z1ZykhZIektQpaWmF6eMlfT2d/gtJHen4N0u6W9L96f8/rXnwVnd7q8HJ5rGxzQmOmdWUpFbgcmARMB84VdL8stnOAJ6LiHnAZ4FPpeOfBU6MiGOAJcC1tYnaGsnWnd1Mq5LgZInPNic4Y54THDOrteOAzoh4JCK6gOuBxWXzLAauTl/fALxJkiLilxHxRDp+DTBR0viaRG0NISLYuqvA1Al7q8FxE9VY5wTHzGptFvB4bnhdOq7iPBFRALYAM8rmeSdwT0TsLt+ApDMlrZa0esOGDcMWuNXfjq4ixVIwdWK1q6jSBGena3DGOic4ZtZ0JL2YpNnqrErTI+KKiFgQEQtmzpxZ2+BsRGWJS7UanKnuZGwpJzhmVmvrgdm54cPTcRXnkdQGTAM2psOHA98CTouIh0c8WmsoWefh6p2MneBYwgmOmdXaXcBRkuZKGgecAqwsm2clSSdigHcBd0RESNof+C6wNCL+t1YBW+PYujNJXKrV4Exob6GtRb6KypzgmFltpX1qzgZuAx4EvhERayRdKOmkdLYrgRmSOoGPANml5GcD84DzJf0q/Tuoxm/B6qiniapKHxxJ6eManOCMdZWPEDOzERQRNwM3l407P/d6F3ByheUuBi4e8QCtYWU1M9UuE4ek+cpNVOYaHDMzaxp762QMyaXivorKnOCYmVnTyO5vU+1hmwBTxrsGx9xEZTkLFy6sdwhmZv3aurObSeNaaWut/vt86sQ2Ht6wo4ZRWSNygmM9zjnnnHqHYGbWr18+tpm21ha++ovHqs7TceAkvv+bDXQVSoxrc0PFWOVP3szMmsbO7iIT2vv/6pp/6FS6iiUe3rC9RlFZI3KCY2ZmTWNHV4GJ7f03Psw/dCoADzyxtRYhWYNygmNmZk0hInhm624OmtL/81XnHjiJ8W0tPPikE5yxzH1wzMysKTy1dRc7u4scMm1C1Xmyvjkzp4znjoee4ciZk3nPq+bUKkRrIK7BMTOzpvCbJ7cBcMjU6glO5tBpE3hy8y5KESMdljUoJzhmZtYUHkibnPqrwcm8YOZkdnYX+f2zvlx8rHKCY2ZmTeE3T23jgP3amdDeutd5jz50KuPaWrj38c0jH5g1JCc4ZmbWFNY8sYWDB9A8BdDe2sKLD53Kr5/Ywq7u4ghHZo3ICY6ZmTW83z29jUc27GDeQZMHvMwrjjiAXd0lbrh73QhGZo3KCY6ZmTW8//7VE7S2iGNmTRvwMnMPnMThB0zkiz96mEKxNILRWSNygmNmZg2tWAq+/av1vHbegUzp5yni5STxJy86iMc37eTLP/n9CEZojcgJjpmZNbTr73qMdc/t5D3HzR70sn9wyBTeeswh/MttD/HTh58dgeisUTnBMTOzhvXMtl185nu/5biO6bzlxYcMenlJ/OOfv4SOAydx+lV3cf2djxG+N86Y4ATHzMwa0pU//j1/dvn/sm1XN686cjpfu/PxIa3nu/c/yamvnMOc6fux9Mb7+dBX72HL893DHK01Gic4ZmbWcH69fgv/9sNOntqyi/ccN4dDp03cp/VNHNfK6a/tYOGLD+F7a55m0ed/xM8e3jhM0VojcoJjZmYN49ntu/n4jfdz4hd+wq7uEme87khedMjUYVl3i8QbXjiTGz/4Gsa1tXDql37OOV/7JXet3eRmq1HID9s0M7O6KpaCe9dt5u+/8yD3rttMKYLXHDmDNx198IDuWjxYv16/ldNfM5cf/PYZbvv1U9x07xN0zNiPE196GK+bdyAvOXx/Jo4b/u1abTnBMbOak7QQ+DzQCnw5Iv6pbPp44BrgFcBG4N0RsTad9nHgDKAInBsRt9UwdBugiOCprbt4cssuugoliqWgUAo2P9/Fuud2sn7zTtY/t5MnNu9k3XM72dldpL1VvOKIA3jNCw5k5pTxIxrfuLYWTph/CH/8wpmseWIr9zz2HF+4o5PL7uikRfCHs6Zx7JwDePmc/Xnp4ftzyLQJI5Js2chxgmNmNSWpFbgceDOwDrhL0sqIeCA32xnAcxExT9IpwKeAd0uaD5wCvBg4DFgl6YURMSbuxR8R7C6U2N1dYnehyO5CcvO6lhbRKtHSAq0SrS3qGdfakvwVS0FXsURXoUR37j8kVxq1SOzqLrJlZzdbdnazfVeBUgQRJP9J/k9oa+WgqePZf+I4nu8qsKOrwPbdRbbvKlCMYPuuAg8+uZUfPPQMW3cVqr6X6ZPGMaG9hf0njuPYOfsz64D9eNHBU2peczK+rZVj5xzAsXMO4PndBR7b9HzP33/+4lG+8tO1PfNOm9jOzCnjOWjKeGYfsB/zDprMofsnj44olnr3VfY6CEoBAtpaW2hvFVMntDN1YjvTJrYzob1vLxFJPa/zn2dbS0vyOv0ss881P38mcp9ZKUBKmuZaRMX5RzMnOGZWa8cBnRHxCICk64HFQD7BWQwsT1/fAHxBSem8GLg+InYDv5fUma7vZ/sa1I9/t4Gzrr274rS9dc9Ivv6rTOtn2X5Xm35BJl+UyRdXqUm6iUyd0EbHgZPomDGJA/Zrp621pedLdmJ7K/vvN45xbY3XBXS/8W38waFT+YNDkz4/xVLw9NZdPLF5J1t3Fdi2q5vtuwuse24n9z6+mR1d9c2rs6Ql0gR0X7sRSUkyJin9DyIdSfIvoOfY7FkuN0N+OfUuOmg/+7s3MXUQN3WsZFAJzt133/2spEf3aYsj60Cgke/k1OjxgWMcDo0eH1SO8YgabXsWkL/edx3wqmrzRERB0hZgRjr+52XLzirfgKQzgTPTwe2SHiqbpZE/o1ER2/0jHEgFo2K/1UFDxjbtImDgsVUsuwaV4ETEzMHMX2uSVkfEgnrHUU2jxweOcTg0enzQHDHui4i4Arii2vRGfv+ObWgc29CM5tgar47QzEa79UD+nvuHp+MqziOpDZhG0tl4IMuamTnBMbOauws4StJcSeNIOg2vLJtnJbAkff0u4I5IblSyEjhF0nhJc4GjgDtrFLeZNZHR1sm4apV0g2j0+MAxDodGjw/qGGPap+Zs4DaSy8Sviog1ki4EVkfESuBK4Nq0E/EmkiSIdL5vkHRILgAfGuIVVI38GTm2oXFsQzNqY5Pv3mhmZmajjZuozMzMbNRxgmNmZmajTlMmOJJOlrRGUknSgrJpH5fUKekhSW/JjV+YjuuUtLTG8S6XtF7Sr9K/t+4t3nqo5z6qRtJaSfen+211Om66pNsl/S79f0CNY7pK0jOSfp0bVzEmJS5N9+l9ko6tY4xNcRwOp2plhaQOSTtz++Lfc9NekR5znelnNyK3f22WcqzRj5tGK7caqcxq5LKqJmVUclvn5voDjgZeBPwAWJAbPx+4FxgPzAUeJunE2Jq+PhIYl84zv4bxLgc+VmF8xXjrtE/ruo/6iWstcGDZuE8DS9PXS4FP1TimNwDHAr/eW0zAW4FbSG7o+WrgF3WMseGPwxHYD9XKio78vilb5s70s1L62S2qcWwNVY418nHTiOVWI5VZjVxW1aKMasoanIh4MCLK70wKudu4R8Tvgew27j23ho+ILiC7NXy9VYu3Hhp1H1WyGLg6fX018Ge13HhE/Ijkyp6BxLQYuCYSPwf2l3RonWKsppGOw2HVT1lRUfrZTI2In0dSsl7DCB1fo6Aca4TjptH2STV1KbMauayqRRnVlAlOPyrdAn5WP+Nr6ey02u+qXPVkI8SVaaRY8gL4nqS7ldx+H+DgiHgyff0UcHB9QuujWkyNtl8b/TispbmSfinph5Jen46bRfL+M/XYF41YjjXqcdMIMZRr9DKr0cuqYTvWGjbBkbRK0q8r/DVidr63eP8NeAHwMuBJ4DP1jLXJvC4ijgUWAR+S9Ib8xPRXdkPd66ARY0qNyuNwiGXFk8CciHg58BHgq5KmNkhsNefya1g1TZnVSLGkhvVYa9gb/UXE8UNYrL/buI/o7d0HGq+kLwHfSQcb6bbzjRRLj4hYn/5/RtK3SKoln5Z0aEQ8mVahPlPXIBPVYmqY/RoRT2evG/g4HLShlBWRPI18d/r6bkkPAy8ked+H52bdp33RLOVYE5dfjRBDH01QZjVsWTXcZVTD1uAMUbXbuA/k1vAjpqwd88+BrNd4I912vq77qBJJkyRNyV4DJ5Dsu/xt/JcA/12fCPuoFtNK4LT0CoVXA1ty1cM11STHYU1ImimpNX19JMl7fiT9bLZKerUkAadR++OrocqxBj9uGqrcapIyq2HLqmE/1kayl/RI/aVvfB3JL7Cngdty0z5B0sP6IXJXP5D0EP9tOu0TNY73WuB+4L70gzp0b/HWab/WbR9ViedIkp7z9wJrspiAGcD/AL8DVgHTaxzX10iqT7vT4/CMajGRXJFwebpP7yd3tUwdYmyK43CY90PFsgJ4Z3pM/Qq4Bzgxt8wCkoL1YeALpHd8r1Vs/X0e9ThHG/24aaRyq9HKrEYuq2pRRvlRDWZmZjbqjLYmKjMzMzMnOGZmZjb6OMExMzOzUccJjpmZmY06TnDMzMxs1HGCM8YpeXrrx+odh5nZQLncsoFwgmNmZmajjhOcMUbSaemDzO6VdG3ZtJdJ+nk6/VvZg84knSvpgXT89em4SenD0O5U8sDChnq2jpmNHi63bCh8o78xRNKLgW8Br4mIZyVNB84FtkfEv0i6DzgnIn4o6UJgakT8P0lPAHMjYrek/SNis6R/AB6IiOsk7U9y2+yXR8SOOr09MxuFXG7ZULkGZ2z5U+CbEfEsQERsyiZImgbsHxE/TEddDWRPwb0P+E9J7wMK6bgTgKWSfgX8AJgAzBnpN2BmY47LLRuShn2auDWUt5EUGicCn5B0DMlzS94ZEQ/VNTIzs8pcbo1xrsEZW+4ATpY0AyCt6gUgIrYAz0l6fTrq/cAPJbUAsyPi+8DfAtOAycBtwDnpE5eR9PLavQ0zG0NcbtmQuAZnDImINZL+nqQAKAK/BNbmZlkC/Luk/YBHgA8ArcB1aVWwgEvTtuyLgM8B96WFye+Bt9fszZjZmOByy4bKnYzNzMxs1HETlZmZmY06TnDMzMxs1HGCY2ZmZqOOExwzMzMbdZzgmJmZ2ajjBMfMzMxGHSc4ZmZmNur8f7DmFiUWgs1qAAAAAElFTkSuQmCC\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 568,
       "height": 280
      }
     },
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00010-627bbab0-9b74-43d9-a0f0-a660deb8e8e6",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "51c323af",
    "execution_start": 1621954338800,
    "execution_millis": 886,
    "deepnote_cell_type": "code"
   },
   "source": [
    "stocks5 = data[['Date', 'open', 'high', 'low', 'close', 'ticker']]\n",
    "import matplotlib.pyplot as plt\n",
    "# prepare the data for visualization\n",
    "stocks5['Date'] = pd.to_datetime(stocks5['Date'])\n",
    "stocks5.set_index('Date')\n",
    "stocks5.sort_values('Date', inplace=True)\n",
    "palette ={\"BAC\": \"C0\", \"MDLZ\": \"C1\", \"GOOG\": \"C2\", \"BA\": \"k\", \"PFE\": \"r\"}\n",
    "# create the figure\n",
    "plt.figure(figsize=(8,4))\n",
    "sns.lineplot(x = 'Date', y = 'close', data = stocks5, hue = 'ticker', palette = palette, legend=False)"
   ],
   "execution_count": 11,
   "outputs": [
    {
     "output_type": "execute_result",
     "execution_count": 11,
     "data": {
      "text/plain": "<AxesSubplot:xlabel='Date', ylabel='close'>"
     },
     "metadata": {}
    },
    {
     "data": {
      "text/plain": "<Figure size 576x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 519,
       "height": 262
      }
     },
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Principal Component Analysis\n",
    "\n",
    "Kernel PCA is an unsupervised learning algorithm and allows dimensionality reduction through non-linear projections."
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00014-a7c896b4-b7ac-4a7d-a02e-5a56fc9b0411",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00009-3cc2fd7e-ade9-4db6-b759-0b3bfd6676df",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "86d9039d",
    "execution_start": 1621954339687,
    "execution_millis": 854582,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from sklearn.decomposition import KernelPCA\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "from sklearn.metrics import make_scorer\n",
    "from sklearn.metrics import mean_squared_error\n",
    "\n",
    "# adjust the training data for the Kernel PCA\n",
    "X_train_adj = X_train.drop(columns = ['Date', 'ticker'])\n",
    "X_valid_adj = X_valid.drop(columns = ['Date', 'ticker'])\n",
    "X_test_adj = X_test.drop(columns = ['Date', 'ticker'])\n",
    "\n",
    "# create the parameter grid that is to be searched\n",
    "param_grid = [{\n",
    "        \"gamma\": [0.001, 0.01, 1, 10],\n",
    "        \"kernel\": [\"rbf\", \"sigmoid\", \"linear\", \"poly\"]\n",
    "    }]\n",
    "\n",
    "# instantiate the PCA\n",
    "pca=KernelPCA(fit_inverse_transform=True, n_jobs=-1) \n",
    "\n",
    "# define scoring methid\n",
    "def my_scorer(estimator, X, y=None):\n",
    "    X_reduced = estimator.transform(X)\n",
    "    X_preimage = estimator.inverse_transform(X_reduced)\n",
    "    return -1 * mean_squared_error(X, X_preimage)\n",
    "\n",
    "# instantiate the Gridsearch object and fit the training data\n",
    "grid_search = GridSearchCV(pca, param_grid, cv=3, scoring=my_scorer)\n",
    "grid_search.fit(X_train_adj)\n",
    "\n",
    "print(\"Parameters selected by grid search: \", grid_search.best_params_)\n",
    "\n",
    "# Apply the best model selected through grid search\n",
    "# extract the model from the grid search object\n",
    "pca_model = grid_search.best_estimator_\n",
    "\n",
    "# transform the feature data \n",
    "X_train_pca = pca_model.transform(X_train_adj)\n",
    "X_valid_pca = pca_model.transform(X_valid_adj)\n",
    "X_test_pca = pca_model.transform(X_test_adj)\n",
    "\n",
    "# create new dataframes of the kernel pca data\n",
    "data_train_pca = pd.DataFrame(X_train_pca)\n",
    "data_valid_pca = pd.DataFrame(X_valid_pca)\n",
    "data_test_pca = pd.DataFrame(X_test_pca)\n",
    "\n",
    "# add the date column, tickers and target values to it\n",
    "data_train_pca['close'] = y_train\n",
    "data_train_pca['Date'] = X_train['Date']\n",
    "data_train_pca['ticker'] = X_train['ticker']\n",
    "\n",
    "data_valid_pca['close'] = y_valid\n",
    "X_valid = X_valid.reset_index(drop = True)\n",
    "data_valid_pca['Date'] = X_valid['Date']\n",
    "data_valid_pca['ticker'] = X_valid['ticker']\n",
    "\n",
    "data_test_pca['close'] = y_test\n",
    "X_test = X_test.reset_index(drop = True)\n",
    "data_test_pca['Date'] = X_test['Date']\n",
    "data_test_pca['ticker'] = X_test['ticker']\n"
   ],
   "execution_count": 12,
   "outputs": [
    {
     "name": "stdout",
     "text": "Parameters selected by grid search:  {'gamma': 1, 'kernel': 'poly'}\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Decision Tree and Random Forest\n",
    "\n",
    "We implemented a Random Forest Regressor and a Decision Tree to understand which features are the most important when predicting stock prices."
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00016-00c16fc8-0961-459e-9d61-cb80947aa38c",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00011-cd7d6948-dbed-4564-88d5-4bd3b1a4ef9f",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "c2aa3bb0",
    "execution_start": 1621955194276,
    "execution_millis": 503,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# Decision Tree for Important Features\n",
    "\n",
    "from sklearn.tree import DecisionTreeRegressor\n",
    "from matplotlib import pyplot\n",
    "\n",
    "# Using scaled but not PCA data\n",
    "X_train['Date'] = pd.to_datetime(X_train['Date'],infer_datetime_format=True)\n",
    "X_train['Date']= X_train['Date'].apply(lambda x: x.toordinal())\n",
    "X_valid['Date'] = pd.to_datetime(X_valid['Date'],infer_datetime_format=True)\n",
    "X_valid['Date']= X_valid['Date'].apply(lambda x: x.toordinal())\n",
    "X_test['Date'] = pd.to_datetime(X_test['Date'],infer_datetime_format=True)\n",
    "X_test['Date']= X_test['Date'].apply(lambda x: x.toordinal())\n",
    "\n",
    "# Dummy Variables / One hot encoding (split tickers into 5 columns)\n",
    "X_train_DT = pd.get_dummies(X_train,columns=[\"ticker\"],drop_first=False)\n",
    "X_valid_DT = pd.get_dummies(X_valid,columns=[\"ticker\"],drop_first=False)\n",
    "X_test_DT = pd.get_dummies(X_test,columns=[\"ticker\"],drop_first=False)\n",
    "\n",
    "# Establish model and fit to training set\n",
    "D_tree = DecisionTreeRegressor(max_depth=30, random_state=42)\n",
    "D_tree.fit(X_train_DT, y_train)\n",
    "\n",
    "# Get R2 of model on training set versus on validation set\n",
    "print(\"R2 of X train & y train: \", D_tree.score(X_train_DT, y_train))\n",
    "print(\"R2 of X validate & y validate: \", D_tree.score(X_valid_DT, y_valid))\n",
    "# r2 of 1 is good, 0 is useless, and negative is horrible\n",
    "\n",
    "# Use R2 for validation set as reference to try to improve performance of model\n",
    "D_tree_adj = DecisionTreeRegressor(max_depth=5, random_state=42)\n",
    "D_tree_adj.fit(X_train_DT, y_train)\n",
    "print(\"Adjusted model: R2 of X validate & y validate: \", D_tree_adj.score(X_valid_DT, y_valid))\n",
    "print(\"Adjusted model: R2 of X test & y test: \", D_tree_adj.score(X_test_DT, y_test))\n",
    "\n",
    "# Plot training versus validation set\n",
    "train_predictions_DT = D_tree_adj.predict(X_train_DT)\n",
    "test_predictions_DT = D_tree_adj.predict(X_valid_DT)\n",
    "plt.scatter(train_predictions_DT, y_train, label='train')\n",
    "plt.scatter(test_predictions_DT, y_valid, label='validate')\n",
    "plt.legend()\n",
    "plt.show()\n",
    "\n",
    "# Review feature importance scores by iterating through \n",
    "importance_DT = D_tree_adj.feature_importances_\n",
    "\n",
    "for score, name in sorted(zip(importance_DT, list(X_train_DT.columns)),reverse=True)[:54]:\n",
    "    print (name, \", Score: {:.5f}\".format(score))"
   ],
   "execution_count": 13,
   "outputs": [
    {
     "name": "stdout",
     "text": "R2 of X train & y train:  0.9796459681691083\nR2 of X validate & y validate:  -0.37337293812757477\nAdjusted model: R2 of X validate & y validate:  -0.27679681382102905\nAdjusted model: R2 of X test & y test:  -0.2776573527134216\n",
     "output_type": "stream"
    },
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 386,
       "height": 248
      }
     },
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "text": "volume , Score: 0.48751\nopen , Score: 0.20617\nmv_avg_3 , Score: 0.18670\nDowJones , Score: 0.05355\nmv_avg_5 , Score: 0.04118\nDate , Score: 0.01641\nweek_day , Score: 0.00847\nticker_PFE , Score: 0.00000\nticker_MDLZ , Score: 0.00000\nticker_GOOG , Score: 0.00000\nticker_BAC , Score: 0.00000\nticker_BA , Score: 0.00000\nS&P500 , Score: 0.00000\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00016-6da317fc-a9b4-428c-a273-62e4ace63950",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "32e1f080",
    "execution_start": 1621955194814,
    "execution_millis": 5484,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# Random Forest for Important Features\n",
    "\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from matplotlib import pyplot\n",
    "\n",
    "# Establish model and fit to training set\n",
    "RF_tree = RandomForestRegressor(max_depth=30, random_state=42)\n",
    "RF_tree.fit(X_train_DT, y_train)\n",
    "\n",
    "# Get R2 of model on training set versus on validation set\n",
    "print(\"R2 of X train & y train: \", RF_tree.score(X_train_DT, y_train))\n",
    "print(\"R2 of X validate & y validate: \", RF_tree.score(X_valid_DT, y_valid))\n",
    "# r2 of 1 is good, 0 is useless, and negative is horrible\n",
    "\n",
    "# Use R2 for validation set as reference to try to improve performance of model\n",
    "RF_tree_adj = RandomForestRegressor(max_depth=3, random_state=42)\n",
    "RF_tree_adj.fit(X_train_DT, y_train)\n",
    "print(\"Adjusted model: R2 of X validate & y validate: \", RF_tree_adj.score(X_valid_DT, y_valid))\n",
    "print(\"Adjusted model: R2 of X test & y test: \", RF_tree_adj.score(X_test_DT, y_test))\n",
    "\n",
    "# Plot training versus validation set\n",
    "train_predictions_RF = RF_tree_adj.predict(X_train_DT)\n",
    "test_predictions_RF = RF_tree_adj.predict(X_valid_DT)\n",
    "plt.scatter(train_predictions_RF, y_train, label='train')\n",
    "plt.scatter(test_predictions_RF, y_valid, label='validate')\n",
    "plt.legend()\n",
    "plt.show()\n",
    "\n",
    "# Review feature importance scores by iterating through \n",
    "importance_RF = RF_tree_adj.feature_importances_\n",
    "\n",
    "for score, name in sorted(zip(importance_RF, list(X_train_DT.columns)),reverse=True)[:54]:\n",
    "    print (name, \", Score: {:.5f}\".format(score))"
   ],
   "execution_count": 14,
   "outputs": [
    {
     "name": "stdout",
     "text": "R2 of X train & y train:  0.8349457359523627\nR2 of X validate & y validate:  -0.3126668008264166\nAdjusted model: R2 of X validate & y validate:  -0.20177466459806115\nAdjusted model: R2 of X test & y test:  -0.19570074505698032\n",
     "output_type": "stream"
    },
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 386,
       "height": 248
      }
     },
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "text": "volume , Score: 0.27733\nmv_avg_5 , Score: 0.26351\nmv_avg_3 , Score: 0.17402\nopen , Score: 0.13359\nDate , Score: 0.09250\nDowJones , Score: 0.02719\nweek_day , Score: 0.01321\nS&P500 , Score: 0.01283\nticker_GOOG , Score: 0.00364\nticker_MDLZ , Score: 0.00218\nticker_PFE , Score: 0.00000\nticker_BAC , Score: 0.00000\nticker_BA , Score: 0.00000\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### ARIMA Model\n",
    "\n",
    "We implement an ARIMA model to see whether the stock price can be predicted just by its previous values using a traditional forecasting method. \n"
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00019-c864b199-a78f-4096-8d46-dd3ff191fb57",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00012-330c2098-6da5-4e4d-8460-d238b83e09e9",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "636c8301",
    "execution_start": 1621955200309,
    "execution_millis": 100274,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# import the relevant packages\n",
    "import math\n",
    "import numpy as np\n",
    "from pmdarima.arima import auto_arima\n",
    "from pmdarima import model_selection\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error\n",
    "import time\n",
    "\n",
    "start_time = time.time()\n",
    "\n",
    "# concat the data together again to be able to split each time series \n",
    "data_pca = pd.concat([data_train_pca, data_valid_pca, data_test_pca])\n",
    "tickers = ['BAC', 'BA', 'GOOG', 'MDLZ', 'PFE']\n",
    "# iterature through the ticker list to calculate an ARIMA model for each stock series \n",
    "for ticker in tickers: \n",
    "    print(ticker)\n",
    "    # filter the data to get all stock values \n",
    "    temp = data_pca[data_pca['ticker']== ticker]\n",
    "    # train/test split \n",
    "    train, test = model_selection.train_test_split(temp['close'], train_size = 0.8)\n",
    "    # fit the model \n",
    "    model = auto_arima(train)\n",
    "    # specify forecast periods \n",
    "    forecast_periods = [test.shape[0], 5]\n",
    "    # calculate the forecasts for long-term and short-term prediction horizon \n",
    "    for period in forecast_periods: \n",
    "        if period == 5: \n",
    "            print(\"Short-Term Forecasts: \")\n",
    "        else: \n",
    "            print(\"Long-Term Forecasts: \")\n",
    "        # predict\n",
    "        print(\"Number of forecast periods: \" + str(period))\n",
    "        preds = model.predict(n_periods = period, return_conf_int = False)\n",
    "        # calculate and print the RMSE and MAE \n",
    "        if period == 5: \n",
    "            mae = mean_absolute_error(test.iloc[:5,], preds)\n",
    "            rmse = np.sqrt(mean_squared_error(test.iloc[:5,],preds))\n",
    "        else:\n",
    "            mae = mean_absolute_error(test, preds)\n",
    "            rmse = np.sqrt(mean_squared_error(test,preds))\n",
    "        print('Test MAE: %.3f' % mae)\n",
    "        print('Test RMSE: %.3f' % rmse)\n",
    "print(\"--- %s seconds ---\" % (time.time() - start_time))"
   ],
   "execution_count": 15,
   "outputs": [
    {
     "name": "stdout",
     "text": "BAC\nLong-Term Forecasts: \nNumber of forecast periods: 221\nTest MAE: 0.003\nTest RMSE: 0.004\nShort-Term Forecasts: \nNumber of forecast periods: 5\nTest MAE: 0.003\nTest RMSE: 0.004\nBA\nLong-Term Forecasts: \nNumber of forecast periods: 221\nTest MAE: 0.030\nTest RMSE: 0.040\nShort-Term Forecasts: \nNumber of forecast periods: 5\nTest MAE: 0.027\nTest RMSE: 0.030\nGOOG\nLong-Term Forecasts: \nNumber of forecast periods: 221\nTest MAE: 0.171\nTest RMSE: 0.235\nShort-Term Forecasts: \nNumber of forecast periods: 5\nTest MAE: 0.168\nTest RMSE: 0.199\nMDLZ\nLong-Term Forecasts: \nNumber of forecast periods: 221\nTest MAE: 0.003\nTest RMSE: 0.004\nShort-Term Forecasts: \nNumber of forecast periods: 5\nTest MAE: 0.006\nTest RMSE: 0.006\nPFE\nLong-Term Forecasts: \nNumber of forecast periods: 221\nTest MAE: 0.003\nTest RMSE: 0.004\nShort-Term Forecasts: \nNumber of forecast periods: 5\nTest MAE: 0.003\nTest RMSE: 0.005\n--- 100.04920387268066 seconds ---\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Logistic Regression\n",
    "\n",
    "The Logistic Regression classifes the data according to the target variable \"Price change\", with \"Price change\" being either an increase or decrease. "
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00022-5c47c86d-c869-476f-8eed-45fb1d2056ee",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00006-519b420a-3f17-4604-b795-be407844e0ae",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "eae09dd3",
    "execution_start": 1621955300612,
    "execution_millis": 42407,
    "output_cleared": false,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from sklearn.linear_model import LogisticRegression\n",
    "\n",
    "#Logistic Regression\n",
    "from sklearn import preprocessing\n",
    "from sklearn import utils\n",
    "from sklearn import metrics\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "\n",
    "# calculate the target variable for logistic regression \n",
    "# 1 is price increase, 0 is price decrease\n",
    "\n",
    "# sort by ticker \n",
    "data_train_pca = data_train_pca.sort_values(by=['ticker', 'Date'])\n",
    "data_valid_pca = data_valid_pca.sort_values(by=['ticker', 'Date'])\n",
    "data_test_pca = data_test_pca.sort_values(by=['ticker', 'Date'] )\n",
    "\n",
    "# calculate increase/decrease\n",
    "data_train_pca['Price change'] = (data_train_pca['close'].diff()).apply(lambda x: \"1\" if x > 0 else \"0\").shift(-1)\n",
    "data_valid_pca['Price change'] = (data_valid_pca['close'].diff()).apply(lambda x: \"1\" if x > 0 else \"0\").shift(-1)\n",
    "data_test_pca['Price change'] = (data_test_pca['close'].diff()).apply(lambda x: \"1\" if x > 0 else \"0\").shift(-1)\n",
    "\n",
    "# remove rows with nan from y and x \n",
    "data_train_pca = data_train_pca.dropna(subset = ['Price change'])\n",
    "data_valid_pca = data_valid_pca.dropna(subset = ['Price change'])\n",
    "data_test_pca = data_test_pca.dropna(subset = ['Price change'])\n",
    "\n",
    "# prepare training, testing and validation data\n",
    "X_train_pca = data_train_pca.drop(columns = ['Date', 'close', 'ticker','Price change'])\n",
    "y_train_pca = data_train_pca['Price change']\n",
    "X_valid_pca = data_valid_pca.drop(columns = ['Date', 'close', 'ticker', 'Price change'])\n",
    "y_valid_pca = data_valid_pca['Price change']\n",
    "X_test_pca = data_test_pca.drop(columns = ['Date', 'close', 'ticker', 'Price change'])\n",
    "y_test_pca = data_test_pca['Price change']\n",
    "\n",
    "# instantiate model \n",
    "lr_model = LogisticRegression(max_iter = 1000, random_state=42)\n",
    "\n",
    "# Build GridSearch Pipeline\n",
    "param_values = {'C': [0.001,0.01,0.1,1,10,100,1000]}\n",
    "\n",
    "grid = GridSearchCV(lr_model, param_grid= param_values)\n",
    "# fit the model with data\n",
    "%time grid.fit(X_train_pca,y_train_pca)\n",
    "\n",
    "# evaluate the performance on the test set\n",
    "y_pred_valid = grid.predict(X_test_pca)\n",
    "\n",
    "# best estimator \n",
    "grid.best_estimator_\n",
    "# LogisticRegression(C=0.001, max_iter=1000, random_state=42)\n",
    "\n",
    "# best parameters \n",
    "grid.best_params_\n",
    "\n",
    "# plot the conclusion matric\n",
    "metrics.plot_confusion_matrix(grid, X_test_pca, y_test_pca, labels = [\"0\", \"1\"])\n",
    "plt.show()\n",
    "\n",
    "# show the classification report \n",
    "clf_report = metrics.classification_report(y_test_pca, y_pred_valid, labels = [\"0\", \"1\"])\n",
    "print(clf_report)\n",
    "\n",
    "# calculate even more metrics\n",
    "metrics = metrics.precision_recall_fscore_support(y_test_pca, y_pred_valid)\n",
    "\n",
    "\n",
    "print(\"Precision: \" + str(metrics[0]))\n",
    "print(\"Recall: \" +  str(metrics[1]))\n",
    "print(\"F-Score: \" + str(metrics[2]))\n",
    "print(\"Support: \" + str(metrics[3]))\n"
   ],
   "execution_count": 16,
   "outputs": [
    {
     "name": "stdout",
     "text": "CPU times: user 38.1 s, sys: 24.9 s, total: 1min 3s\nWall time: 42 s\n",
     "output_type": "stream"
    },
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 2 Axes>",
      "image/png": "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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 312,
       "height": 262
      }
     },
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "text": "              precision    recall  f1-score   support\n\n           0       0.50      0.96      0.66       278\n           1       0.37      0.03      0.05       273\n\n    accuracy                           0.50       551\n   macro avg       0.43      0.49      0.35       551\nweighted avg       0.43      0.50      0.36       551\n\nPrecision: [0.5        0.36842105]\nRecall: [0.95683453 0.02564103]\nF-Score: [0.65679012 0.04794521]\nSupport: [278 273]\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Support Vector Regression (SVR)\n",
    "\n",
    "We use a Support Vector Regression to predict continuous stock prices with a Support Vector Machine. "
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00024-b880e6a7-95e3-4eda-8da2-502d4bd166ba",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00018-acc13f6c-9373-4947-bb28-c45a57957452",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "fd6610b3",
    "execution_start": 1621955343034,
    "execution_millis": 7415,
    "deepnote_cell_type": "code"
   },
   "source": [
    "from sklearn.svm import SVR\n",
    "from sklearn import metrics\n",
    "from sklearn.model_selection import PredefinedSplit\n",
    "from sklearn.model_selection import RandomizedSearchCV\n",
    "\n",
    "# prepare training, testing and validation data\n",
    "X_train_svr = data_train_pca.drop(columns = ['Date', 'close', 'ticker', 'Price change'])\n",
    "X_valid_svr = data_valid_pca.drop(columns = ['Date', 'close', 'ticker', 'Price change'])\n",
    "X_test_svr = data_test_pca.drop(columns = ['Date', 'close', 'ticker', 'Price change'])\n",
    "y_train_svr = data_train_pca['close']\n",
    "y_valid_svr = data_valid_pca['close']\n",
    "y_test_svr = data_test_pca[\"close\"]\n",
    "\n",
    "\n",
    "# Set up model\n",
    "svr = SVR()\n",
    "\n",
    "X_check_svr = pd.concat([X_train_svr, X_valid_svr], ignore_index=True)\n",
    "y_check_svr = np.concatenate((y_train_svr, y_valid_svr))\n",
    "\n",
    "# Create a list where train data indices are -1 and validation data indices are 0\n",
    "split_index = [-1 if x in X_train_svr.index else 0 for x in X_check_svr.index]\n",
    "\n",
    "# Use the list to create PredefinedSplit\n",
    "pds = PredefinedSplit(test_fold = split_index)\n",
    "\n",
    "# Use a grid search cross-validation to explore combinations of parameters\n",
    "\n",
    "param_grid = {'kernel': ['poly', 'rbf', 'sigmoid'],\n",
    "             'C': [0.001, 0.1, 1, 10, 100],\n",
    "             'gamma': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1],\n",
    "            'epsilon': [0.01, 0.1, 1]}\n",
    "            \n",
    "grid = RandomizedSearchCV(estimator=svr, cv=pds, param_distributions=param_grid, n_jobs = -1, random_state=42)\n",
    "\n",
    "%time grid.fit(X_check_svr, y_check_svr)\n",
    "print(grid.best_params_)"
   ],
   "execution_count": 17,
   "outputs": [
    {
     "name": "stdout",
     "text": "CPU times: user 1.01 s, sys: 52.1 ms, total: 1.06 s\nWall time: 7.4 s\n{'kernel': 'sigmoid', 'gamma': 0.001, 'epsilon': 0.01, 'C': 1}\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00021-09058563-08f7-4a2b-8b9e-d9ae81ac08df",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "4b201e23",
    "execution_start": 1621955350453,
    "execution_millis": 90,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# Use cross-validated model to predict the labels for the test data, which the model has not yet seen:\n",
    "\n",
    "svr_model = grid.best_estimator_\n",
    "y_pred_svr = svr_model.predict(X_test_svr)\n",
    "\n",
    "from sklearn.metrics import r2_score\n",
    "# regression score function, best possible score is 1\n",
    "print(\"R2 score:\", r2_score(y_test_svr, y_pred_svr))\n",
    "\n",
    "from sklearn.metrics import mean_absolute_error\n",
    "# average magnitude of the errors, best possible score is 0\n",
    "print(\"Mean absolute error:\", mean_absolute_error(y_test_svr, y_pred_svr))\n",
    "\n",
    "from sklearn.metrics import mean_squared_error\n",
    "# RMSE, the distance, on average, of a data point from the fitted line, measured along a vertical line.\n",
    "print(\"Root mean squared error:\", mean_squared_error(y_test_svr, y_pred_svr, squared = False))\n",
    "\n",
    "#The RMSE will always be larger or equal to the MAE; the greater difference between them, the greater the variance in the individual errors in the sample."
   ],
   "execution_count": 18,
   "outputs": [
    {
     "name": "stdout",
     "text": "R2 score: 0.0191881098639628\nMean absolute error: 0.04528851741697144\nRoot mean squared error: 0.11455298771054803\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00018-fa0f1857-2b85-4b36-96d7-801879be831e",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "3482a04f",
    "execution_start": 1621955350545,
    "execution_millis": 26,
    "deepnote_cell_type": "code"
   },
   "source": [
    "# look at values of predictions versus true y test data\n",
    "comparison = pd.DataFrame(y_test_svr)\n",
    "#comparison.rename(columns = {'close':'test'}, inplace = True)\n",
    "y_pred_svr = pd.DataFrame(y_pred_svr)\n",
    "comparison['prediction'] = y_pred_svr\n",
    "print(comparison)\n",
    "\n",
    "under_pred = comparison.query('close > prediction').count()\n",
    "print(\"Number of under predictions: \", under_pred['close'])\n",
    "\n",
    "over_pred = comparison.query('prediction > close').count()\n",
    "print(\"Number of over predictions: \", over_pred['close'])\n",
    "\n",
    "accurate_pred = comparison.query('prediction == close').count()\n",
    "print(\"Accurate predictions: \", accurate_pred['close'])\n",
    "\n",
    "# see an average of how much stock prices rise/fall and the min and max\n",
    "pred_diff = []\n",
    "pred_diff = comparison['prediction'].sub(comparison['close'], axis = 0)\n",
    "print(\"Average of scaled stock price differences between prediction and actual close: \", pred_diff.mean())\n",
    "print(\"Smallest difference between scaled prediction and close: \", min(abs(pred_diff)))\n",
    "print(\"Largest difference between scaled prediction and close: \", max(abs(pred_diff)))"
   ],
   "execution_count": 19,
   "outputs": [
    {
     "name": "stdout",
     "text": "        close  prediction\n1   -0.055260   -0.026633\n4   -0.038063   -0.024971\n7   -0.019427   -0.025285\n12  -0.051878   -0.024655\n18  -0.059073   -0.024394\n..        ...         ...\n523 -0.026335   -0.016881\n529 -0.025112   -0.014778\n535 -0.026191   -0.013781\n537 -0.027342   -0.016812\n544 -0.023673   -0.016104\n\n[551 rows x 2 columns]\nNumber of under predictions:  154\nNumber of over predictions:  397\nAccurate predictions:  0\nAverage of scaled stock price differences between prediction and actual close:  -2.064976292493721e-05\nSmallest difference between scaled prediction and close:  5.000503270499723e-06\nLargest difference between scaled prediction and close:  1.0132891465361604\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "### Neural Network: Long-Term Short-Term Memory (LSTM)\n",
    "\n",
    "LSTM is a type of Recurrent Neural Networks (RNN) used in the field of supervised Deep Learning and can store long-term information about the data, it is therefore better suited for long-term forecasts than ARIMA. "
   ],
   "metadata": {
    "tags": [],
    "cell_id": "00029-c50b120f-d841-4bae-b327-43706a7cf52a",
    "deepnote_cell_type": "markdown"
   }
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00024-518428b6-1fb0-4354-99a2-ba6f5f7ce1e4",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "89328b6f",
    "execution_start": 1621955350613,
    "execution_millis": 4234,
    "deepnote_cell_type": "code"
   },
   "source": [
    "import tensorflow as tf\n",
    "from tensorflow import keras\n",
    "from tensorflow.keras import layers\n",
    "from tensorflow.keras import activations\n",
    "\n",
    "from sklearn.metrics import mean_squared_error\n",
    "#from sklearn.metrics import accuracy_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "from tensorflow.keras import optimizers\n",
    "from sklearn import preprocessing\n",
    "#from joblib import dump, load\n",
    "import plotly.express as px\n",
    "\n",
    "#define train, test and valid set\n",
    "X_train_f = X_train_pca\n",
    "X_test_f = X_test_pca\n",
    "X_valid_f = X_valid_pca\n",
    "\n",
    "y_train_f = data_train_pca['close']\n",
    "y_test_f = data_test_pca['close']\n",
    "y_valid_f = data_valid_pca['close']\n",
    "\n",
    "\n",
    "#create time lags\n",
    "def create_dataset(X, y, time_steps=1):\n",
    "    Xs, ys = [], []\n",
    "    for i in range(len(X) - time_steps):\n",
    "        v = X[i:(i + time_steps)]\n",
    "        Xs.append(v)\n",
    "        ys.append(y[i + time_steps])\n",
    "    return np.array(Xs), np.array(ys)\n",
    "\n",
    "time_steps = 30\n",
    "# reshape to [samples, time_steps, n_features]\n",
    "X_train_f, y_train_f = create_dataset(X_train_f, y_train_f, time_steps)\n",
    "X_test_f, y_test_f = create_dataset(X_test_f, y_test_f, time_steps)\n",
    "\n",
    "print(\"*** SHAPES\")\n",
    "print(X_train_f.shape, y_train_f.shape)\n",
    "print(X_test_f.shape, y_test_f.shape)\n",
    "\n",
    "# Building the model\n",
    "model = keras.Sequential()\n",
    "model.add(keras.Input(shape=((X_train_f.shape[1], X_test_f.shape[2])))) #input shape\n",
    "\n",
    "model.add(layers.LSTM(300, return_sequences=False, activation = 'tanh'))\n",
    "model.add(layers.BatchNormalization())\n",
    "\n",
    "model.add(keras.layers.Dense(units=1))\n",
    "model.compile(loss='mean_squared_error', optimizer='adam')\n",
    "model.summary()"
   ],
   "execution_count": 20,
   "outputs": [
    {
     "name": "stdout",
     "text": "*** SHAPES\n(4384, 30, 116) (4384,)\n(521, 30, 116) (521,)\nModel: \"sequential\"\n_________________________________________________________________\nLayer (type)                 Output Shape              Param #   \n=================================================================\nlstm (LSTM)                  (None, 300)               500400    \n_________________________________________________________________\nbatch_normalization (BatchNo (None, 300)               1200      \n_________________________________________________________________\ndense (Dense)                (None, 1)                 301       \n=================================================================\nTotal params: 501,901\nTrainable params: 501,301\nNon-trainable params: 600\n_________________________________________________________________\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00016-d767e8e5-214f-402d-be8e-69db72923bbb",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "cbc46ee8",
    "execution_start": 1621955354842,
    "execution_millis": 372586,
    "output_cleared": false,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#fit the model\n",
    "hist = model.fit(X_train_f, y_train_f, batch_size = 200, epochs = 50, shuffle=False, validation_split=0.1)\n"
   ],
   "execution_count": 21,
   "outputs": [
    {
     "name": "stdout",
     "text": "Epoch 1/50\n20/20 [==============================] - 10s 414ms/step - loss: 2.0016 - val_loss: 0.0525\nEpoch 2/50\n20/20 [==============================] - 7s 362ms/step - loss: 2.2187 - val_loss: 0.0834\nEpoch 3/50\n20/20 [==============================] - 7s 362ms/step - loss: 2.1040 - val_loss: 0.0456\nEpoch 4/50\n20/20 [==============================] - 7s 354ms/step - loss: 1.6869 - val_loss: 0.0466\nEpoch 5/50\n20/20 [==============================] - 7s 353ms/step - loss: 1.0928 - val_loss: 0.0391\nEpoch 6/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.8070 - val_loss: 0.0567\nEpoch 7/50\n20/20 [==============================] - 7s 357ms/step - loss: 0.6966 - val_loss: 0.0409\nEpoch 8/50\n20/20 [==============================] - 7s 358ms/step - loss: 0.5708 - val_loss: 0.2222\nEpoch 9/50\n20/20 [==============================] - 7s 357ms/step - loss: 1.1280 - val_loss: 0.1328\nEpoch 10/50\n20/20 [==============================] - 7s 355ms/step - loss: 1.6744 - val_loss: 0.3288\nEpoch 11/50\n20/20 [==============================] - 7s 353ms/step - loss: 1.1953 - val_loss: 0.0398\nEpoch 12/50\n20/20 [==============================] - 7s 358ms/step - loss: 0.5793 - val_loss: 0.3352\nEpoch 13/50\n20/20 [==============================] - 7s 357ms/step - loss: 0.5158 - val_loss: 0.1060\nEpoch 14/50\n20/20 [==============================] - 7s 355ms/step - loss: 0.3184 - val_loss: 0.1099\nEpoch 15/50\n20/20 [==============================] - 7s 359ms/step - loss: 0.2505 - val_loss: 0.0261\nEpoch 16/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.2211 - val_loss: 0.0678\nEpoch 17/50\n20/20 [==============================] - 7s 347ms/step - loss: 0.0615 - val_loss: 0.0334\nEpoch 18/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0191 - val_loss: 0.0408\nEpoch 19/50\n20/20 [==============================] - 7s 347ms/step - loss: 0.0129 - val_loss: 0.0262\nEpoch 20/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0088 - val_loss: 0.0349\nEpoch 21/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0075 - val_loss: 0.0253\nEpoch 22/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0064 - val_loss: 0.0273\nEpoch 23/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0061 - val_loss: 0.0285\nEpoch 24/50\n20/20 [==============================] - 7s 363ms/step - loss: 0.0057 - val_loss: 0.0257\nEpoch 25/50\n20/20 [==============================] - 7s 357ms/step - loss: 0.0054 - val_loss: 0.0271\nEpoch 26/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0051 - val_loss: 0.0282\nEpoch 27/50\n20/20 [==============================] - 7s 354ms/step - loss: 0.0051 - val_loss: 0.0262\nEpoch 28/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0050 - val_loss: 0.0274\nEpoch 29/50\n20/20 [==============================] - 7s 365ms/step - loss: 0.0052 - val_loss: 0.0280\nEpoch 30/50\n20/20 [==============================] - 7s 376ms/step - loss: 0.0058 - val_loss: 0.0264\nEpoch 31/50\n20/20 [==============================] - 7s 371ms/step - loss: 0.0067 - val_loss: 0.0277\nEpoch 32/50\n20/20 [==============================] - 7s 359ms/step - loss: 0.0074 - val_loss: 0.0294\nEpoch 33/50\n20/20 [==============================] - 7s 372ms/step - loss: 0.0079 - val_loss: 0.0277\nEpoch 34/50\n20/20 [==============================] - 11s 575ms/step - loss: 0.0082 - val_loss: 0.0268\nEpoch 35/50\n20/20 [==============================] - 13s 665ms/step - loss: 0.0089 - val_loss: 0.0308\nEpoch 36/50\n20/20 [==============================] - 10s 483ms/step - loss: 0.0108 - val_loss: 0.0267\nEpoch 37/50\n20/20 [==============================] - 8s 383ms/step - loss: 0.0130 - val_loss: 0.0310\nEpoch 38/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0175 - val_loss: 0.0344\nEpoch 39/50\n20/20 [==============================] - 7s 359ms/step - loss: 0.0229 - val_loss: 0.0284\nEpoch 40/50\n20/20 [==============================] - 7s 356ms/step - loss: 0.0308 - val_loss: 0.0310\nEpoch 41/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0443 - val_loss: 0.0305\nEpoch 42/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0452 - val_loss: 0.0590\nEpoch 43/50\n20/20 [==============================] - 7s 354ms/step - loss: 0.0440 - val_loss: 0.0483\nEpoch 44/50\n20/20 [==============================] - 7s 353ms/step - loss: 0.0322 - val_loss: 0.0336\nEpoch 45/50\n20/20 [==============================] - 7s 355ms/step - loss: 0.0243 - val_loss: 0.0910\nEpoch 46/50\n20/20 [==============================] - 7s 357ms/step - loss: 0.0452 - val_loss: 0.0326\nEpoch 47/50\n20/20 [==============================] - 7s 358ms/step - loss: 0.0281 - val_loss: 0.1117\nEpoch 48/50\n20/20 [==============================] - 7s 358ms/step - loss: 0.0682 - val_loss: 0.0973\nEpoch 49/50\n20/20 [==============================] - 7s 358ms/step - loss: 0.0585 - val_loss: 0.0590\nEpoch 50/50\n20/20 [==============================] - 7s 355ms/step - loss: 0.0591 - val_loss: 0.1846\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00017-4bbc8477-0195-4892-92e9-76bcb850622d",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "f7120a2a",
    "execution_start": 1621955727469,
    "execution_millis": 171,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#plot loss of training and validation set\n",
    "loss = hist.history['loss']\n",
    "val_loss = hist.history['val_loss']\n",
    "epochs = range(1, len(loss) + 1)\n",
    "plt.plot(epochs, loss, 'bo', label='Training loss')\n",
    "plt.plot(epochs, val_loss, 'b', label='Validation loss')\n",
    "plt.title('Training and validation loss')\n",
    "plt.xlabel('Epochs')\n",
    "plt.ylabel('Loss')\n",
    "plt.legend()\n",
    "plt.show()"
   ],
   "execution_count": 22,
   "outputs": [
    {
     "data": {
      "text/plain": "<Figure size 432x288 with 1 Axes>",
      "image/png": "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2LFjB8OHD2ft2rUcd9xxLF26lC5dujBp0iTuueeetG6zKgoEIpJWmWqX27p1K126dAHgrrvuSvv6e/fuzdtvv826desAeOCBB6pdZsSIEcyNGkeWLFlCp06dOOCAA3jrrbc46qijuPrqqxk8eDBr165l/fr1HHzwwVx44YVccMEFrFixIu37kIwCgYikVWEhzJkDPXqAWXieMyf+6tmrrrqKa665hgEDBqT9DB6gVatW3HLLLZxyyikMGjSItm3bcuCBB1a5zIwZM1i+fDn9+vVj2rRp3H333QDceOONHHnkkfTr14/mzZszatQolixZQv/+/RkwYAAPPPAAl1xySdr3IZlGd8/igoIC141pROrX66+/zje/+c1MZyPjtm/fTps2bXB3LrroInr16sVll12W6Wzto7Lvy8yWu3tBZfOrRCAikqJbb72V/Px8+vbty9atW/nhD3+Y6SylRWy9hsysG3APcDDgwBx3/22FeUYCfwbeiZL+5O7Xx5UnEZG6uOyyyxpkCaCu4iwR7AKucPcjgKOBi8zsiErmW+bu+dGj3oOARiYVkVwXW4nA3TcCG6PXxWb2OtAFeC2ubdaURiYVEamnNgIzywMGAC9W8vYwM3vVzBaZWd8ky082syIzK9q0aVPa8qWRSUVE6iEQmFkb4GHgUnffVuHtFUAPd+8P/A8wv7J1uPscdy9w94LOnTunLW8amVREJOZAYGbNCUFgrrv/qeL77r7N3bdHrxcCzc2sU5x5SqSRSUUahxNOOIEnnniiXNqNN97I1KlTky4zcuRISruajx49mi1btuwzz4wZM5g1a1aV254/fz6vvVZWo/2zn/2Mp59+uga5r1xDGq46tkBg4TY5twOvu/uvk8zztWg+zGxIlJ/NceWpIo1MKtI4TJgwgXnz5pVLmzdvXkoDv0EYNbRdu3a12nbFQHD99ddz8skn12pdDVWcJYLhwLnAiWa2MnqMNrMpZjYlmmc8sNrMXgVmA+d4PV7hlqkrIEWkZsaPH8/jjz++9yY069at44MPPmDEiBFMnTqVgoIC+vbty3XXXVfp8nl5eXzyyScAzJw5k8MPP5xjjz1271DVEK4RGDx4MP379+eMM86gpKSEF154gQULFnDllVeSn5/PW2+9xaRJk3jooYcAeOaZZxgwYABHHXUU559/Pl9++eXe7V133XUMHDiQo446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\n"
     },
     "metadata": {
      "needs_background": "light",
      "image/png": {
       "width": 386,
       "height": 278
      }
     },
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00018-7afa8ea6-3e37-4aec-a0b9-844898533949",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "4ec14dcb",
    "execution_start": 1621955727636,
    "execution_millis": 1792,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#make prediction from model\n",
    "y_pred = model.predict(X_test_f)\n",
    "\n",
    "#evaluate performance of model\n",
    "y_test_f = y_test_f.reshape(-1,1)\n",
    "y_test_inv = t_transformer.inverse_transform(y_test_f)\n",
    "y_pred_inv = t_transformer.inverse_transform(y_pred)\n",
    "\n",
    "results = model.evaluate(X_test_f, y_test_f)\n",
    "print(\"mse: %s\" % (mean_squared_error(y_test_inv, y_pred_inv)))\n",
    "print(results)"
   ],
   "execution_count": 23,
   "outputs": [
    {
     "name": "stdout",
     "text": "17/17 [==============================] - 1s 32ms/step - loss: 2.3282\nmse: 44969.99433302891\n2.3281869888305664\n",
     "output_type": "stream"
    }
   ]
  },
  {
   "cell_type": "code",
   "metadata": {
    "tags": [],
    "cell_id": "00018-0b60daf1-2288-4f63-ba9e-9f2cf80947be",
    "deepnote_to_be_reexecuted": false,
    "source_hash": "85e92ac6",
    "execution_start": 1621955729427,
    "execution_millis": 1210,
    "deepnote_cell_type": "code"
   },
   "source": [
    "#plot actual vs. predicted stock prices\n",
    "a = np.repeat(1, len(y_test_f))\n",
    "b = np.repeat(2, len(y_pred))\n",
    "\n",
    "# prepare data for visualization \n",
    "df1 = pd.DataFrame(data = np.concatenate((y_test_inv,(np.reshape(a, (-1, 1)))),axis=1), columns=[\"price\",\"type\"])\n",
    "df2 = pd.DataFrame(data = np.concatenate((y_pred_inv,(np.reshape(b, (-1, 1)))),axis=1), columns=[\"price\",\"type\"])\n",
    "\n",
    "frames = [df1, df2]\n",
    "result = pd.concat(frames, ignore_index=False)\n",
    "\n",
    "result[\"type\"].replace({1: \"actual\", 2: \"predict\"}, inplace=True)\n",
    "(result[result.type == \"actual\"]).head(10)\n",
    "\n",
    "# create figure\n",
    "fig = px.line(result, x=result.index.values, y=\"price\", color='type', title='Stock Price')\n",
    "fig.show()"
   ],
   "execution_count": 24,
   "outputs": [
    {
     "data": {
      "text/html": "<html>\n<head><meta charset=\"utf-8\" /></head>\n<body>\n    <div>            <script src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG\"></script><script type=\"text/javascript\">if (window.MathJax) {MathJax.Hub.Config({SVG: {font: \"STIX-Web\"}});}</script>                <script type=\"text/javascript\">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>\n        <script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>                <div id=\"f114c863-2eb4-4679-9591-5b462552c46e\" class=\"plotly-graph-div\" style=\"height:525px; width:100%;\"></div>            <script type=\"text/javascript\">                                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById(\"f114c863-2eb4-4679-9591-5b462552c46e\")) {                    Plotly.newPlot(                        \"f114c863-2eb4-4679-9591-5b462552c46e\",                        [{\"hovertemplate\": \"type=actual<br>x=%{x}<br>price=%{y}<extra></extra>\", \"legendgroup\": \"actual\", \"line\": {\"color\": \"#636efa\", \"dash\": \"solid\"}, \"mode\": \"lines\", \"name\": \"actual\", \"showlegend\": true, \"type\": \"scattergl\", \"x\": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520], \"xaxis\": \"x\", \"y\": [-0.299999237060547, 1.069999694824219, -0.6399993896484374, -0.5299987792968465, -0.5200004577636721, -0.5300006866455076, -15.869995117187502, 0.8400001525878905, 8.8800048828125, 0.18999862670897724, 0.6999969482421807, 0.910003662109375, 6.469970703125, 0.5000000000000001, -0.09000015258789058, -0.1699981689453053, -2.5400085449218466, 37.23999023437499, 0.1700000762939452, 0.4200019836425854, -0.45000076293945296, -1.0599975585937498, 0.1600036621093466, -0.11999893188476198, 0.18000030517578117, -17.369995117187496, 0.22999954223632835, -0.030000686645511285, -19.199951171875, -0.45000076293945296, 0.41999816894531233, -0.30999755859374983, 12.3599853515625, 0.3299999237060544, 0.4700012207031249, 0.06999969482421865, -2.610000610351591, -0.5500030517578126, -23.6400146484375, 0.0, -0.27999877929687506, -11.339996337890597, 0.22999954223633173, 0.3799972534179617, 0.06000137329101582, 8.910003662109375, 12.6800537109375, 1.8900012969970668, -5.630004882812499, -0.3199996948242117, -0.11000061035156253, -0.6000061035156251, 0.709999084472656, 51.95996093750001, -0.11000061035156253, 0.1900024414062498, 1.6800079345703125, -0.33000183105468756, 0.43000030517577426, -2.810012817382784, 0.06999969482421865, 19.9599609375, 0.5400009155273435, -1.0999984741210869, -3.110000610351591, -40.489990234375, 0.6399993896484374, -0.5900001525878907, 0.22999954223632835, 0.5900001525878907, 1.620010375976534, -20.169921875, -0.20000076293945312, -1.199996948242159, -0.31999969482421897, 7.8499755859375, 0.04999923706054671, 2.699996948242159, 0.5300025939941407, -14.219970703125002, -0.11000061035156253, -0.059997558593750014, -0.09000015258789058, -5.5899963378905975, -0.04999923706054671, -3.9901123046875, -0.9800033569335936, 6.3899993896484375, 0.029998779296874764, -0.08000183105468728, 54.6700439453125, -0.2399978637695312, -0.04000091552735063, -0.22999954223632835, 96.0400390625, 0.7399902343750001, -0.43000030517578147, -4.039993286132841, -0.02000045776367194, -0.9799995422363216, 4.3499755859375, -0.5699996948242188, 0.06999969482421865, -0.22000122070312506, 0.13000106811523446, 9.800048828125, -1.5700073242186938, -2.479995727539062, 0.7299995422363352, -1.6500244140624998, -0.3899993896484376, 0.6199989318847655, 0.7200012207031252, -1.300003051757869, 0.030002593994133343, -0.21999931335449238, 17.8399658203125, -1.110000610351566, -86.449951171875, -1.0699996948242183, -1.1700019836425781, -8.029998779296847, 32.3199462890625, 3.199996948242159, -0.38000106811523426, 0.4899997711181675, 0.7000007629394532, -27.369995117187496, 0.04000091552734388, -0.670000076293942, -1.680000305175788, -3.039993286132784, 0.3099994659423791, -0.18999862670897724, 1.6499938964844034, 65.60998535156227, -0.10000228881835922, 5.100006103515597, 1.0700016021728516, 0.9099998474121092, 26.160034179687727, -0.8099975585937504, 6.4499969482421875, 0.5499992370605434, -0.8800010681152272, 142.56005859375, -0.15000152587890642, 0.920000076293949, 0.7200012207031179, -7.699951171875, 0.04999923706054671, 3.25, 0.029998779296874764, 0.20999908447265642, -2.710006713867187, -0.13000106811523446, 35.6298828125, 4.0200042724609375, -5.090087890625, 0.7200012207031252, -0.09999847412109389, -0.18999862670898449, -9.39990234375, 0.15000152587890642, 3.1699981689453125, -0.1399993896484373, -0.5200004577636721, -3.1999969482421875, 0.029998779296874764, 11.869873046875, -0.22999954223632835, -0.2499999999999998, -1.2599945068359655, -0.09999847412109389, 0.5100097656249999, -0.3100013732910156, 0.43000030517578147, -0.49000167846680404, 0.2900009155273437, 0.48999786376953103, 8.22021484375, 0.31999206542968733, 17.789794921875, 0.9000015258789064, -0.30999755859374306, -0.030002593994140576, 6.199996948242216, 0.1399993896484373, 0.03999710083007807, 6.41015625, 0.20000076293945312, -1.6599884033203411, 1.210002899169922, -11.110107421875, -0.32999801635742176, -0.22000122070312506, -7.040008544921875, 8.990005493164091, -1.8199996948242183, -0.12000274658203117, 0.35000228881835954, -16.06005859375, -4.589996337890625, 0.009998321533203305, -0.18000030517578117, 0.6100006103515626, -36.260009765625, 0.3699989318847656, 0.4799995422363282, -0.3499984741210937, -0.7600097656250002, 5.980224609375, -0.46999740600585954, 0.8600006103515625, 17.220001220703153, -0.15999984741210924, 24.309814453125, 0.06999969482421865, -0.2900009155273437, -12.889999389648466, -0.45000076293945296, -63.8099365234375, -1.2200012207031252, -0.32999801635742176, -4.440002441406222, 5.5, -0.8800010681152349, 44.6500244140625, 0.5000000000000001, 1.0800018310546875, 12.380004882812472, 0.1999969482421873, -0.2600021362304689, -1.2500000000000004, -5.669921875, 0.02000045776367194, -0.18000030517578117, 0.8899993896484373, -49.130126953125, 0.8800010681152344, -0.7400016784668039, 5.419998168945284, -0.18999862670898449, 1.020000457763679, 22.380126953125, -3.8499908447265345, 0.08000183105468728, 0.18999862670898449, 1.6200027465820312, 59.449951171875, -1.4900054931640618, 0.43000030517578147, 0.80999755859375, 0.20000076293945312, -84.3699951171875, -0.04000091552734388, -0.43000030517578147, 0.46999740600585954, 28.5299072265625, 6.580001831054716, 0.10000228881835922, -0.8100013732910157, 0.4799995422363282, 1.0499992370605469, 0.5699996948242115, 14.729995727539062, 2.330078125, 59.739990234375, 6.660003662109347, 0.08000183105469451, -0.12999725341796867, -0.22000122070312506, 17.19000244140625, 0.599998474121094, -52.85009765625, 0.6999969482421807, 0.22999954223632835, -3.55999755859375, 4.570068359375001, 0.4700012207031249, 0.36000061035156233, -0.18999862670897724, 26.030029296875, 0.4200019836425782, 0.5499992370605541, -10.419998168945312, -0.11000061035156253, -0.04000091552734388, 0.13999938964843053, -1.4399414062500002, 0.3100013732910156, 8.379989624023438, -54.860107421875, -0.009998321533203305, 0.9899978637695239, -7.529998779296931, -0.02000045776367194, 6.97998046875, 0.18999862670897724, -0.40999984741209505, -0.23999023437494316, -0.24000167846679699, -0.869998931884773, 0.7400016784668039, -4.6099853515625, -4.590011596679716, 0.4700012207031249, -0.6399993896484374, -0.24000167846680376, 14.3699951171875, -9.979995727539034, -0.7599983215332032, 0.2499999999999998, -0.5399971008300709, 0.0, -7.899902343750001, -2.0099945068359095, -0.7000732421874998, 0.7599983215332032, 0.059997558593750014, 7.949996948242159, 0.5000000000000001, 1.0200004577636717, -8.8099365234375, -2.3200073242187496, 0.8799972534179619, 0.5800018310546874, -0.3699989318847656, 0.7400016784668039, 20.39990234375, 5.650009155273409, 0.3699989318847656, -1.4000015258788998, -0.5099983215332029, -0.4099121093750002, 0.6800003051757812, 1.4899902343750568, 13.08984375, 2.710006713867159, -0.2499999999999998, 0.11999893188476583, -0.30000305175781955, -0.09000015258790506, 0.06999969482421865, 0.8000030517578197, 69.1201171875, -1.7599945068359373, -0.020000457763664707, 0.30999755859374983, 87.800048828125, 6.3999786376953125, 0.38000106811524154, -0.22999954223633512, -4.1899871826171875, -0.8000488281250002, 0.27000045776367176, -0.11000061035156976, -0.1399993896484373, 0.3600006103515696, 0.09999847412108666, 24.929931640625, -2.589996337890625, 15.760009765625, 0.04999923706054671, -0.2099990844726492, -0.3499984741210937, 2.3699951171875, -2.589996337890596, 20.43994140625, -0.1300010681152417, 0.6399993896484302, 0.2900009155273437, -31.08984375, -2.8399963378906823, -0.23999786376952395, 0.06999969482421865, 0.3700027465820382, -0.7400016784667967, 3.75, 0.07999801635741471, 12.47998046875, 0.18999862670898449, -0.8400115966796591, 0.5600013732910155, -12.429931640625, -0.3699989318847584, 0.009998321533203305, -1.1399993896484375, 0.43000030517577426, -1.319992065429659, 0.3899993896484376, 41.81982421875, 0.06000137329101582, -2.93000793457034, 0.9700012207031322, 0.40999984741210954, 1.10009765625, -0.08000183105469451, 4.639892578125, -4.0299987792968475, 0.36000061035156233, 0.01999664306640613, 0.09999847412110065, -8.77001953125, -1.089996337890625, 0.5200004577636788, -10.089996337890682, 0.36000061035156233, 1.860000610351591, -0.3398437499999999, 0.5000000000000001, 0.6399993896484374, -0.36000061035156233, -1.5899963378906246, -0.02000045776367194, -0.8899993896484449, -25.3701171875, 0.02000045776367194, -0.04000091552734388, 47.380126953125, 4.0500030517578125, 0.8199996948242186, 11.43994140625, -0.7399978637695312, 3.0599975585937496, 0.22999954223632835, 0.02000045776367194, -0.22999954223632835, 0.4700012207031249, 1.029998779296875, -19.619873046875, -0.04999923706054671, 2.1599998474121094, 0.36000061035156233, 72.789794921875, -7.009994506835937, 0.14999771118164784, -0.21000289916992898, 1.0800018310546804, 0.029998779296874764, 49.97998046875001, 0.4799957275390624, -19.769775390625, -0.09999847412109389, 0.05000305175781975, -0.5800018310546806, -1.6300048828125282, 0.599998474121094, -14.9501953125, 1.1800003051757815, 0.030002593994133343, 0.8800048828125282, 0.11999893188476583, -1.5599975585937504, -0.6699981689453126, -40.919921875, 0.4399986267089843, 0.3899993896484376, 0.02000045776367194, -5.45001220703125, 0.3999977111816404, 2.489990234375, 1.6300048828124716, 0.6199989318847655, 24.610107421875, 0.5800018310546874, -0.7800025939941482, 0.17000198364257835, 17.33984375, 0.3900032043457102, 0.12999725341796142, 5.660003662109403, -57.030029296875, 0.27999877929687506, -2.5400085449218754, -0.13000106811523446, 0.2200012207031323, -4.04998779296875, -0.11999893188476583, -0.510002136230476, -32.89990234375, -0.4799995422363282, 0.3400001525878904, -69.679931640625, -8.100006103515625, -0.3899993896484376, -0.3899993896484376, 0.6599998474121094, 0.40999984741210954, 0.8299980163574219, 22.889892578125, 1.8600006103515625, -0.02000045776367194, -0.07999801635741471, 0.5200004577636721, 54.18994140625, 5.8300018310546875, -0.4900054931640911, 5.25, 0.09000015258789058, 0.10000228881835922, 0.38000106811523426, -0.4299926757812214, -0.5800018310546874, -17.97998046875, -0.06000137329101582, -0.2900009155273437, -0.21999740600585924, 0.15999984741210924, -3.1300048828125, -0.18999862670898449, 5.280029296875, -0.10000228881835922, 47.380126953125, 0.2899971008300779, 3.229995727539091, 0.7700004577636719, 0.2499999999999998, 0.5300025939941407, -10.989990234375, 7.170013427734347], \"yaxis\": \"y\"}, {\"hovertemplate\": \"type=predict<br>x=%{x}<br>price=%{y}<extra></extra>\", \"legendgroup\": \"predict\", \"line\": {\"color\": \"#EF553B\", \"dash\": \"solid\"}, \"mode\": \"lines\", \"name\": \"predict\", \"showlegend\": true, \"type\": \"scattergl\", \"x\": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520], \"xaxis\": \"x\", \"y\": [-125.57007598876953, -134.04888916015625, -156.66110229492188, -163.86326599121094, -133.73948669433594, -127.78841400146484, -137.35247802734375, -156.4730224609375, -161.6017303466797, -144.5320281982422, -137.01002502441406, -142.88113403320312, -157.02859497070312, -156.4590301513672, -149.59393310546875, -143.43984985351562, -149.41197204589844, -152.4024658203125, -151.75613403320312, -139.1173095703125, -147.57171630859375, -168.19613647460938, -174.83836364746094, -166.3579864501953, -150.70437622070312, -155.13690185546875, -177.71385192871094, -187.08872985839844, -183.87413024902344, -169.23287963867188, -172.1956024169922, -188.03387451171875, -196.6939697265625, -217.04025268554688, -202.04872131347656, -199.2602081298828, -205.26426696777344, -201.0552520751953, -216.55787658691406, -195.75216674804688, -190.4049072265625, -198.07327270507812, -195.610107421875, -223.50563049316406, -198.71234130859375, -187.9473114013672, -188.55821228027344, -218.0771026611328, -203.61888122558594, -196.11790466308594, -191.2079620361328, -176.7030029296875, -222.467041015625, -198.08053588867188, -185.92501831054688, -178.1222686767578, -162.86521911621094, -226.12936401367188, -202.87997436523438, -185.35775756835938, -176.66415405273438, -156.13546752929688, -227.98329162597656, -194.48745727539062, -181.8030548095703, -173.06809997558594, -155.35940551757812, -231.4456024169922, -204.72068786621094, -183.57949829101562, -172.7574462890625, -148.5305938720703, -251.0523681640625, -213.72616577148438, -191.4058380126953, -183.09127807617188, -158.17494201660156, -243.72613525390625, -204.08351135253906, -186.33656311035156, -172.46559143066406, -158.95486450195312, -225.20396423339844, -174.65989685058594, -170.05458068847656, -189.693115234375, -203.57168579101562, -226.95675659179688, -198.30706787109375, -196.80076599121094, -217.94529724121094, -247.09207153320312, -233.12181091308594, -229.4247283935547, -232.63595581054688, -272.0268859863281, -253.62295532226562, -245.93032836914062, -253.83702087402344, -256.6872253417969, -285.1306457519531, -266.0788879394531, -260.7469177246094, -263.8565368652344, -265.2803039550781, -262.1580505371094, -256.7864990234375, -265.47198486328125, -273.7989807128906, -303.0878601074219, -307.7996826171875, -303.1484375, -309.77740478515625, -313.342041015625, -325.319091796875, -320.9349670410156, -309.76373291015625, -306.9788513183594, -308.604248046875, -340.7310485839844, -341.21624755859375, -328.1343078613281, -332.4253845214844, -335.789794921875, -351.4395446777344, -325.2074890136719, -309.7904357910156, -275.0242919921875, -313.89630126953125, -309.14404296875, -294.0768737792969, -281.0327453613281, -275.92779541015625, -322.333740234375, -314.11651611328125, -287.9315185546875, -276.1590270996094, -279.7917785644531, -328.60662841796875, -299.5146484375, -281.1956481933594, -279.07513427734375, -286.042236328125, -358.60528564453125, -327.00653076171875, -292.94403076171875, -270.7709655761719, -270.5874328613281, -338.907470703125, -307.7197265625, -284.69970703125, -287.4314880371094, -327.98577880859375, -393.392822265625, -336.9217834472656, -295.4097900390625, -300.1120300292969, -397.3630065917969, -329.448974609375, -285.8331604003906, -281.3865661621094, -309.3614501953125, -391.04400634765625, -316.435546875, -264.0970764160156, -259.9851379394531, -234.2036590576172, -356.3596496582031, -279.9674987792969, -226.53932189941406, -214.9623260498047, -229.55535888671875, -366.4399719238281, -281.838134765625, -230.74366760253906, -217.36788940429688, -217.20362854003906, -362.1200256347656, -279.8993225097656, -225.12925720214844, -202.27590942382812, -183.48329162597656, -360.3325500488281, -267.8282165527344, -210.2016143798828, -188.25743103027344, -179.716552734375, -347.3633117675781, -269.8612976074219, -222.6207733154297, -197.4698028564453, -187.5504913330078, -322.5240783691406, -329.1976013183594, -333.39703369140625, -326.48028564453125, -327.9949951171875, -296.2842102050781, -130.4391632080078, 19.490846633911133, 100.43269348144531, -19.080312728881836, -63.879024505615234, -142.53759765625, -157.78973388671875, -193.9018096923828, -67.84796905517578, 1.7996165752410889, 2.866732358932495, -2.5050458908081055, 30.604259490966797, -5.641641139984131, -50.25932312011719, -81.44623565673828, -93.60969543457031, -48.00062561035156, -63.244049072265625, -77.9305648803711, -77.47148895263672, -28.640321731567383, -28.333574295043945, -40.09025573730469, -53.698036193847656, -56.31412887573242, -27.617816925048828, -32.80356216430664, -58.98517608642578, -81.48191833496094, -95.47406768798828, -65.02783966064453, -68.5584945678711, -94.0038833618164, -115.15499877929688, -123.52267456054688, -87.19248962402344, -102.12598419189453, -121.47352600097656, -128.33474731445312, -92.88448333740234, -80.56565856933594, -93.40613555908203, -102.31922149658203, -98.08847045898438, -68.63993835449219, -61.620914459228516, -77.68165588378906, -88.12120056152344, -93.06175994873047, -72.15889739990234, -57.869590759277344, -73.67230224609375, -85.16967010498047, -97.9034194946289, -76.48265075683594, -63.981021881103516, -80.09860229492188, -96.6296615600586, -102.34771728515625, -89.17271423339844, -68.29949188232422, -80.60990142822266, -91.06403350830078, -97.4096450805664, -81.47172546386719, -65.975830078125, -78.07124328613281, -93.55776977539062, -106.98759460449219, -100.45557403564453, -124.09053802490234, -153.84320068359375, -156.439697265625, -163.67672729492188, -159.99539184570312, -169.9212188720703, -157.80055236816406, -133.2342529296875, -116.12036895751953, -112.67195129394531, -119.87171936035156, -134.8033447265625, -142.2982635498047, -86.19336700439453, -104.37222290039062, -114.44540405273438, -110.70951080322266, -131.9657440185547, -72.02165222167969, -114.4462661743164, -122.38111877441406, -133.40692138671875, -173.9191131591797, -97.54755401611328, -147.3423614501953, -174.42727661132812, -207.25057983398438, -242.08450317382812, -208.139404296875, -252.29150390625, -256.20880126953125, -265.6611328125, -271.850341796875, -86.8003921508789, -118.03289794921875, -68.64210510253906, 21.304460525512695, 103.66027069091797, 140.0351104736328, 199.46861267089844, 215.9305877685547, 215.48178100585938, 154.550048828125, 109.04357147216797, 61.79238510131836, -17.34072494506836, -120.98184967041016, -184.6249542236328, -223.76962280273438, -251.52452087402344, -273.93902587890625, -271.58721923828125, -257.91058349609375, -241.1190948486328, -220.3036651611328, -192.9159393310547, -148.5535430908203, -158.12637329101562, -141.23257446289062, -131.95150756835938, -118.27386474609375, -128.3211669921875, -129.00511169433594, -132.28721618652344, -138.3107452392578, -131.78102111816406, -134.25381469726562, -138.74549865722656, -141.81582641601562, -144.40188598632812, -129.71151733398438, -148.14093017578125, -149.96092224121094, -149.6154327392578, -148.7412872314453, -131.9548797607422, -149.37158203125, -139.82626342773438, -135.7710418701172, -123.26246643066406, -149.2090606689453, -146.5348358154297, -147.8084716796875, -146.31439208984375, -136.97824096679688, -160.29766845703125, -156.16348266601562, -154.99148559570312, -157.3167266845703, -149.41224670410156, -182.02699279785156, -174.3419952392578, -169.2771453857422, -160.24534606933594, -144.76165771484375, -192.18914794921875, -181.934326171875, -173.16314697265625, -162.87950134277344, -151.92958068847656, -204.4271240234375, -186.9206085205078, -177.45143127441406, -168.46546936035156, -150.9451141357422, -209.47410583496094, -190.7371063232422, -177.7244415283203, -164.0049285888672, -236.2069854736328, -227.64059448242188, -212.60211181640625, -184.82199096679688, -146.93313598632812, -238.50157165527344, -212.91632080078125, -194.26986694335938, -163.38308715820312, -126.492431640625, -239.00567626953125, -206.44329833984375, -185.32131958007812, -157.31578063964844, -121.3664779663086, -240.92465209960938, -203.96583557128906, -185.4239959716797, -155.35560607910156, -124.78948974609375, -246.05474853515625, -209.86361694335938, -185.9998779296875, -152.26451110839844, -110.21131896972656, -255.54652404785156, -207.3677978515625, -179.23573303222656, -152.1801300048828, -118.7919692993164, -248.60032653808594, -201.03701782226562, -178.02243041992188, -148.9847869873047, -120.87632751464844, -242.85336303710938, -182.5381317138672, -180.36305236816406, -201.55763244628906, -215.3594207763672, -237.43556213378906, -210.18296813964844, -206.8734130859375, -217.00074768066406, -245.9329071044922, -234.054443359375, -226.14242553710938, -226.6751251220703, -262.5574035644531, -248.84046936035156, -243.87664794921875, -241.9700164794922, -226.994384765625, -250.1946258544922, -238.88653564453125, -233.78131103515625, -231.56539916992188, -221.2486114501953, -223.28189086914062, -214.01663208007812, -214.46429443359375, -208.35430908203125, -222.96327209472656, -223.33753967285156, -223.21156311035156, -224.04563903808594, -220.80540466308594, -232.44744873046875, -231.7596435546875, -234.01206970214844, -240.9301300048828, -235.30746459960938, -264.0960693359375, -255.3455047607422, -245.46278381347656, -240.2888946533203, -227.52342224121094, -239.04457092285156, -223.3856658935547, -214.92315673828125, -204.9677276611328, -240.34239196777344, -231.9199981689453, -227.54710388183594, -223.95884704589844, -217.5279998779297, -254.38491821289062, -243.66104125976562, -232.49049377441406, -233.70863342285156, -228.2608642578125, -273.2851257324219, -260.83935546875, -248.97987365722656, -236.56591796875, -214.5581512451172, -274.8467712402344, -257.1502380371094, -240.21485900878906, -225.7340545654297, -214.54051208496094, -278.4859619140625, -257.2548522949219, -241.69813537597656, -226.58438110351562, -209.54058837890625, -284.9527893066406, -259.7509765625, -241.3006134033203, -222.17935180664062, -319.7381896972656, -296.1020202636719, -270.839111328125, -236.76861572265625, -201.9798126220703, -308.5430603027344, -275.1200256347656, -247.2109832763672, -212.016357421875, -185.55709838867188, -306.67169189453125, -263.60791015625, -234.6089630126953, -203.24488830566406, -165.14834594726562, -302.1561279296875, -257.1549987792969, -227.22203063964844, -192.67225646972656, -162.43087768554688, -320.74285888671875, -268.5784606933594, -227.90748596191406, -192.10047912597656, -148.28628540039062, -327.95556640625, -264.32623291015625, -220.78956604003906, -190.00955200195312, -158.0869903564453, -315.4330139160156, -257.8241271972656, -223.8615264892578], \"yaxis\": \"y\"}],                        {\"legend\": {\"title\": {\"text\": \"type\"}, \"tracegroupgap\": 0}, \"template\": {\"data\": {\"bar\": [{\"error_x\": {\"color\": \"#2a3f5f\"}, \"error_y\": {\"color\": \"#2a3f5f\"}, \"marker\": {\"line\": {\"color\": \"#E5ECF6\", \"width\": 0.5}}, \"type\": \"bar\"}], \"barpolar\": [{\"marker\": {\"line\": {\"color\": \"#E5ECF6\", \"width\": 0.5}}, \"type\": \"barpolar\"}], \"carpet\": [{\"aaxis\": {\"endlinecolor\": \"#2a3f5f\", \"gridcolor\": \"white\", \"linecolor\": \"white\", \"minorgridcolor\": \"white\", \"startlinecolor\": \"#2a3f5f\"}, \"baxis\": {\"endlinecolor\": \"#2a3f5f\", \"gridcolor\": \"white\", \"linecolor\": \"white\", \"minorgridcolor\": \"white\", \"startlinecolor\": \"#2a3f5f\"}, \"type\": \"carpet\"}], \"choropleth\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"choropleth\"}], \"contour\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"contour\"}], \"contourcarpet\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"contourcarpet\"}], \"heatmap\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"heatmap\"}], \"heatmapgl\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"heatmapgl\"}], \"histogram\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"histogram\"}], \"histogram2d\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"histogram2d\"}], \"histogram2dcontour\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"histogram2dcontour\"}], \"mesh3d\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"mesh3d\"}], \"parcoords\": [{\"line\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"parcoords\"}], \"pie\": [{\"automargin\": true, \"type\": \"pie\"}], \"scatter\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatter\"}], \"scatter3d\": [{\"line\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatter3d\"}], \"scattercarpet\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattercarpet\"}], \"scattergeo\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattergeo\"}], \"scattergl\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattergl\"}], \"scattermapbox\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattermapbox\"}], \"scatterpolar\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterpolar\"}], \"scatterpolargl\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterpolargl\"}], \"scatterternary\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterternary\"}], \"surface\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"surface\"}], \"table\": [{\"cells\": {\"fill\": {\"color\": \"#EBF0F8\"}, \"line\": {\"color\": \"white\"}}, \"header\": {\"fill\": {\"color\": \"#C8D4E3\"}, \"line\": {\"color\": \"white\"}}, \"type\": \"table\"}]}, \"layout\": {\"annotationdefaults\": {\"arrowcolor\": \"#2a3f5f\", \"arrowhead\": 0, \"arrowwidth\": 1}, \"autotypenumbers\": \"strict\", \"coloraxis\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"colorscale\": {\"diverging\": [[0, \"#8e0152\"], [0.1, \"#c51b7d\"], [0.2, \"#de77ae\"], [0.3, \"#f1b6da\"], [0.4, \"#fde0ef\"], [0.5, \"#f7f7f7\"], [0.6, \"#e6f5d0\"], [0.7, \"#b8e186\"], [0.8, \"#7fbc41\"], [0.9, \"#4d9221\"], [1, \"#276419\"]], \"sequential\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"sequentialminus\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]]}, \"colorway\": [\"#636efa\", \"#EF553B\", \"#00cc96\", \"#ab63fa\", \"#FFA15A\", \"#19d3f3\", \"#FF6692\", \"#B6E880\", \"#FF97FF\", \"#FECB52\"], \"font\": {\"color\": \"#2a3f5f\"}, \"geo\": {\"bgcolor\": \"white\", \"lakecolor\": \"white\", \"landcolor\": \"#E5ECF6\", \"showlakes\": true, \"showland\": true, \"subunitcolor\": \"white\"}, \"hoverlabel\": {\"align\": \"left\"}, \"hovermode\": \"closest\", \"mapbox\": {\"style\": \"light\"}, \"paper_bgcolor\": \"white\", \"plot_bgcolor\": \"#E5ECF6\", \"polar\": {\"angularaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"bgcolor\": \"#E5ECF6\", \"radialaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}}, \"scene\": {\"xaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}, \"yaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}, \"zaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}}, \"shapedefaults\": {\"line\": {\"color\": \"#2a3f5f\"}}, \"ternary\": {\"aaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"baxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"bgcolor\": \"#E5ECF6\", \"caxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}}, \"title\": {\"x\": 0.05}, \"xaxis\": {\"automargin\": true, \"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\", \"title\": {\"standoff\": 15}, \"zerolinecolor\": \"white\", \"zerolinewidth\": 2}, \"yaxis\": {\"automargin\": true, \"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\", \"title\": {\"standoff\": 15}, \"zerolinecolor\": \"white\", \"zerolinewidth\": 2}}}, \"title\": {\"text\": \"Stock Price\"}, \"xaxis\": {\"anchor\": \"y\", \"domain\": [0.0, 1.0], \"title\": {\"text\": \"x\"}}, \"yaxis\": {\"anchor\": \"x\", \"domain\": [0.0, 1.0], \"title\": {\"text\": \"price\"}}},                        {\"responsive\": true}                    ).then(function(){\n                            \nvar gd = document.getElementById('f114c863-2eb4-4679-9591-5b462552c46e');\nvar x = new MutationObserver(function (mutations, observer) {{\n        var display = window.getComputedStyle(gd).display;\n        if (!display || display === 'none') {{\n            console.log([gd, 'removed!']);\n            Plotly.purge(gd);\n            observer.disconnect();\n        }}\n}});\n\n// Listen for the removal of the full notebook cells\nvar notebookContainer = gd.closest('#notebook-container');\nif (notebookContainer) {{\n    x.observe(notebookContainer, {childList: true});\n}}\n\n// Listen for the clearing of the current output cell\nvar outputEl = gd.closest('.output');\nif (outputEl) {{\n    x.observe(outputEl, {childList: true});\n}}\n\n                        })                };                            </script>        </div>\n</body>\n</html>"
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "<a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=0c40d680-c720-488b-84aa-395d60b39534' target=\"_blank\">\n",
    "<img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>\n",
    "Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>"
   ],
   "metadata": {
    "tags": [],
    "created_in_deepnote_cell": true,
    "deepnote_cell_type": "markdown"
   }
  }
 ],
 "nbformat": 4,
 "nbformat_minor": 2,
 "metadata": {
  "orig_nbformat": 2,
  "deepnote": {
   "is_reactive": false
  },
  "deepnote_notebook_id": "28fb5011-b124-4569-a6a4-9a49ba7cade2",
  "deepnote_execution_queue": []
 }
}