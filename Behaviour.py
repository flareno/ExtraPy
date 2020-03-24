# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:36:18 2019

@author: F.LARENO-FACCINI
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


    
def load_lickfile(file_path, sep="\t", header=None):
    A = np.array(pd.read_csv(file_path, sep=sep, header=header))
    return np.array([[A[i][0], float(A[i][1].replace(',','.'))] for i in range(len(A))])


def scatter_lick(licks, ax=None, x_label='Time (s)', y_label='Trial Number', **kwargs):
    if len(licks)>0:
        ax = ax or plt.gca()
        x_label = x_label
        y_label = y_label
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        return ax.scatter(licks[:,1], licks[:,0], marker = "|", **kwargs)
    else:
        pass


def PSTH_lick(licks, ax=None, lentrial=10, samp_period=0.01, **kwargs):
    ax = ax or plt.gca()
   
    if len(licks)>0:
        bins = np.arange(0,lentrial+samp_period,samp_period)
        return ax.hist(licks[:,1], bins, density=1, **kwargs)
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
    del(random[0])
    
    for i in random:
        temp__ = i.split(' ')[-1]
        temp__ = temp__.split('\n')[0]
        r_time.append(temp__)
      
    r_time = np.asarray([[r_time[i].replace(',','.')] for i in range(len(r_time))])
    # r_time = np.asarray(r_time)
    RandomT = [float(r_time[i]) for i in range(len(r_time))]
    return [[float(RandomT[i]), int(i+1)] for i in range (len(RandomT))]


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
    l400 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 400ms between the last cue and the reward
        
    l900 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 900ms between the last cue and the reward
        
    l900_400 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 400ms and of 900ms at trial-1
        
    l900_900 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 900ms for the last two trials (trial and trial-1)
        
    l400_400 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 900ms for the last two trials (trial and trial-1)
        
    l400_900 : 2D numpy array
        Array containing every lick event and the corresponding trial that had a delay of 900ms and of 400ms at trial-1
    """
    
    d400, d900, d900_900, d400_400, d400_900, d900_400= [], [], [], [], [], []
    
    for idx,(d,t) in enumerate(random):
        if d == delay1:
            d400.append([d,t])
            if idx == 0:
                pass
            elif random[idx-1][0] == delay1:
                d400_400.append(random[idx])
            elif random[idx-1][0] == delay2:
                d900_400.append(random[idx])
                
        elif d == delay2:
            d900.append([d,t])
            if idx == 0:
                pass
            elif random[idx-1][0] == delay1:
                d400_900.append(random[idx])
            elif random[idx-1][0] == delay2:
                d900_900.append(random[idx])
                
    d400 = np.asarray(d400)
    d900 = np.asarray(d900)
    d900_400 = np.asarray(d900_400)
    d400_400 = np.asarray(d400_400)
    d400_900 = np.asarray(d400_900)
    d900_900 = np.asarray(d900_900)
    
    l400 = []
    l900 = []
    l900_400 = []
    l400_400 = []
    l400_900 = []
    l900_900 = []
    
    
    for t,l in licks:
        for d,tr in d400:
            if t==tr:
                l400.append([t,l])
        for d,tr in d900:
            if t==tr:
                l900.append([t,l])
        for d,tr in d400_400:
            if t==tr:
                l400_400.append([t,l])
        for d,tr in d900_400:
            if t==tr:
                l900_400.append([t,l])
        for d,tr in d400_900:
            if t==tr:
                l400_900.append([t,l])
        for d,tr in d900_900:
            if t==tr:
                l900_900.append([t,l])
    
    l400 = np.asarray(l400)
    l900 = np.asarray(l900)
    l400_400 = np.asarray(l400_400)
    l400_900 = np.asarray(l400_900)
    l900_400 = np.asarray(l900_400)
    l900_900 = np.asarray(l900_900)

            
    return l400, l900, l900_400, l900_900, l400_400, l400_900, (d400, d900, d900_400, d900_900, d400_400, d400_900)



if __name__ == '__main__':
    

    path = r"D:/F.LARENO.FACCINI/Preliminary Results/Behaviour/Group 12/1089/Training/1089_2019_12_09_14_29_45.lick"
    param = r"D:/F.LARENO.FACCINI/Preliminary Results/Behaviour/Group 12/1089/Training/1089_2019_12_09_14_29_45.param"
    B = load_lickfile(path)  
    
    fig, ax = plt.subplots(2)
    scatter_lick(B, ax=ax[0], color='r')
    
    psth = PSTH_lick(B, ax=ax[1], color='r')
    
    rand = extract_random_delay(param)
    
   