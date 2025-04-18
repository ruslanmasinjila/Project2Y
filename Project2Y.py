##########################################################################################
# Project2Y (PROJECT YIN AND YANG)
# AUTHOR: RUSLAN MASINJILA
# USAGE: python Project2Y.py <scan | step> <offset> <symbol>
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
if len(sys.argv) != 4:
    print("USAGE: python Project2Y.py <scan | step> <offset> <symbol>")
    sys.exit(1)
    
mode   = sys.argv[1]
offset = int(sys.argv[2])

if(sys.argv[3]!='all'):
    symbols= [sys.argv[3]]
    
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
            
            sixth_sequence_indices  = sorted_merged_list[-1]
            fifth_sequence_indices  = sorted_merged_list[-2]
            fourth_sequence_indices = sorted_merged_list[-3]
            third_sequence_indices  = sorted_merged_list[-4]
            second_sequence_indices = sorted_merged_list[-5]
            first_sequence_indices  = sorted_merged_list[-6]
            
            
            length_sixth_sequence   = len(sixth_sequence_indices)
            length_fifth_sequence   = len(fifth_sequence_indices)
            length_fourth_sequence  = len(fourth_sequence_indices)
            length_third_sequence   = len(third_sequence_indices)
            length_second_sequence  = len(second_sequence_indices)
            length_first_sequence   = len(first_sequence_indices)
            
            sixth_sequence_head_open    = rates_frame['open'].iloc[sixth_sequence_indices[-1]]
            sixth_sequence_head_close   = rates_frame['close'].iloc[sixth_sequence_indices[-1]]
            sixth_sequence_is_green = ( sixth_sequence_head_close - sixth_sequence_head_open ) > 0
            sixth_sequence_is_red   = ( sixth_sequence_head_close - sixth_sequence_head_open ) < 0
            
            fifth_sequence_head_open    = rates_frame['open'].iloc[fifth_sequence_indices[-1]]
            fifth_sequence_head_close   = rates_frame['close'].iloc[fifth_sequence_indices[-1]]
            fifth_sequence_is_green = ( fifth_sequence_head_close - fifth_sequence_head_open ) > 0
            fifth_sequence_is_red   = ( fifth_sequence_head_close - fifth_sequence_head_open ) < 0
            
            fourth_sequence_head_open   = rates_frame['open'].iloc[fourth_sequence_indices[-1]]
            fourth_sequence_head_close  = rates_frame['close'].iloc[fourth_sequence_indices[-1]]
            fourth_sequence_is_green = ( fourth_sequence_head_close - fourth_sequence_head_open ) > 0
            fourth_sequence_is_red   = ( fourth_sequence_head_close - fourth_sequence_head_open ) < 0
            
            third_sequence_head_open   = rates_frame['open'].iloc[third_sequence_indices[-1]]
            third_sequence_head_close  = rates_frame['close'].iloc[third_sequence_indices[-1]]
            third_sequence_is_green = ( third_sequence_head_close -third_sequence_head_open ) > 0
            third_sequence_is_red   = ( third_sequence_head_close - third_sequence_head_open ) < 0
            
            second_sequence_head_open   = rates_frame['open'].iloc[second_sequence_indices[-1]]
            second_sequence_head_close  = rates_frame['close'].iloc[second_sequence_indices[-1]]
            second_sequence_is_green = ( second_sequence_head_close -second_sequence_head_open ) > 0
            second_sequence_is_red   = ( second_sequence_head_close - second_sequence_head_open ) < 0
            
            first_sequence_head_open   = rates_frame['open'].iloc[first_sequence_indices[-1]]
            first_sequence_head_close  = rates_frame['close'].iloc[first_sequence_indices[-1]]
            first_sequence_is_green = ( first_sequence_head_close -first_sequence_head_open ) > 0
            first_sequence_is_red   = ( first_sequence_head_close - first_sequence_head_open ) < 0
            
            sixth_sequence_highest_open = rates_frame['open'].iloc[sixth_sequence_indices].max()
            sixth_sequence_lowest_open  = rates_frame['open'].iloc[sixth_sequence_indices].min()
            sixth_sequence_highest_high  = rates_frame['high'].iloc[sixth_sequence_indices].max()
            sixth_sequence_lowest_low    = rates_frame['low'].iloc[sixth_sequence_indices].min()
            sixth_sequence_highest_close = rates_frame['close'].iloc[sixth_sequence_indices].max()
            sixth_sequence_lowest_close  = rates_frame['close'].iloc[sixth_sequence_indices].min()            
            
            fifth_sequence_highest_open = rates_frame['open'].iloc[fifth_sequence_indices].max()
            fifth_sequence_lowest_open  = rates_frame['open'].iloc[fifth_sequence_indices].min()
            fifth_sequence_highest_high  = rates_frame['high'].iloc[fifth_sequence_indices].max()
            fifth_sequence_lowest_low    = rates_frame['low'].iloc[fifth_sequence_indices].min()
            fifth_sequence_highest_close = rates_frame['close'].iloc[fifth_sequence_indices].max()
            fifth_sequence_lowest_close  = rates_frame['close'].iloc[fifth_sequence_indices].min()

            

            fourth_sequence_highest_open = rates_frame['open'].iloc[fourth_sequence_indices].max()
            fourth_sequence_lowest_open  = rates_frame['open'].iloc[fourth_sequence_indices].min()
            fourth_sequence_highest_high  = rates_frame['high'].iloc[fourth_sequence_indices].max()
            fourth_sequence_lowest_low    = rates_frame['low'].iloc[fourth_sequence_indices].min()
            fourth_sequence_highest_close = rates_frame['close'].iloc[fourth_sequence_indices].max()
            fourth_sequence_lowest_close  = rates_frame['close'].iloc[fourth_sequence_indices].min()

            third_sequence_highest_open = rates_frame['open'].iloc[third_sequence_indices].max()
            third_sequence_lowest_open  = rates_frame['open'].iloc[third_sequence_indices].min()
            third_sequence_highest_high  = rates_frame['high'].iloc[third_sequence_indices].max()
            third_sequence_lowest_low    = rates_frame['low'].iloc[third_sequence_indices].min()
            third_sequence_highest_close = rates_frame['close'].iloc[third_sequence_indices].max()
            third_sequence_lowest_close  = rates_frame['close'].iloc[third_sequence_indices].min()            

            second_sequence_highest_open = rates_frame['open'].iloc[second_sequence_indices].max()
            second_sequence_lowest_open  = rates_frame['open'].iloc[second_sequence_indices].min()
            second_sequence_highest_high  = rates_frame['high'].iloc[second_sequence_indices].max()
            second_sequence_lowest_low    = rates_frame['low'].iloc[second_sequence_indices].min()
            second_sequence_highest_close = rates_frame['close'].iloc[second_sequence_indices].max()
            second_sequence_lowest_close  = rates_frame['close'].iloc[second_sequence_indices].min()
            
            first_sequence_highest_open = rates_frame['open'].iloc[first_sequence_indices].max()
            first_sequence_lowest_open  = rates_frame['open'].iloc[first_sequence_indices].min()
            first_sequence_highest_high  = rates_frame['high'].iloc[first_sequence_indices].max()
            first_sequence_lowest_low    = rates_frame['low'].iloc[first_sequence_indices].min()
            first_sequence_highest_close = rates_frame['close'].iloc[first_sequence_indices].max()
            first_sequence_lowest_close  = rates_frame['close'].iloc[first_sequence_indices].min()           

                             
            ##########################################################################################
            
            if((first_sequence_is_red     and 
                second_sequence_is_green  and 
                third_sequence_is_red     and 
                fourth_sequence_is_green  and
                fifth_sequence_is_red     and
                sixth_sequence_is_green)):
                if(sixth_sequence_highest_high < first_sequence_lowest_low):
                    difference = abs((sixth_sequence_highest_high - first_sequence_lowest_low)/(symbol_info.point)) - spread
                    if(difference >= 50):
                        if(sixth_sequence_highest_close > fourth_sequence_highest_high):
                            if(fourth_sequence_highest_high > fifth_sequence_highest_high):
                                if(first_sequence_lowest_low < second_sequence_lowest_low):
                                    signal = 'BUY '
                                    beep = 1

            if((first_sequence_is_green   and 
                second_sequence_is_red    and 
                third_sequence_is_green   and 
                fourth_sequence_is_red    and
                fifth_sequence_is_green   and
                sixth_sequence_is_red)):
                if(sixth_sequence_lowest_low > first_sequence_highest_high):
                    difference = abs((sixth_sequence_lowest_low - first_sequence_highest_high)/(symbol_info.point)) - spread
                    if(difference >= 50):
                        if(sixth_sequence_lowest_close < fourth_sequence_lowest_low):
                            if(fourth_sequence_lowest_low < fifth_sequence_lowest_low):
                                if(first_sequence_highest_high > second_sequence_highest_high):
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