import sys
sys.path.insert(1, 'Path of multiSyncPy folder')

import pandas as pd
import scipy as sp
from scipy import signal
import numpy as np
import synchrony_metrics as sm
import math
import pingouin as pg
import sklearn as sl
from sklearn.feature_selection import mutual_info_regression

trialNum = pd.read_csv("Path of the trial numbe file (comp_trials.csv or coop_trials.csv)")
path ="Path of the data folder"

def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation. 
    Shifted data filled with NaNs 
    
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    if wrap:
        shiftedy = datay.shift(lag)
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy)
    else: 
        test = datax.corr(datay.shift(lag))
        return datax.corr(datay.shift(lag))

for dyad in range(1,11):
    T1 = trialNum[str(dyad)]

    CCReusltLis = []
    CCr = []
    CClag = []
    CCr_pos = []
    CClag_pos = []
    Coh10 = []
    coh20 = []
    plv = []
    pcc = []
    MI = []

    for block in range(1,4):
        Ts = trialNum.at[block-1, str(dyad)]
        T1 = trialNum[str(dyad)]

        for trial in range(1, Ts+1):
            dat = pd.read_csv(path + "D" + str(dyad) + "/" + str(block) + "_" + str(trial) + ".csv", header=None)

            d1 = dat[2]
            d2 = dat[6]
            df = pd.concat([d1, d2], axis=1, keys=['a', 'b'])

            # Pearson's correlation
            dat_corr = df.corr()
            print(dat_corr.iloc[0,1])
            CCReusltLis.append(dat_corr.iloc[0,1])

            # cross-correlation
            seconds = 0.5
            fps = 20
            rs = [crosscorr(d1,d2, lag) for lag in range(-int(seconds*fps-1),int(seconds*fps))]
            # offset = np.floor(len(rs)/2)-np.argmax(rs)
            if np.all(np.isnan(rs)):
                CCr.append("NaN")
                CClag.append("NaN")

            else:
                rs = [x for x in rs if not math.isnan(x)]
                max_r = np.max(rs)
                min_r = np.min(rs)
                max_indices = np.where(np.round(rs,decimals=5) == np.round(max_r,decimals=5))[0]
                min_indices = np.where(np.round(rs,decimals=5) == np.round(min_r,decimals=5))[0]
                nearest_max_index = np.abs(max_indices - len(rs)/2).argmin()
                nearest_min_index = np.abs(min_indices - len(rs)/2).argmin()
                nearest_max_index_value = max_indices[nearest_max_index]
                nearest_min_index_value = min_indices[nearest_min_index]

                if abs(max_r) > abs(min_r):
                    nearest_index = nearest_max_index
                    indices = max_indices
                elif abs(max_r) < abs(min_r):
                    nearest_index = nearest_min_index
                    indices = min_indices
                else:
                    if np.abs(nearest_max_index_value - len(rs)/2) < np.abs(nearest_min_index_value - len(rs)/2):
                        nearest_index = nearest_max_index
                        indices = max_indices
                    else:
                        nearest_index = nearest_min_index
                        indices = min_indices

                CCr.append(rs[indices[nearest_index]])
                CClag.append((len(rs)/2-indices[nearest_index])/fps)
                CCr_pos.append(rs[max_indices[nearest_max_index]])
                CClag_pos.append((len(rs)/2-max_indices[nearest_max_index])/fps)

            # coherence
            nperseg = 10
            f, Cxy1 = signal.coherence(d1, d2, nperseg=nperseg)
            nperseg = 20
            f, Cxy2 = signal.coherence(d1, d2, nperseg=nperseg)
            Coh10.append(Cxy1.mean())
            coh20.append(Cxy2.mean())
            
            # # symbolic entropy
            # df = pd.concat([d1, d2], axis=1, keys=['a', 'b'])
            # plt.plot(df)
            # sv = sm.symbolic_entropy(df)

            # phase synchrony (phase locking)
            d1Phase = np.angle(sp.signal.hilbert(d1))
            d2Phase = np.angle(sp.signal.hilbert(d2))
            phaseDiff = d1Phase-d2Phase
            phi = np.exp(1j * phaseDiff).mean()
            rho1 = np.abs(phi)
            plv.append(rho1)

            # pahse synchrony (Circular Correlation) lag sensitive
            rho2, p_value = pg.circ_corrcl(d1, d2)
            pcc.append(rho2)

            # mutual information
            x = d1.values.reshape(-1,1)
            y = d2.values
            mi = mutual_info_regression(x,y)
            MI.append(mi[0])

        CCReusltLis.append("NaN")
        CCr.append("NaN")
        CClag.append("NaN")
        CCr_pos.append("NaN")
        CClag_pos.append("NaN")
        Coh10.append("NaN")
        coh20.append("NaN")
        plv.append("NaN")
        pcc.append("NaN")
        MI.append("NaN")
    
    all_data = [CCReusltLis, CCr, CClag, CCr_pos, CClag_pos, Coh10, coh20, plv, pcc, MI]
    all_data_df = pd.DataFrame(all_data)
    all_data_df_T = all_data_df.T

    all_data_df_T.to_csv(path + "D" + str(dyad)  + ".csv", index=False, header=False)

