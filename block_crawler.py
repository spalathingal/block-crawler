import argparse
import requests
import sqlite3
import logging
from datetime import datetime

from query import query_block_with_highest_volume

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# retrieves block data through endpoint in specific block range
def retrieve_transactions(endpoint, start_block, end_block):
    # Define JSON-RPC payload
    payload = {
        "method": "eth_getBlockByNumber",
        "params": ["", True],
        "id": 1,
        "jsonrpc": "2.0"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    blocks = []
    # loop through block range
    for block_number in range(start_block, end_block + 1):
        logger.info(f"Fetching transactions for block number: {block_number}")
        
        # update block number in payload
        payload["params"][0] = hex(block_number)
        
        # conduct post request
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching block {block_number}: {e}")
            continue
        
        # check response
        if response.status_code == 200:  # success
            block_data = response.json().get("result")
            if block_data:
                # add data to list
                blocks.append(block_data)
    
    return blocks

# persists transactions to SQLite database
def save_to_database(blocks, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # create table for blocks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            hash TEXT PRIMARY KEY,
            number INTEGER,
            timestamp DATETIME
        )
    """)
    
    # create table for transaction
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            hash TEXT PRIMARY KEY,
            blockHash TEXT,
            blockNumber INTEGER,
            sender TEXT,
            receiver TEXT,
            value REAL,
            FOREIGN KEY (blockHash) REFERENCES blocks(hash)
        )
    """)

    # loop through blocks
    for block in blocks:
        # do conversions from hexadecimal
        hex_number = block['number']
        number = int(hex_number, 16)
        hex_timestamp = block['timestamp']
        timestamp = datetime.utcfromtimestamp(int(hex_timestamp, 16)).strftime("%Y-%m-%d %H:%M:%S")
        
        # prep block data
        block_data = (block['hash'], number, timestamp)
        
        # persist block data
        cursor.execute("INSERT OR IGNORE INTO blocks VALUES (?, ?, ?)", block_data)
        
        # loop through transactions
        for t in block['transactions']:
            # prep transaction data (with conversions)
            t_data = (
                t['hash'],
                t['blockHash'],
                int(t['blockNumber'], 16),
                t['from'],
                t['to'],
                int(t['value'], 16) / 1e18
            )
            
            # persist transaction data
            cursor.execute("INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?)", t_data)
    
    conn.commit()
    conn.close()


# called at command line
def main():
    parser = argparse.ArgumentParser(description="Ethereum Mainnet block crawler")
    parser.add_argument("endpoint")
    parser.add_argument("db_file")
    parser.add_argument("block_range")
    args = parser.parse_args()

    start_block, end_block = map(int, args.block_range.split("-"))

    # get block data from Ethereum Mainnet
    blocks = retrieve_transactions(args.endpoint, start_block, end_block)
    
    # persist to SQLite3 database
    if blocks:
        save_to_database(blocks, args.db_file)
        logger.info(f"Transactions saved to {args.db_file}")
    else:
        logger.warning("No blocks retrieved. Database not updated.")
        
    # query database to find block with largest volume in timeframe
    db_file = "db.sqlite3"
    result = query_block_with_highest_volume(db_file)
    if result:
        # unpack tuple
        block_number, total_volume = result
        logger.info(f"Block Number: {block_number}, Total Volume Transferred: {total_volume}")
    else:
        logger.info("No blocks found within the specified time range.")

if __name__ == "__main__":
    main()
