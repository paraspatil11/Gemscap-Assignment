import pandas as pd
import json
import os

INPUT_FILE = r'C:\Gemscap\ticks_2025-12-16.ndjson' 

def process_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: File '{INPUT_FILE}' not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    data = []
    
    with open(INPUT_FILE, 'r') as f:
        for line_num, line in enumerate(f):
            if line.strip():
                try:
                    entry = json.loads(line)
                    data.append(entry)
                except json.JSONDecodeError:
                    continue

    if not data:
        print("Error: No valid data found in file.")
        return

    df = pd.DataFrame(data)
    
    df['ts'] = pd.to_datetime(df['ts'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce') # Handle non-numbers
    df['size'] = pd.to_numeric(df['size'], errors='coerce')

    initial_count = len(df)

    df = df[df['price'] > 0]
    df.dropna(subset=['price', 'size'], inplace=True)
    
    dropped_count = initial_count - len(df)
    if dropped_count > 0:
        print(f"⚠️ Cleaned data: Removed {dropped_count} bad rows (zeros/errors).")

    df.set_index('ts', inplace=True)

    for symbol, group in df.groupby('symbol'):
        print(f"\nProcessing {symbol}...")
        
        ohlc = group['price'].resample('1Min').ohlc()
        volume = group['size'].resample('1Min').sum()
        
        final_df = pd.concat([ohlc, volume], axis=1)
        final_df.rename(columns={'size': 'volume'}, inplace=True)
        
        final_df.dropna(inplace=True)
        
        final_df = final_df.round({'open': 2, 'high': 2, 'low': 2, 'close': 2, 'volume': 3})
        
        output_filename = f"{symbol.upper()}_aggregated.csv"
        final_df.to_csv(output_filename)
        
        print(f"--> Saved {output_filename}")
        print(final_df.head()) 

if __name__ == "__main__":
    process_data()