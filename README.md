# Relayer Technical Challenge

## Overview
Here is my approach to the Relayer Block-Crawler challenge submitted March 2024.


## Task
Write a Python program that retrieves Ethereum Mainnet transactions within a given block range (18908800 to 18909050) and persists them to a database. Then to write a python script that queries this database and returns the largest volume of ether transferred between 2024-01-01 00:00:00 and 2024-01-01 00:30:00.

The program should take 3 command line inputs:
1. A JSON-RPC endpoint to call an Ethereum client (e.g.
https://rpc.quicknode.pro/key)
2. The path of the SQLite file to write to (e.g. db.sqlite3)
3. A block range, formatted as "{start}-{end}", (e.g. 200-300)


## Dependencies
- Install [Python3](https://www.python.org/downloads/) if you don't already have it
- Install [pipenv](https://pipenv.pypa.io/en/latest/) using pip/homebrew/apt
- Run `pipenv install` to install dependencies

## To Run
- Start shell environment: `pipenv shell`
- Run block crawler:
```
python block_crawler.py {URL HERE} \
{database name} \
{start block}-{end block}
```

What I ran:
```
python block_crawler.py https://icy-attentive-daylight.quiknode.pro/{KEY}/ db.sqlite3 18908800-18909050
```

## Approach
My approach was to follow the guidelines listed in the problem statement, which was to create 3 functions (split into two files), one for retrieving the Ethereum Mainnet transactions, another for formatting and persisting the data into the SQLite database, and the last for querying the populated database for blocks that had the largest volume in the given range.

## Metrics
- This took me about 5 hours to complete
- Results can be seen in results.txt

## Conclusion
- Was a neat assignment, my first exposure to crawling through the blockchain (API is quick to set up!).
- Conversions of table values from hexadecimal caused me a decent amount of trouble that I had to debug.
- I might have separated these functions into separate files in hindsight for modularity and organization.
- If I had a much larger input range, I would likely need to persist to the database with each QuickNode api call as opposed to storing all transactions in-memory in a list.
- Overall a fun task, felt like I learned a lot more about how the blockchain operates!