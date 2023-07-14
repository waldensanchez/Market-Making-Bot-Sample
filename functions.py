
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# ----- Generic libraries
import pandas as pd
import numpy as np

# ----- Useful dataframes
def dataframes():
    # Informative dataframe
    df_info = pd.DataFrame({
        'bid_volume': [0.0001],
        'ask_volume': [0.0001],
        'commission': [0.000025]
    })

    # Inventory dataframe
    df_inventory = pd.DataFrame({
        'timestamp': [0],
        'base (BTC)': [5],
        'quote (USDT)': [500000]
    })

    # Rebalance dataframe
    df_rebalances = pd.DataFrame(columns = ['timestamp', 'sent', 'recieved', 'price', 'fee'])

    return df_info, df_inventory, df_rebalances

# ---- Textt for Data Frames
def names(name):
    if name == 'bid':
        return 'buy'
    elif name == 'ask':
        return 'sell'
    else:
        'Function Failure: names'

# Position valuation
def filled_volume(size_variation: float, price_variation: float, operation: str = None, constant_position_base: float = .0001):
    # Ask
    if operation == 'ask':
        if price_variation > 0:
            current_position = constant_position_base
        elif price_variation == 0:
            if size_variation > 0:
                current_position = 0
            else:
                if size_variation <= constant_position_base:
                    current_position = size_variation
                else:
                    current_position = constant_position_base
        else:
            current_position = 0
    # Bid
    if operation == 'bid':
        if price_variation < 0:
            current_position = constant_position_base
        elif price_variation == 0:
            if size_variation > 0:
                current_position = 0
            else:
                if size_variation <= constant_position_base:
                    current_position = size_variation
                else:
                    current_position = constant_position_base
        else:
            current_position = 0
    return current_position

# ---- Trade
def execute_trade(df_bitfinex_tob,df_orders,side,passed_index, current_id, traded_volume, trade_fee,i, first_input:bool = False, df_trades = None):
    if first_input == True:
        df_output = pd.DataFrame([
        df_bitfinex_tob.iloc[1]['timestamp'],
        df_orders[df_orders['side'] == names(side)].iloc[-1]['order_id'],
        1, names(side), df_orders[df_orders['side'] == names(side)].iloc[-1]['price'], 'BTC/USDT',
        traded_volume, df_orders[df_orders['side'] == names(side)].iloc[-1]['order_amount'],
        trade_fee * traded_volume * df_orders[df_orders['side'] == names(side)].iloc[-1]['price']
    ], index = ['timestamp','order_id','trade_id','side','price','symbol','filled_amount','order_amount','fee']
    ).transpose()
        return df_output
    else:
        df_trades.at[passed_index,'timestamp'] = df_bitfinex_tob.iloc[i]['timestamp']
        df_trades.at[passed_index,'order_id'] = df_orders[df_orders['side'] == names(side)].iloc[-1]['order_id']
        df_trades.at[passed_index,'trade_id'] = current_id
        df_trades.at[passed_index,'side'] = names(side)
        df_trades.at[passed_index,'price'] = df_orders[df_orders['side'] == names(side)].iloc[-1]['price']
        df_trades.at[passed_index,'symbol'] = 'BTC/USDT'
        df_trades.at[passed_index,'filled_amount'] = traded_volume
        df_trades.at[passed_index,'order_amount'] = df_orders[df_orders['side'] == names(side)].iloc[-1]['order_amount']
        df_trades.at[passed_index,'fee'] = trade_fee * traded_volume * df_orders[df_orders['side'] == names(side)].iloc[-1]['price']

# ---- Orders
def place_order(i, df_orders, df_bitfinex_tob, passed_index, side, current_id, amount):
    df_orders.at[passed_index, 'timestamp'] = df_bitfinex_tob.iloc[i]['timestamp']
    df_orders.at[passed_index, 'order_id'] = current_id
    df_orders.at[passed_index, 'side'] = names(side)
    df_orders.at[passed_index, 'price'] = df_bitfinex_tob.iloc[i][side]
    df_orders.at[passed_index, 'order_amount'] = amount
    df_orders.at[passed_index, 'symbol'] = 'BTC/USDT'

# ----- Inventory
def inventory(index_inventory,df_trades, df_inventory):
    if df_trades['side'].iloc[-1] == "sell":

        df_inventory.at[index_inventory, 'timestamp'] = df_trades['timestamp'].iloc[-1]
        df_inventory.at[index_inventory, 'base (BTC)'] = df_trades['filled_amount'].iloc[-1] + df_inventory.at[index_inventory-1, 'base (BTC)']
        df_inventory.at[index_inventory, 'quote (USDT)'] = df_inventory.at[index_inventory-1, 'quote (USDT)'] - df_trades['filled_amount'].iloc[-1]*df_trades['price'].iloc[-1]

    elif df_trades['side'].iloc[-1] == "buy":

        df_inventory.at[index_inventory, 'timestamp'] = df_trades['timestamp'].iloc[-1]
        df_inventory.at[index_inventory, 'base (BTC)'] = df_inventory.at[index_inventory-1, 'base (BTC)'] - df_trades['filled_amount'].iloc[-1]
        df_inventory.at[index_inventory, 'quote (USDT)'] = df_inventory.at[index_inventory-1, 'quote (USDT)'] + df_trades['filled_amount'].iloc[-1]*df_trades['price'].iloc[-1]

# ---- Rebalance
def rebalance(trade_fee, df_trades, df_inventory, df_rebalance, rebalance_index, inventory_index):
    
    decimals_usdt=10e18
    decimals_btc=10e8
    decimals_btcusdt=int(decimals_btc/decimals_usdt)
    decimals_usdtbtc=int(decimals_usdt/decimals_btc)
    initial_base = df_inventory.at[0, 'base (BTC)']
    last_base = df_inventory.at[inventory_index - 1, 'base (BTC)']
    initial_quote = df_inventory.at[0, 'quote (USDT)']
    last_quote = df_inventory.at[inventory_index - 1, 'quote (USDT)']

  

    if df_inventory['base (BTC)'].iloc[-1] < 4.9 :
        swap_price = decimals_usdtbtc/(((int(np.sqrt(df_trades['price'].iloc[-1])*96)*2)/(2*96))*2)
        swap_amount = initial_base - last_base
        swap_fee = trade_fee * decimals_usdtbtc/swap_price * swap_amount

        df_rebalance.at[rebalance_index,'timestamp'] = df_inventory['timestamp'].iloc[-1]
        df_rebalance.at[rebalance_index,'sent'] = 'USDT'
        df_rebalance.at[rebalance_index,'recieved'] = 'BTC'
        df_rebalance.at[rebalance_index,'price'] = swap_price
        df_rebalance.at[rebalance_index,'fee'] = swap_fee

        df_inventory.at[inventory_index, 'timestamp'] = df_inventory.at[inventory_index - 1, 'timestamp']
        df_inventory.at[inventory_index, 'base (BTC)'] = last_base  + decimals_usdtbtc/(int(swap_price - swap_fee)/(2*96))*2 * swap_amount
        df_inventory.at[inventory_index, 'quote (USDT)'] = last_quote - swap_amount

    elif df_inventory['quote (USDT)'].iloc[-1] < 499980:
        swap_price = decimals_usdtbtc/(((int(np.sqrt(df_trades['price'].iloc[-1])*96)*2)/(2*96))*2)
        swap_amount = initial_quote - last_quote
        swap_fee = trade_fee * decimals_btcusdt/swap_price * swap_amount

        df_rebalance.at[rebalance_index,'timestamp'] = df_inventory['timestamp'].iloc[-1]
        df_rebalance.at[rebalance_index,'sent'] = 'BTC'
        df_rebalance.at[rebalance_index,'recieved'] = 'USDT'
        df_rebalance.at[rebalance_index,'price'] = swap_price
        df_rebalance.at[rebalance_index,'fee'] = trade_fee*swap_price

        df_inventory.at[inventory_index, 'timestamp'] = df_inventory.at[inventory_index - 1, 'timestamp']
        df_inventory.at[inventory_index, 'base (BTC)'] = last_base - swap_amount
        df_inventory.at[inventory_index, 'quote (USDT)'] = decimals_usdtbtc/(int(swap_price)/(2*96))*2 * swap_amount + last_quote