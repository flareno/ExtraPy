# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:36:18 2019
@author: F.LARENO-FACCINI
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import os



def load_lickfile(file_path, sep="\t", header=None):
    A = np.array(pd.read_csv(file_path, sep=sep, header=header))
    return np.array([[A[i][0], float(A[i][1].replace(',','.'))] for i in range(len(A))])



def scatter_lick(licks, ax=None, x_label='Time (s)', y_label='Trial Number',**kwargs):
    if len(licks)>0:
        ax = ax or plt.gca()
        x_label = x_label
        y_label = y_label
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        return ax.scatter(licks[:,1], licks[:,0], marker = "|", **kwargs)
    else:
        pass


def psth_lick(licks, ax=None, lentrial=10, samp_period=0.01, density=False,**kwargs):
    ax = ax or plt.gca()
   
    if len(licks)>0:
        bins = np.arange(0,lentrial+samp_period,samp_period)
        return ax.hist(licks[:,1], bins, density=density, **kwargs)
    else:
        return ax.axis('off')
        


def extract_random_delay(param):
    random = []
    r_time = []
    param = param
    
    with open(param, 'r') as filehandle:
        for line in filehandle:
                if 'A2 to A3 transition duration:' in line:        
                    random.append(line)
                else:
                    continue
    del(random[0]) # delete first row of param files. This is to overcome a bug in the acquisition software that logs the parameters shifted of one trial. Hence, we loose last trial
    
    for i in random:
        temp__ = i.split(' ')[-1]
        temp__ = temp__.split('\n')[0]
        r_time.append(temp__)
      
    r_time = np.asarray([[r_time[i].replace(',','.')] for i in range(len(r_time))])
    # r_time = np.asarray(r_time)
    RandomT = [float(r_time[i]) for i in range(len(r_time))]
    return [[float(RandomT[i]), int(i+1)] for i in range (len(RandomT))]


def loop_dict_1d(title,d1,iterab1,iterab2):
    if '{:d}'.format(d1) not in title:
        title['{:d}'.format(d1)] = np.asarray([iterab1,iterab2])
    else:
        title['{:d}'.format(d1)] = np.vstack((title['{:d}'.format(d1)],np.asarray([iterab1,iterab2])))

def loop_dict_2d(title,d1,d2,iterab1,iterab2):
    if '{:d}_{:d}'.format(d1,d2) not in title:
        title['{:d}_{:d}'.format(d1,d2)] = np.asarray([iterab1,iterab2])
    else:
        title['{:d}_{:d}'.format(d1,d2)] = np.vstack((title['{:d}_{:d}'.format(d1,d2)],np.asarray([iterab1,iterab2])))

def loop_dict_3d(title,d1,d2,d3,iterab1,iterab2):
    if '{:d}_{:d}_{:d}'.format(d1,d2,d3) not in title:
        title['{:d}_{:d}_{:d}'.format(d1,d2,d3)] = np.asarray([iterab1,iterab2])
    else:
        title['{:d}_{:d}_{:d}'.format(d1,d2,d3)] = np.vstack((title['{:d}_{:d}_{:d}'.format(d1,d2,d3)],np.asarray([iterab1,iterab2])))


def separate_by_delay(random, licks, delay1=400, delay2=900):
    """
    
    This function separates the behavioural trials depending on the delay used for the delivery of the reward.
    
    
    Parameters
    ----------
    random : Python List
        List of lists containing, in each sublist, the number of trial and the delay for each trial of the behaviour session 
        
    licks : 2D numpy array
        The resulting array of the function Behaviour.load_lickfile
        
    delay1 : INT, optional
        The default is 400.
        
    delay2 : INT, optional
        The default is 900.
    Returns
    -------
    delays :  python dictionary
        Dictionary containing every trial and the corresponding delay. Classified based on the daly at t,t-1 and t-2
        
    licks_by_delay :  python dictionary
        Dictionary containing every lick event and the corresponding trial. Classified based on the daly at t,t-1 and t-2        
    """
    delays, licks_by_delay = {}, {}
    
    
    for idx,(d,t) in enumerate(random):
        if d == delay1:
            loop_dict_1d(delays,delay1,d,t) #create key in the dict of all the trials with delay==delay1
        
            if idx == 0:  # skip first trial since it has no trial-1
                pass
            elif random[idx-1][0] == delay1: # further divide by the delays of trial-1
                loop_dict_2d(delays, d1=delay1, d2=delay1, iterab1=d, iterab2=t)
                if random[idx-2][0] == delay1: # further divide by the delays of trial-2
                    loop_dict_3d(delays,delay1,delay1,delay1,d,t)
                elif random[idx-2][0] == delay2:
                    loop_dict_3d(delays,delay2,delay1,delay1,d,t)
            elif random[idx-1][0] == delay2:
                loop_dict_2d(delays,delay2,delay1,d,t)
                                
        elif d == delay2: # extract trials with a delay==delay2 (usually 900ms)
            loop_dict_1d(delays,delay2,d,t)
        
            if idx == 0: # skip first trial since it has no trial-1
                pass
            elif random[idx-1][0] == delay1:
                loop_dict_2d(delays,delay1,delay2,d,t)
            elif random[idx-1][0] == delay2:
                loop_dict_2d(delays,delay2,delay2,d,t)
                if random[idx-2][0] == delay2: # further divide by the delays of trial-2
                    loop_dict_3d(delays,delay2,delay2,delay2,d,t)
                elif random[idx-2][0] == delay1:
                    loop_dict_3d(delays,delay1,delay2,delay2,d,t)

    for t,l in licks: # licks has 2 columns: t(trial number) and l(lick time)
        for d,tr in delays['{:d}'.format(delay1)]: # series of loops to append in one array the licks for the proper delay. So to have an array similar to the original one but divided by the delays
            if t==tr:
                loop_dict_1d(licks_by_delay,delay1,t,l)
        for d,tr in delays['{:d}'.format(delay2)]:
            if t==tr:
                loop_dict_1d(licks_by_delay,delay2,t,l)
        for d,tr in delays['{:d}_{:d}'.format(delay1,delay1)]:
            if t==tr:
                loop_dict_2d(licks_by_delay,delay1,delay1,t,l)
        for d,tr in delays['{:d}_{:d}'.format(delay2,delay1)]:
            if t==tr:
                loop_dict_2d(licks_by_delay,delay2,delay1,t,l)
        for d,tr in delays['{:d}_{:d}'.format(delay1,delay2)]:
            if t==tr:
                loop_dict_2d(licks_by_delay,delay1,delay2,t,l)
        for d,tr in delays['{:d}_{:d}'.format(delay2,delay2)]:
            if t==tr:
                loop_dict_2d(licks_by_delay,delay2,delay2,t,l)
        for d,tr in delays['{:d}_{:d}_{:d}'.format(delay1,delay1,delay1)]:
            if t==tr:
                loop_dict_3d(licks_by_delay,delay1,delay1,delay1,t,l)
        for d,tr in delays['{:d}_{:d}_{:d}'.format(delay2,delay1,delay1)]:
            if t==tr:
                loop_dict_3d(licks_by_delay,delay2,delay1,delay1,t,l)
        for d,tr in delays['{:d}_{:d}_{:d}'.format(delay2,delay2,delay2)]:
            if t==tr:
                loop_dict_3d(licks_by_delay,delay2,delay2,delay2,t,l)
        for d,tr in delays['{:d}_{:d}_{:d}'.format(delay1,delay2,delay2)]:
            if t==tr:
                loop_dict_3d(licks_by_delay,delay1,delay2,delay2,t,l)

    return delays, licks_by_delay



def separate_by_condition(lick, nb_control_trials=30):
    nostim = []
    stim = []
    
    [nostim.append([t,l]) for t,l in lick if t <= nb_control_trials]
    nostim = np.asarray(nostim)
    [stim.append([t,l]) for t,l in lick if t > nb_control_trials]
    stim = np.asarray(stim)
    return nostim, stim
 
    
    
def envelope(n, bins, ax=None, len_trial=10, x_label='Time (s)', y_label='Number Count', sigma=2):
    # PLOTTING THE ENVELOPE (which is n, the y value of each point of the PSTH)
    binning = []
    for h in range(len(bins)):
        if h>0:
            binning.append(np.mean((bins[h],bins[h-1])))
    step = len_trial/len(binning)
    x = np.arange(0,len_trial,step)
    
    # smoothening the envelope
    nsmoothed = gaussian_filter1d(n, sigma)

    ax = ax or plt.gca()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return ax.plot(x, nsmoothed)


def concatenate_licks(path, skip_last=False):
    """
    Concatenates multiple .lick files present in the same folder.
    The resulting array has incremental trial numbers (as if they had all been recorded in one session). 
    It can remove the last trial (with corresponding lick times) in case there is the need to use this data
    with the info coming from .param file (which skips the logging of the last trial hence we need to exclude 
                                           the last trial also from the .lick file)
    
    Parameters
    ----------
    path : str
        path to the directory containinf the .lick files to concatenate.
    
    skip_last : boolean
        if True, it will remove the last trial (both the trial number and each corresponding lick)

    Returns
    -------
    2d array
        new 2d array with same original structure (column0: trial number; column1: lick time).

    """
    pre_list = os.listdir(path)
    lick_files = [x for x in pre_list if 'lick' in x]
    
    Concat_trials = [0]  
    Concat_licks = [0]
        
    for lickfile in lick_files:
        new_path = '{}\{}'.format(path,lickfile)
        try:
            B = load_lickfile(new_path)
            B[:,0] = [B[i,0]+Concat_trials[-1] for i in range(len(B))]
            Concat_trials = np.append(Concat_trials,B[:,0])
            Concat_licks = np.append(Concat_licks,B[:,1])
            uncut = len(Concat_trials)
            if skip_last:
                Concat_trials = Concat_trials[Concat_trials != Concat_trials[-1]]
                delta = uncut-len(Concat_trials)
                Concat_licks = Concat_licks[:-delta]  
        except:
            pass
        
    Concat_trials = Concat_trials.astype(int)
    all_conc = np.zeros((len(Concat_licks),2))
    all_conc[:,0] = Concat_trials
    all_conc[:,1] = Concat_licks
    return np.delete(all_conc,0,0)


if __name__ == '__main__':
    import time
    
    startTime = time.time()

    path = r"D:/F.LARENO.FACCINI/Preliminary Results/Behaviour/Group 14/6409/Training/T9.1/6409_2020_06_11_11_55_35.lick"
    param = r"D:/F.LARENO.FACCINI/Preliminary Results/Behaviour/Group 14/6409/Training/T9.1/6409_2020_06_11_11_55_35.param"
    B = load_lickfile(path)  
    
    fig, ax = plt.subplots(2)
    scatter_lick(B, ax=ax[0], color='r')
    psth_lick(B, ax=ax[1], color='r')
    
    rand = extract_random_delay(param)
    delays, licks_by_delay = separate_by_delay(rand,B)
    
    # nostim, stim = separate_by_condition(B)
    
    # delay_400, delay_900, delay_900_400, delay_900_900, delay_400_400, delay_400_900 = d
    print ('The script took {0} second !'.format(time.time() - startTime))
    
