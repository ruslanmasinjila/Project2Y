##########################################################################################
# ProjectQM (PROJECT QUASIMODO)
# AUTHOR: RUSLAN MASINJILA
# USAGE: python ProjectQM.py <scan | step> <offset>
##########################################################################################

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from itertools import groupby
import time
import os
import sys
import winsound

duration  = 50
freq      = 1500


# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print('initialize() FAILED, ERROR CODE =',mt5.last_error())
    quit()

# MT5 TIMEFRAME
M1   = mt5.TIMEFRAME_M1
M2   = mt5.TIMEFRAME_M2
M3   = mt5.TIMEFRAME_M3
M4   = mt5.TIMEFRAME_M4
M5   = mt5.TIMEFRAME_M5
M6   = mt5.TIMEFRAME_M6
M10  = mt5.TIMEFRAME_M10
M12  = mt5.TIMEFRAME_M12
M15  = mt5.TIMEFRAME_M15
M20  = mt5.TIMEFRAME_M20
M30  = mt5.TIMEFRAME_M30
H1   = mt5.TIMEFRAME_H1
H2   = mt5.TIMEFRAME_H2
H3   = mt5.TIMEFRAME_H3
H4   = mt5.TIMEFRAME_H4
H6   = mt5.TIMEFRAME_H6
H8   = mt5.TIMEFRAME_H8
H12  = mt5.TIMEFRAME_H12
D1   = mt5.TIMEFRAME_D1
W1   = mt5.TIMEFRAME_W1
MN1  = mt5.TIMEFRAME_MN1

symbols = None
with open('symbols.txt') as f:
    symbols = [line.rstrip('\n') for line in f]
    
# TIMEFRAMES
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
strTimeframe   = ['M1','M2','M3','M4','M5','M6','M10','M12','M15','M20','M30','H1','H2','H3','H4','H6','H8','H12','D1']


mode                = "scan"
num_candles         = 100
sleep_time          = 5


offset              = 0
if len(sys.argv) != 3:
    print("USAGE: python ProjectQM.py <scan | step> <offset>")
    sys.exit(1)
    
mode   = sys.argv[1]
offset = int(sys.argv[2])

##########################################################################################

def get_consecutive_indices(lst):
    if not lst:
        return []

    consecutive_lists = []
    
    for _, group in groupby(enumerate(lst), lambda x: x[0] - x[1]):
        consecutive_lists.append([item[1] for item in group])

    return consecutive_lists


def get_signals():

    beep = 0

    # Create dataframe for holding the results
    results_dataframe = pd.DataFrame(columns = ['Symbol']+strTimeframe+['Spread'])
    
    for symbol in symbols:
           
        signals = []
        
        for t in range(len(mt5Timeframe)):
        
            signal = '-----'
            
            ##########################################################################################
            
            # Calculate the spread for the symbol
            symbol_info  = mt5.symbol_info(symbol)
            ask          = symbol_info.ask
            bid          = symbol_info.bid
            spread       = int((ask- bid)/(symbol_info.point))
            
            ##########################################################################################
                    
            # Get the rates for the symbol
            rates_frame  = getRates(symbol, mt5Timeframe[t], num_candles)
            
            
            # Find the difference between close and open
            rates_frame['diff']             = rates_frame['close'] - rates_frame['open']
            
            # Get all consecutive green and red candles
            green_candles                   = list(rates_frame[rates_frame['diff']>0].index)
            red_candles                     = list(rates_frame[rates_frame['diff']<0].index)
            zero_candles                    = list(rates_frame[rates_frame['diff']==0].index)
            
            consecutive_green_candles       = get_consecutive_indices(green_candles)
            consecutive_red_candles         = get_consecutive_indices(red_candles)
            consecutive_zero_candles        = get_consecutive_indices(zero_candles)
            
            # Merge the two lists
            merged_list = consecutive_green_candles + consecutive_red_candles + consecutive_zero_candles

            # Sort the merged list based on the first element of each inner list
            sorted_merged_list = sorted(merged_list, key=lambda x: x[0])
            ##########################################################################################
 
            W8_indices = sorted_merged_list[-1]
            W7_indices = sorted_merged_list[-2] 
            W6_indices = sorted_merged_list[-3]
            W5_indices = sorted_merged_list[-4]
            W4_indices = sorted_merged_list[-5]
            W3_indices  = sorted_merged_list[-6]
            W2_indices = sorted_merged_list[-7]
            W1_indices  = sorted_merged_list[-8]
            
            length_W8  = len(W8_indices)   
            length_W7  = len(W7_indices)
            length_W6  = len(W6_indices)
            length_W5  = len(W5_indices)
            length_W4  = len(W4_indices)
            length_W3  = len(W3_indices)
            length_W2  = len(W2_indices)
            length_W1  = len(W1_indices)
            
            W8_head_open   = rates_frame['open'].iloc[W8_indices[-1]]
            W8_head_close  = rates_frame['close'].iloc[W8_indices[-1]]
            W8_IS_G = ( W8_head_close - W8_head_open ) > 0
            W8_IS_R   = ( W8_head_close - W8_head_open ) < 0
            
            W7_head_open   = rates_frame['open'].iloc[W7_indices[-1]]
            W7_head_close  = rates_frame['close'].iloc[W7_indices[-1]]
            W7_IS_G = ( W7_head_close - W7_head_open ) > 0
            W7_IS_R   = ( W7_head_close - W7_head_open ) < 0
 
            W6_head_open   = rates_frame['open'].iloc[W6_indices[-1]]
            W6_head_close  = rates_frame['close'].iloc[W6_indices[-1]]
            W6_IS_G = ( W6_head_close - W6_head_open ) > 0
            W6_IS_R   = ( W6_head_close - W6_head_open ) < 0
            
            W5_head_open   = rates_frame['open'].iloc[W5_indices[-1]]
            W5_head_close  = rates_frame['close'].iloc[W5_indices[-1]]
            W5_IS_G = ( W5_head_close - W5_head_open ) > 0
            W5_IS_R   = ( W5_head_close - W5_head_open ) < 0
            
            W4_head_open   = rates_frame['open'].iloc[W4_indices[-1]]
            W4_head_close  = rates_frame['close'].iloc[W4_indices[-1]]
            W4_IS_G = ( W4_head_close - W4_head_open ) > 0
            W4_IS_R   = ( W4_head_close - W4_head_open ) < 0
            
            W3_head_open   = rates_frame['open'].iloc[W3_indices[-1]]
            W3_head_close  = rates_frame['close'].iloc[W3_indices[-1]]
            W3_IS_G = ( W3_head_close -W3_head_open ) > 0
            W3_IS_R   = ( W3_head_close - W3_head_open ) < 0
            
            W2_head_open   = rates_frame['open'].iloc[W2_indices[-1]]
            W2_head_close  = rates_frame['close'].iloc[W2_indices[-1]]
            W2_IS_G = ( W2_head_close -W2_head_open ) > 0
            W2_IS_R   = ( W2_head_close - W2_head_open ) < 0
            
            W1_head_open   = rates_frame['open'].iloc[W1_indices[-1]]
            W1_head_close  = rates_frame['close'].iloc[W1_indices[-1]]
            W1_IS_G = ( W1_head_close -W1_head_open ) > 0
            W1_IS_R   = ( W1_head_close - W1_head_open ) < 0
            
            W8_HO = rates_frame['open'].iloc[W8_indices].max()
            W8_LO  = rates_frame['open'].iloc[W8_indices].min()
            W8_HH  = rates_frame['high'].iloc[W8_indices].max()
            W8_LL    = rates_frame['low'].iloc[W8_indices].min()
            W8_HC = rates_frame['close'].iloc[W8_indices].max()
            W8_LC  = rates_frame['close'].iloc[W8_indices].min()
            
            W7_HO = rates_frame['open'].iloc[W7_indices].max()
            W7_LO  = rates_frame['open'].iloc[W7_indices].min()
            W7_HH  = rates_frame['high'].iloc[W7_indices].max()
            W7_LL    = rates_frame['low'].iloc[W7_indices].min()
            W7_HC = rates_frame['close'].iloc[W7_indices].max()
            W7_LC  = rates_frame['close'].iloc[W7_indices].min()
            
            W6_HO = rates_frame['open'].iloc[W6_indices].max()
            W6_LO  = rates_frame['open'].iloc[W6_indices].min()
            W6_HH  = rates_frame['high'].iloc[W6_indices].max()
            W6_LL    = rates_frame['low'].iloc[W6_indices].min()
            W6_HC = rates_frame['close'].iloc[W6_indices].max()
            W6_LC  = rates_frame['close'].iloc[W6_indices].min()
            
            W5_HO = rates_frame['open'].iloc[W5_indices].max()
            W5_LO  = rates_frame['open'].iloc[W5_indices].min()
            W5_HH  = rates_frame['high'].iloc[W5_indices].max()
            W5_LL    = rates_frame['low'].iloc[W5_indices].min()
            W5_HC = rates_frame['close'].iloc[W5_indices].max()
            W5_LC  = rates_frame['close'].iloc[W5_indices].min()
            
            W4_HO = rates_frame['open'].iloc[W4_indices].max()
            W4_LO  = rates_frame['open'].iloc[W4_indices].min()
            W4_HH  = rates_frame['high'].iloc[W4_indices].max()
            W4_LL    = rates_frame['low'].iloc[W4_indices].min()
            W4_HC = rates_frame['close'].iloc[W4_indices].max()
            W4_LC  = rates_frame['close'].iloc[W4_indices].min()

            W3_HO = rates_frame['open'].iloc[W3_indices].max()
            W3_LO  = rates_frame['open'].iloc[W3_indices].min()
            W3_HH  = rates_frame['high'].iloc[W3_indices].max()
            W3_LL    = rates_frame['low'].iloc[W3_indices].min()
            W3_HC = rates_frame['close'].iloc[W3_indices].max()
            W3_LC  = rates_frame['close'].iloc[W3_indices].min()            

            W2_HO = rates_frame['open'].iloc[W2_indices].max()
            W2_LO  = rates_frame['open'].iloc[W2_indices].min()
            W2_HH  = rates_frame['high'].iloc[W2_indices].max()
            W2_LL    = rates_frame['low'].iloc[W2_indices].min()
            W2_HC = rates_frame['close'].iloc[W2_indices].max()
            W2_LC  = rates_frame['close'].iloc[W2_indices].min()
            
            W1_HO = rates_frame['open'].iloc[W1_indices].max()
            W1_LO  = rates_frame['open'].iloc[W1_indices].min()
            W1_HH  = rates_frame['high'].iloc[W1_indices].max()
            W1_LL    = rates_frame['low'].iloc[W1_indices].min()
            W1_HC = rates_frame['close'].iloc[W1_indices].max()
            W1_LC  = rates_frame['close'].iloc[W1_indices].min()           

                             
            ##########################################################################################
            
            if(W1_IS_R and W2_IS_G and W3_IS_R and W4_IS_G and W5_IS_R and W6_IS_G and W7_IS_R and W8_IS_G):
                if(all (W1_HH > HH for HH in[ W2_HH,W3_HH])):
                    if(all(W1_LL > HH for HH in [W4_HH,W5_HH,W6_HH,W7_HH,W8_HH]) and all(W2_LL > HH for HH in [W4_HH,W5_HH,W6_HH,W7_HH,W8_HH])):
                        if(all(W5_LL < LL for LL in [W3_LL,W4_LL]) or all(W6_LL < LL for LL in [W3_LL,W4_LL])):
                            if(all(W5_LL < LL for LL in [W7_LL,W8_LL]) or all(W6_LL < LL for LL in [W7_LL,W8_LL])):
                                    difference = abs((W1_LL - W4_LL)/(symbol_info.point)) - spread
                                    if(difference >= 10):
                                        signal = 'BUY '
                                        beep = 1
            
            if(W1_IS_G and W2_IS_R and W3_IS_G and W4_IS_R and W5_IS_G and W6_IS_R and W7_IS_G and W8_IS_R):
                if(all(W1_LL < LL for LL in [W2_LL,W3_LL])):
                    if(all(W1_HH <  LL for LL in [W4_LL,W5_LL,W6_LL,W7_LL,W8_LL]) and all(W2_HH <  LL for LL in [W4_LL,W5_LL,W6_LL,W7_LL,W8_LL])):
                        if(all(W5_HH > HH for HH in[ W3_HH,W4_HH]) or all(W6_HH > HH for HH in[ W3_HH,W4_HH])):
                            if(all(W5_HH > HH for HH in[ W7_HH,W8_HH]) or all(W6_HH > HH for HH in[ W7_HH,W8_HH])):
                                    difference = abs((W1_HH - W4_HH)/(symbol_info.point)) - spread
                                    if(difference >= 10):
                                        signal = 'SELL'
                                        beep = 1
            


            ##########################################################################################
            
            signals.append(signal)

        ##########################################################################################
        
        new_row   = pd.DataFrame([[symbol]+signals+[spread]], columns=results_dataframe.columns)
        
        results_dataframe = pd.concat([results_dataframe, new_row], ignore_index=True)

        ##########################################################################################

    results_dataframe = results_dataframe.sort_values(by='Spread')
    results_dataframe = results_dataframe.reset_index(drop=True)
    
    ##########################################################################################
    
    # Filter out columns
    selected_columns = []
    for column_name in results_dataframe.columns:
        results = list(results_dataframe[column_name])
        if all(result == "-----" for result in results):
            pass
        else:
            selected_columns.append(column_name)
            
    results_dataframe = results_dataframe[selected_columns] 
    
    ##########################################################################################
    
    # Filter out rows
    selected_rows = []
    for index in results_dataframe.index:
        results = list(results_dataframe[results_dataframe.columns[1:-1]].iloc[index])
        if all(result == "-----" for result in results):
            pass
        else:
            selected_rows.append(index)
            
    results_dataframe = results_dataframe.iloc[selected_rows]

    ##########################################################################################
    
    if(beep == 1):
        winsound.Beep(freq, duration)
        
        
    ##########################################################################################
        
    return results_dataframe
    
    ##########################################################################################

def getRates(symbol, mt5Timeframe, num_candles):
    rates_frame =  mt5.copy_rates_from_pos(symbol, mt5Timeframe, offset, num_candles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################

# Clean Terminal Before Display
os.system('cls' if os.name == 'nt' else 'clear')

banner = ''
banner+='##############################   \n'
banner+='          SIGNALS                \n'
banner+='##############################   \n'
   

while(True):
    display = banner + f"\nMode: {mode} | Offset={offset}"
    print(display)
    print(get_signals())
    if(mode == "step"):
        input("Press Enter to Continue...")
        offset+=1
    elif(mode == "scan"):
        time.sleep(sleep_time)
    os.system('cls' if os.name == 'nt' else 'clear')
    
##########################################################################################