import sqlite3


def query_block_with_highest_volume(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # SQL query
    query = """
        SELECT 
            transactions.blockNumber AS block_number,
            SUM(transactions.value) AS total_volume_transferred
        FROM 
            transactions
        JOIN 
            blocks ON transactions.blockHash = blocks.hash
        WHERE 
            blocks.timestamp BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:30:00'
        GROUP BY 
            transactions.blockNumber
        ORDER BY 
            total_volume_transferred DESC
        LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return result