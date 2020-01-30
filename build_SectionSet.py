import math
import time

# Input a matrix of interested stock, with the size of search window and the precent of designed step.
#   and the desired profit per cycle(20 trade days), defaultly this value is set to 0.025( 2.5%)
# Output a double dimension list which contained all high profit section of this stock.
#   The shape of this list will like to: (n, 3) each name of col: rate_of_profit, start_date, end_date
#   BTW: the output list HighProfit_Sections actually is some kind of mark point but not the 'section' it is.
def find_HighProfitSection(Matrix, windows_size, step_precent, profitrate_pre20):
    step_size = math.ceil(windows_size * step_precent)
    m = len(Matrix)
    CheckPoints = range(0, m-windows_size, step_size)
    ChangeRate_list = []
    HighProfit_Sections = []
    DesireProfit = (1 + profitrate_pre20)**math.floor(windows_size/20)
    for CheckPoint in CheckPoints:
        ChangeRate_list.append([((Matrix.at[CheckPoint+windows_size-1,'close'])/(Matrix.at[CheckPoint,'close'])),
                               CheckPoint, CheckPoint+windows_size-1])
    for i in range(1, (len(ChangeRate_list)-1)):
        if((ChangeRate_list[i][0] >= ChangeRate_list[i-1][0]) and (ChangeRate_list[i][0] >= ChangeRate_list[i+1][0])):
            if(ChangeRate_list[i][0] >= DesireProfit):
                HighProfit_Sections.append(ChangeRate_list[i])
    return HighProfit_Sections

# Input the original matrix of stock we interestd, and the high profit sections set from function find_HighProfitSection.
# Output a dict named SectionSet that contained
#   The shape of SectionSet will likt to:
#       {code1_startdate1_enddate1: data of all features from orignal matrix, 2_2:data2, ...:... }
def cutout_Section(Matrix, HighProfit_Sections):
    SectionSet = {}
    for section in HighProfit_Sections:
        code = Matrix.at[section[1], 'ts_code']
        start_date = Matrix.at[section[1], 'trade_date']
        end_date = Matrix.at[section[2], 'trade_date']
        SectionSet[code+'_'+start_date+'_'+end_date] = Matrix.iloc[section[1]:section[2]+1]
    return SectionSet

# Input a matrixset that contained all data of all interested stock. And size of window and precent of step
#   for the function find_HighProfitSections.
# Output a dict SectionBundle which has only one dimension. It contains all of high profit section of all stock.
def build_SectionBundle(MatrixSet, windows_size, step_precent, profit_rate=0.25):
    SectionBundle = {}
    m = len(MatrixSet)
    n = 0
    tik = time.time()
    print('Slicing process starting...')
    tik = time.time()
    print(str(m)+' of matrix will be slice...')
    for key in MatrixSet.keys():
        n += 1
        HighProfit_Sections = find_HighProfitSection(MatrixSet[key], windows_size, step_precent,
                                                     profitrate_pre20=profit_rate)
        single_SectionSet = cutout_Section(MatrixSet[key], HighProfit_Sections)
        if(single_SectionSet):
            SectionBundle.update(single_SectionSet)
            print(str(n)+'/'+str(m)+' has done! '+key+' is successfully sliced.')
        else:
            print(str(n)+'/'+str(m)+' Find no section! '+key+' is failed slicing.')
    tok = time.time()
    print('Slicing process is done!')
    bundle_size = len(SectionBundle)
    print('The size of the section bundle is like to be:'+str(bundle_size))
    toc = time.time()
    print('Time consume:' + str(round(toc - tik, 4)) + ' s.\n')
    return SectionBundle