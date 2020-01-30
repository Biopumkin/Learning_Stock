import tushare as ts
import pandas as pd
import time
ts.set_token('34b4122f3743264c5b079149f56c2f95b588346b5056241774c3814a')
pro = ts.pro_api('34b4122f3743264c5b079149f56c2f95b588346b5056241774c3814a')

# Input two different dataframes
# Output one merged dataframe which axis is horizon
def merged_DifferentCol(df1, df2):
    cols_to_use = df2.columns.difference(df1.columns)
    dfNew = pd.merge(df1, df2[cols_to_use], left_index=True, right_index=True, how='outer')
    return dfNew

# Input a code with start date and end date which indicate the interested data we want.
# Output a matrix that merged all of data from different API of tushare.
# The shape of matrix will like to: (row=days, col=features)
def download_RawData(code, start, end):
    Matrix_probar = ts.pro_bar(ts_code=code, start_date=start, end_date=end)
    Matrix_dailybasic = pro.daily_basic(ts_code=code, start_date=start, end_date=end)
    Matrix_moneyflow = pro.moneyflow(ts_code=code, start_date=start, end_date=end)
    Matrix = merged_DifferentCol(Matrix_moneyflow, merged_DifferentCol(Matrix_dailybasic,Matrix_probar))
    return Matrix

# Input a matrix
# Output a matrix which has been trimed.
def clean_RawData(Matrix):
    # Matrix = Matrix.drop(labels=['open','close','high','low','pre_close','change','amount'],
    #                      axis=1) #Delete the useless col from pro_bar
    Matrix = Matrix.drop(labels=['total_share','float_share','free_share','total_mv','circ_mv',
                                 'pe_ttm', 'ps_ttm', 'dv_ratio', 'dv_ttm'],
                         axis=1) #Delete col from daily_basic
    Matrix = Matrix.drop(labels=['buy_sm_amount','sell_sm_amount',
                                 'buy_md_amount','sell_md_amount',
                                 'buy_lg_amount','sell_lg_amount',
                                 'buy_elg_amount','sell_elg_amount','net_mf_amount'],
                         axis=1) #Delete col from moneyflow
    return Matrix

def check_alignment(MatrixSet):
    col_names = []
    for key in MatrixSet.keys():
        col_names.append(MatrixSet[key].columns.values)
    output_colnames = col_names[0]
    col_names = pd.DataFrame(col_names)
    col_names = col_names.drop_duplicates(keep=False)
    if(col_names.empty == True):
        print('Alignment check!')
        print('The features set contains:')
        print(str(output_colnames))
        print(str(len(output_colnames)-2)+' features totaly.\n***: the ts_code and trade_date will be delete later.')
    else:
        print('The features is not aligned! ')

# Input a list contained all of code of interested stock, with the start date and end date of course.
# Output a dict contained all of matrix of interested stock.
# The shape of output dict will like to: {{code1: matrix1},{code2: matrix2},{code_n: matrix_n}}
def downloading_RawData(codeslist, start, end):
    MatrixSet = {}
    failedDownload = []
    m = len(codeslist)
    n = 0
    print('Download process starting...')
    tik = time.time()
    print(str(m)+' of stock will be download...')
    for code in codeslist:
        n += 1
        M = download_RawData(code, start, end) #download data and merged them
        M = clean_RawData(M) #delete some col that we need not
        M = M.iloc[::-1] #reversed the matrix
        M = M.reset_index(drop=True)
        if(M.empty == False):
            MatrixSet[code] = M
            print(str(n)+'/'+str(m)+' has done! '+code+' was successfully downloaded.')
        else:
            failedDownload.append(code)
            print(str(n)+'/'+str(m)+' error! '+code+' failed download.')
        time.sleep(0.5)
    print('Download process is done!')
    if(failedDownload):
        print(str(len(failedDownload))+' stock '+str(failedDownload)+' cannot be downloaded!\n')
    check_alignment(MatrixSet)
    toc = time.time()
    print('Time consume:'+str(round(toc-tik,4))+' s.')
    return MatrixSet