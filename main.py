# Project Libraries
import data
import functions as fn

# Generic Libraries
import numpy as np
import pandas as pd

# ----- Market information
df_bitfinex_tob = pd.DataFrame(data.read_file(file_name = "orderbooks_05jul21.json", folder_route = "files/")['bitfinex']).transpose().reset_index()
df_bitfinex_tob['index'] = pd.to_datetime(df_bitfinex_tob['index'])
df_bitfinex_tob = df_bitfinex_tob.set_index('index').resample('S').last().ffill()
for column in df_bitfinex_tob.columns:
    df_bitfinex_tob[column] = df_bitfinex_tob[column].apply(lambda x: x['0'])
df_bitfinex_tob = df_bitfinex_tob.reset_index().rename(columns = {'index':'timestamp'})

# SLA Conditions
contracted_volume = .0001
platform_fee = .000025

# Initial Conditions Data Frames
df_info, df_inventory, df_rebalance = fn.dataframes()

# ----- Market information
df_bitfinex_tob = pd.DataFrame(data.read_file(file_name = "orderbooks_05jul21.json", folder_route = "files/")['bitfinex']).transpose().reset_index()
df_bitfinex_tob['index'] = pd.to_datetime(df_bitfinex_tob['index'])
df_bitfinex_tob = df_bitfinex_tob.set_index('index').resample('S').last().ffill()
for column in df_bitfinex_tob.columns:
    df_bitfinex_tob[column] = df_bitfinex_tob[column].apply(lambda x: x['0'])
df_bitfinex_tob = df_bitfinex_tob.reset_index().rename(columns = {'index':'timestamp'})

# SLA Conditions
contracted_volume = .0001
platform_fee = .000025

# Initial Conditions Data Frames
df_info, df_inventory, df_rebalance = fn.dataframes()

# Initial Order
df_orders = pd.DataFrame([
    [df_bitfinex_tob.iloc[0]['timestamp'], df_bitfinex_tob.iloc[0]['timestamp']],
    [1,2], ['buy','sell'], [df_bitfinex_tob.iloc[0]['bid'], df_bitfinex_tob.iloc[0]['ask']],
    [contracted_volume, contracted_volume], ['BTC/USDT','BTC/USDT']
    ], 
    index =  ['timestamp','order_id','side','price', 'order_amount','symbol'],
    columns = [0,1]
).transpose()

for side_filled in ['ask','bid']:
    filled = fn.filled_volume(
        size_variation = df_bitfinex_tob.iloc[1][side_filled+'_size'] - df_bitfinex_tob.iloc[0][side_filled+'_size'],
        operation = side_filled, 
        price_variation = df_bitfinex_tob.iloc[1][side_filled] - df_orders[df_orders['side'] == fn.names(side_filled)].iloc[-1]['price'], 
        constant_position_base = contracted_volume
    )
    if filled > 0:            
            df_trades = fn.execute_trade(
                df_bitfinex_tob = df_bitfinex_tob,
                df_orders = df_orders,
                side = side_filled,
                i = 1,
                passed_index = 0, 
                current_id = 1, 
                traded_volume = filled,
                trade_fee = platform_fee,
                first_input = True)
            
            # ---- Liquidity Pool Adjustment
            passed_index_inventory = df_inventory.index[-1] + 1
            fn.inventory(
                 index_inventory = passed_index_inventory,
                 df_trades = df_trades, 
                 df_inventory = df_inventory
                 )

            if len(df_rebalance) == 0:
                index_rebalance = 0
            else:
                index_rebalance = df_rebalance.index[-1] + 1
            fn.rebalance(
                trade_fee = platform_fee,
                rebalance_index = index_rebalance,
                df_inventory = df_inventory, 
                df_rebalance = df_rebalance,
                df_trades = df_trades,
                inventory_index = df_inventory.index[-1] + 1
                )
            # ----

            last_id = df_orders.iloc[-1]['order_id']
            fn.place_order(
                i = 1,
                df_bitfinex_tob = df_bitfinex_tob,
                df_orders = df_orders,
                passed_index = 2,
                side = side_filled,
                current_id = last_id + 1, 
                amount = contracted_volume
                )
            
for period in range(2,len(df_bitfinex_tob)):
    for side_filled in ['ask','bid']:
        filled = fn.filled_volume(
            size_variation = df_bitfinex_tob.iloc[period][side_filled+'_size'] - df_bitfinex_tob.iloc[period - 1][side_filled+'_size'],
            operation = side_filled, 
            price_variation = df_bitfinex_tob.iloc[period][side_filled] - df_orders[df_orders['side'] == fn.names(side_filled)].iloc[-1]['price'], 
            constant_position_base = contracted_volume
        )
        if filled > 0:
            try:
                last_id_trades = df_trades.iloc[-1]['trade_id']
                passed_index_trades = df_trades.index[-1] + 1
                fn.execute_trade(
                    df_bitfinex_tob = df_bitfinex_tob,
                    df_trades = df_trades,
                    df_orders = df_orders,
                    side = side_filled,
                    i = period,
                    passed_index = passed_index_trades, 
                    current_id = last_id_trades + 1, 
                    traded_volume = filled, 
                    trade_fee = platform_fee
                    )
            except:
                df_trades = fn.execute_trade(
                df_bitfinex_tob = df_bitfinex_tob,
                df_orders = df_orders,
                side = side_filled,
                i = 1,
                passed_index = 0, 
                current_id = 1, 
                traded_volume = filled,
                trade_fee = platform_fee,
                first_input = True)
            
            # ---- Liquidity Pool Adjustment
            passed_index_inventory = df_inventory.index[-1] + 1
            fn.inventory(
                 index_inventory = passed_index_inventory,
                 df_trades = df_trades, 
                 df_inventory = df_inventory
                 )
            
            if len(df_rebalance) == 0:
                index_rebalance = 0
            else:
                index_rebalance = df_rebalance.index[-1] + 1
            fn.rebalance(
                trade_fee = platform_fee,
                rebalance_index = index_rebalance,
                df_inventory = df_inventory, 
                df_rebalance = df_rebalance,
                df_trades = df_trades,
                inventory_index = df_inventory.index[-1] + 1
                )
            # ----

            last_id_orders = df_orders.iloc[-1]['order_id']
            passed_index_orders = df_orders.index[-1] + 1
            fn.place_order(
                i = period,
                df_bitfinex_tob = df_bitfinex_tob,
                df_orders = df_orders,
                passed_index = passed_index_orders,
                side = side_filled,
                current_id = last_id_orders + 1, 
                amount = contracted_volume
                )