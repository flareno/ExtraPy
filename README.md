# ExtraPy
Python3 package to analyse and handle electrophyiological extracellular recordings

For the moment there is only the filters.py
The base of this script was the filter_signal function created by Sam Garcia, I have adapted this function also to a Notch filter.

The expected modules are:

1) Behaviour
    - load lick and param files
    - plot scatter plots
    - PSTH of lick
    - analyze training with different delays
    
2) Electrophysiology
    - Handle files
    - Filters (thanks to Sam Garcia)
    - Spike sorting (post TDC)
    - Phase-locking (by Lilian Goepp)
    - Scalogram (by Sam Garcia)
