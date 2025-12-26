import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta, time
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

class TradingSimulator:
    # __init__ now takes 'month' and 'year', and no longer needs 'timestamp_trade'
    def __init__(self, price_data, milestones, initial_balance, month, year, goal, 
                 spread_pips=0.0, swap_long=0.0, swap_short=0.0, commission_per_lot=0.0):

        timestamp_start, timestamp_end = self.month_to_date_range(year, month)

        self.curr_stampend = pd.to_datetime(timestamp_start) 

        self.timestamp_start = pd.to_datetime(timestamp_start) 
        self.timestamp_end = pd.to_datetime(timestamp_end) 

        self.status = ''
        self.goal = goal
        self.previous_win = ''

        self.price_data = price_data
        self.milestones = milestones
        self.current_balance = initial_balance
        self.initial_balance = initial_balance
        
        self.current_index = 0

        self.current_level = self.get_current_level()
        # self.trade_time is no longer needed
        
        self.trade_log = []

        # Fee structure
        self.spread_pips = spread_pips
        self.swap_long = swap_long
        self.swap_short = swap_short
        self.commission_per_lot = commission_per_lot

    # This function is updated to calculate a specific month's range
    def month_to_date_range(self, year: int, month: int):
        # Ensure the month is valid
        if not 1 <= month <= 12:
            raise ValueError("Month must be an integer between 1 and 12")
        
        # Get the start of the month
        start_date = datetime(year, month, 1)
        
        # Calculate the end of the month by finding the start of the next month and subtracting one second
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        # Format the dates into strings
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
        
        return start_date_str, end_date_str

    def get_current_level(self):
        levels = self.milestones[
            (self.milestones['Starting Balance'] <= self.current_balance) &
            (self.milestones['Ending Balance'] > self.current_balance)
        ]
        if levels.empty:
            raise ValueError("No suitable level found for the current balance.")
        return levels.iloc[0]['Level']

    def get_lot_size(self):
        previous_level = self.current_level - 1
        lot_size = self.milestones[self.milestones['Level'] == previous_level]['Lot Size']
        if lot_size.empty:
            raise ValueError("Lot size for the previous level not found.")
        return lot_size.item()

    def calculate_pips_needed(self, profit_goal, lot_size):
        profit_per_pip = lot_size * 10.0
        pips_needed = profit_goal / profit_per_pip
        pips_needed_rounded = int(pips_needed) if pips_needed.is_integer() else int(pips_needed) + 1
        return pips_needed_rounded

    def calculate_pips_to_liquidate(self, account_balance, lot_size):
        profit_per_pip = lot_size * 10.0
        if profit_per_pip <= 0:
            return 0
        pips_to_liquidate = account_balance / profit_per_pip
        return pips_to_liquidate

    def simulate_trade(self, entry_price):
        initial_long_balance = self.current_balance / 2.0
        initial_short_balance = self.current_balance / 2.0

        # next_level = self.current_level + 1
        # next_level_starting = self.milestones[self.milestones['Level'] == next_level]['Starting Balance'].item()
        # profit_goal = next_level_starting - initial_long_balance
        
        ending_balance = self.milestones[self.milestones['Level'] == self.current_level]['Ending Balance'].item()
        profit_goal = ending_balance - initial_long_balance

        lot_size = self.get_lot_size()
        profit_per_pip = lot_size * 10.0

        pips_needed = profit_goal / profit_per_pip
        price_change_needed = pips_needed * 0.0001

        all_timestamps = self.price_data.index
        timestamps = all_timestamps[self.current_index:]

        if len(timestamps) == 0:
            return

        # entry_price = self.price_data.loc[timestamps[0], 'BidOpen']

        # Adjust Entry Price for Spread (Simulate buying at Ask = Bid + Spread)
        # For Long, we buy at Ask (Higher). For Short, we sell at Bid (Lower).
        # But wait, entry_price passed here is usually Bid.
        # So Long Entry = Bid + Spread. Short Entry = Bid.
        # Exit Long = Bid. Exit Short = Ask = Bid + Spread.
        
        long_entry_price = entry_price + (self.spread_pips * 0.0001)
        short_entry_price = entry_price # Sell at Bid

        target_long = long_entry_price + price_change_needed
        target_short = short_entry_price - price_change_needed

        long_account_balance = initial_long_balance
        short_account_balance = initial_short_balance

        for local_i, timestamp in enumerate(timestamps):
            row = self.price_data.loc[timestamp]
            self.curr_stampend = row.name

            if long_account_balance > 0:
                long_account_balance = initial_long_balance - (self.commission_per_lot * lot_size)

            if short_account_balance > 0:   
                short_account_balance = initial_short_balance - (self.commission_per_lot * lot_size)

            # Calculate PnL with Spread included
            # Long: Exit at Bid. Entry was Ask (Bid+Spread). PnL = (Bid_Current - Entry_Ask)
            long_pips = (row['BidHigh'] - long_entry_price) / 0.0001
            short_pips = (row['BidLow'] - short_entry_price) / 0.0001
            
            # Short: Exit at Ask (Bid_Current+Spread). Entry was Bid. PnL = (Entry_Bid - Exit_Ask)
            # short_pips = (short_entry_price - (row['BidLow'] + (self.spread_pips * 0.0001))) / 0.0001

            # --- Swap / Overnight Fee Calculation ---
            # Check if day changed from previous iteration (or start)
            # if local_i > 0:
            #     prev_timestamp = timestamps[local_i - 1]
            #     if timestamp.date() > prev_timestamp.date():
            #         # Apply swap
            #         swap_cost_long = self.swap_long * lot_size
            #         swap_cost_short = self.swap_short * lot_size
                    
            #         if long_account_balance > 0:
            #             long_account_balance -= swap_cost_long
            #         if short_account_balance > 0:
            #             short_account_balance -= swap_cost_short

            if long_account_balance > 0:
                if long_pips > 0:
                    long_account_balance += (long_pips * profit_per_pip)
                else:
                    long_account_balance += (short_pips * profit_per_pip)
            
            if short_account_balance > 0:
                if short_pips < 0:
                    short_account_balance += (-short_pips * profit_per_pip)
                else:
                    short_account_balance += (-long_pips * profit_per_pip)

            if long_account_balance <= 0:
                long_account_balance = 0

            if short_account_balance <= 0:
                short_account_balance = 0

            current_long_profit = long_account_balance - initial_long_balance
            if current_long_profit >= profit_goal:

                if local_i == 0 and self.previous_win == 'short':
                    continue
                    
                # self.current_balance = long_account_balance
                self.current_balance = ending_balance
                # self.current_index += (local_i + 1)
                self.current_index += (local_i)
                self.previous_win = 'long'
                return target_long

            current_short_profit = short_account_balance - initial_short_balance
            if current_short_profit >= profit_goal:

                if local_i == 0 and self.previous_win == 'long':
                    continue

                # self.current_balance = short_account_balance
                self.current_balance = ending_balance
                # self.current_index += (local_i + 1)
                self.current_index += (local_i)
                self.previous_win = 'short'
                return target_short

            if long_account_balance <= 0 and short_account_balance <= 0:
                self.current_balance = 0
                self.current_index = len(all_timestamps)
                self.previous_win = ''
                return None
        else:
            self.current_index = len(all_timestamps)

    def run(self):
        month_data = self.price_data.loc[self.timestamp_start:self.timestamp_end]
        print(f"Simulating trades from {self.timestamp_start} to {self.timestamp_end}")

        year = self.timestamp_start.year
        month = self.timestamp_start.month

        for start_timestamp in tqdm(month_data.index, desc="Simulating Trades", unit="trade"):
            self.current_index = self.price_data.index.get_loc(start_timestamp)

            # THIS IS THE KEY CHANGE: Trigger a trade at the start of every hour
            # It checks if the minutes and seconds are zero.

            if start_timestamp.minute != 30 or start_timestamp.second != 0:
                continue

            current_entry_price = self.price_data.loc[start_timestamp, 'BidOpen']
            exit_price = None

            while self.current_level <= self.goal and self.current_balance > 0 and self.current_index < len(self.price_data):
                exit_price = self.simulate_trade(current_entry_price)

                # if self.current_balance > 0:
                #     self.current_level = self.get_current_level()
                # else:
                #     self.status = 'Liquidated'
                #     break

                # if self.current_level >= self.goal:
                #     self.status = 'Successfull'
                #     break

                if exit_price is not None:
                    # ---- THIS IS THE CRITICAL FIX ----
                    current_entry_price = exit_price # Use the exit price for the next trade
                    # ---------------------------------
                    
                    self.current_level = self.get_current_level()
                    if self.current_level >= self.goal:
                        self.status = 'Successful'
                        break
                else:
                    # Trade failed (liquidated or ran out of data)
                    self.status = 'Liquidated' if self.current_balance == 0 else 'Failed'
                    break

            self.trade_log.append({
                'Start Timestamp': start_timestamp,
                'End Timestamp': self.curr_stampend,
                'Latest Level': self.current_level,
                'Ending Balance': self.current_balance,
                'Result': self.status,
            })

            self.current_balance = self.initial_balance
            self.current_level = self.get_current_level()

        trade_log_df = pd.DataFrame(self.trade_log)
        trade_log_df['Start Timestamp'] = pd.to_datetime(trade_log_df['Start Timestamp'])

        # Merge the 'is_stale' flag from the main price data into the trade log
        # based on the trade's starting timestamp.
        trade_log_df = pd.merge(
            trade_log_df, 
            self.price_data['is_stale'], 
            left_on='Start Timestamp', 
            right_index=True, 
            how='left'
        )

        # 1. Define the styling function
        def style_rows(row):
            # Highlight non-tradable/stale periods in green
            if row['is_stale']:
                return ['background-color: #C8E6C9'] * len(row)  # A light green color
            
            # Highlight the start of a new day in yellow
            if row['Start Timestamp'].time() == time(0, 0):
                return ['background-color: #FDFFB6'] * len(row)  # A light yellow color
            
            # Default style for other rows
            return [''] * len(row)

        # 2. Apply the new, intelligent style to the DataFrame
        styled_df = trade_log_df.style.apply(style_rows, axis=1)
        # styled_df.hide(['is_stale'], axis=1)

        # 3. Save the styled DataFrame to Excel
        file_dir = f"{year}-{month:02d}"
        os.makedirs(f"output/hourly/perhourdlhc/{file_dir}", exist_ok=True)
        file_path = f"output/hourly/perhourdlhc/{file_dir}/str_month_hourly_{year}_{month:02d}_simulation.xlsx"

        columns_to_save = [col for col in trade_log_df.columns if col != 'is_stale']

        # Use the styled object's to_excel method
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            styled_df.to_excel(writer, sheet_name='Trade Log', index=False, columns=columns_to_save)
        
        print(f"Simulation completed. Styled results saved to {file_path}.")

        # The rest of the code for plotting remains the same
        df = trade_log_df # Use the original df for plotting
        # This part of the visualization groups by day, which is still useful
        df['Date'] = df['Start Timestamp'].dt.date
        grouped = df.groupby('Date')['Latest Level'].max().reset_index()
        grouped.rename(columns={'Latest Level': 'Max Level'}, inplace=True)
        grouped['Max Level'] = grouped['Max Level'].round().astype(int)
        grouped['color'] = grouped['Max Level'].apply(lambda level: 'green' if level >= self.goal else 'red')

        plt.figure(figsize=(12, 8))
        plt.barh(grouped['Date'].astype(str), grouped['Max Level'], color=grouped['color'])
        plt.xlabel('Highest Level Reached')
        plt.ylabel('Date')
        plt.title('Highest Trading Level Reached per Day (from Hourly Attempts)')
        plt.tight_layout()
        
        # Save the plot to a file
        plt.savefig(f"output/hourly/perhourdlhc/{file_dir}/str_hourly_{year}_{month:02d}_simulation_chart.png")

# -------------------------
#  HOW TO USE THIS CLASS
# -------------------------

# 1. Load your data
price_data = pd.read_csv('staging/datecorrected-raw-price.csv', parse_dates=['Date'], index_col='Date')
price_data = price_data.resample('15min').ffill()

# STEP 2: NOW, check for stale data on this complete, filled-in DataFrame.
# A row is stale if the price hasn't changed from the previous 15-minute interval.
is_stale_price = price_data[['BidOpen', 'BidHigh', 'BidLow', 'BidClose']].diff().sum(axis=1) == 0

# Add the correctly calculated stale flag as a new column.
price_data['is_stale'] = is_stale_price

# 2. Load milestones
milestones = pd.read_csv('data/milestone.csv')

# 3. Create instance of simulator
initial_balance = 13.99
year = 2025
month = 11  # Integer from 1-12 (e.g., 1 for January)
goal = 10
# 'timestamp_trade' is no longer passed to the simulator
# Fee Configuration (Example)
spread_pips = 1.6 # 1.6 pips spread
swap_long = -5.0 # Cost $5 per lot per night
swap_short = 2.0 # Earn $2 per lot per night (positive swap)
commission = 7.0 # $7 per lot round turn

simulator = TradingSimulator(price_data, milestones, initial_balance, month, year, goal,
                             spread_pips=spread_pips, swap_long=swap_long, swap_short=swap_short, commission_per_lot=commission)

# 4. Run simulation
simulator.run()