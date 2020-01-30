import pandas as pd
from math import floor
import time

# Input a sectino set that contains all section of only one stock.
#   Then, delete some of redundancy columns and vectoring all section. In succession, aligning those vectors as an Matrix
# Output a matrix contains all vectored section.
#   This matrix will like to be: ( n_features, m_section), n_features = trade_date * features
def collect_VectorToMatrix(SectionSet):
    frames = {}
    for key in SectionSet.keys():
        Section_Matrix = SectionSet[key].drop(labels=['ts_code', 'trade_date'], axis=1)
        Section_vector = pd.Series(Section_Matrix.values.reshape(-1))
        frames.update({key:Section_vector})
    SectionSet_Matrix = pd.concat(frames, axis=1)
    return SectionSet_Matrix

# Input a section set matrix then shuffle all columns and output it.
def shuffle_SectionSetMatrix(SectionSet_Matrix):
    SectionSet_Matrix = SectionSet_Matrix.T
    new_SectionSetMatrix = SectionSet_Matrix.sample(frac=1)
    new_SectionSetMatrix = new_SectionSetMatrix.T
    return new_SectionSetMatrix

# Input a section set matrix with set up the desired size(precentage) of training set and the needing of cross validation set
# Output train set, cross validation set and test set.
def distribute_Data(SectionSetMatrix, trainset_size=0.6, cvset=False):
    m = SectionSetMatrix.shape[1]
    Train_Set = SectionSetMatrix.iloc[:, 0:(floor(m*trainset_size))]
    if(not cvset):
        CV_Set = pd.DataFrame()
        Test_Set = SectionSetMatrix.iloc[:, (floor(m*trainset_size)):m]
    else:
        cvset_size = (1 - trainset_size) / 2
        CV_Set = SectionSetMatrix.iloc[:, (floor(m*trainset_size)):(floor(m*(trainset_size+cvset_size)))]
        Test_Set = SectionSetMatrix.iloc[:, (floor(m*(trainset_size+cvset_size))):m]
    return Train_Set, CV_Set, Test_Set

def normalizing_Matrix(Matrix):
    new_Matrix = (Matrix-Matrix.min())/(Matrix.max()-Matrix.min())
    return new_Matrix