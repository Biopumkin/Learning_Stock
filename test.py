import download_DataSet
import build_SectionSet
import build_DataSet
import pandas as pd

list = ['600028.SH', '600111.SH', '600160.SH', '600176.SH', '600188.SH', '600206.SH', '600219.SH', '600226.SH']
        # '600256.SH', '600259.SH', '600273.SH', '600277.SH', '600309.SH', '600346.SH', '600352.SH', '600362.SH',
        # '600366.SH', '600392.SH', '600426.SH', '600486.SH', '600489.SH', '600490.SH', '600497.SH', '600516.SH',
        # '600547.SH', '600549.SH', '600596.SH', '600598.SH', '600673.SH', '600740.SH', '600803.SH', '600988.SH',
        # '600989.SH', '601069.SH', '601088.SH', '601118.SH', '601212.SH', '601216.SH', '601225.SH', '601233.SH',
        # '601600.SH', '601699.SH', '601857.SH', '601898.SH', '601899.SH', '601958.SH', '603260.SH', '603379.SH',
        # '603799.SH', '603993.SH']
MatrixSet = download_DataSet.downloading_RawData(list, start='20160101', end='20200101')
SectionSet = build_SectionSet.build_SectionBundle(MatrixSet, 60, 0.05, 0.03)
SectionSet_Matrix = build_DataSet.collect_VectorToMatrix(SectionSet)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
SectionSet_Matrix = build_DataSet.shuffle_SectionSetMatrix(SectionSet_Matrix)
SectionSet_Matrix = build_DataSet.normalizing_Matrix(SectionSet_Matrix)
train_set, cv_set, test_set = build_DataSet.distribute_Data(SectionSet_Matrix, 0.8, cvset=True)
print(train_set.shape, cv_set.shape, test_set.shape)
print(test_set)
# print(test_set[test_set.isnull().values==True])