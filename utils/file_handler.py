
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    
    Returns: list of raw lines (strings)
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                lines = f.readlines()
                
            # Filter out empty lines and strip whitespace
            # Requirement says "Remove empty lines"
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            
            # Skip header row (assuming first row is always header if file is valid)
            if cleaned_lines:
                return cleaned_lines[1:]
            return []
            
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return []
            
    print(f"Error: Could not decode file '{filename}' with any of the attempted encodings.")
    return []

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName', 
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """
    transactions = []
    
    for line in raw_lines:
        fields = line.split('|')
        
        # Requirement: Skip rows with incorrect number of fields
        # Expected fields: 8
        if len(fields) != 8:
            continue
            
        # Unpack fields for clarity
        t_id, date, p_id, p_name, qty_str, price_str, c_id, region = fields
        
        # Clean fields
        # Requirement: Handle commas within ProductName (remove or replace)
        clean_p_name = p_name.replace(',', ' ')
        
        try:
            # Requirement: Remove commas from numeric fields and convert
            clean_qty = int(qty_str.replace(',', ''))
            clean_price = float(price_str.replace(',', ''))
        except ValueError:
            # Skip if number conversion fails (implicit in "clean data" requirement, 
            # or could capture as invalid, but usually parsing function just produces what it can)
            # The assignment doesn't explicitly say to skip invalid numbers here, 
            # but usually type conversion failure implies skipping or error.
            # I will skip this row if conversion fails to ensure "clean list of dictionaries"
            continue

        transaction = {
            'TransactionID': t_id.strip(),
            'Date': date.strip(),
            'ProductID': p_id.strip(),
            'ProductName': clean_p_name.strip(),
            'Quantity': clean_qty,
            'UnitPrice': clean_price,
            'CustomerID': c_id.strip(),
            'Region': region.strip()
        }
        
        transactions.append(transaction)
        
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    valid_transactions = []
    invalid_count = 0
    
    # 1. Validation
    temp_valid_transactions = []
    for t in transactions:
        is_valid = True
        
        # Rule: Quantity > 0
        if t['Quantity'] <= 0:
            is_valid = False
            
        # Rule: UnitPrice > 0
        if t['UnitPrice'] <= 0:
            is_valid = False
            
        # Rule: All required fields must be present
        # Checking for empty strings as "present" implies having a value
        required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 'CustomerID', 'Region']
        for field in required_fields:
            if not t[field]: # Empty string check
                is_valid = False
                break
                
        # Rule: IDs must start with correct letters
        if not t['TransactionID'].startswith('T'):
            is_valid = False
        if not t['ProductID'].startswith('P'):
            is_valid = False
        if not t['CustomerID'].startswith('C'):
            is_valid = False
            
        if is_valid:
            temp_valid_transactions.append(t)
        else:
            invalid_count += 1
            
    # 2. Display Info (as per requirements)
    # "Print available regions to user before filtering"
    available_regions = sorted(list(set(t['Region'] for t in temp_valid_transactions if t['Region'])))
    print(f"Available Regions: {available_regions}")
    
    # "Print transaction amount range (min/max) to user"
    amounts = [t['Quantity'] * t['UnitPrice'] for t in temp_valid_transactions]
    if amounts:
        print(f"Transaction Amount Range: Min={min(amounts)}, Max={max(amounts)}")
    else:
        print("Transaction Amount Range: N/A (no valid transactions)")

    # 3. Filtering
    filtered_transactions = []
    
    # Track counts for summary
    filtered_by_region_count = 0
    filtered_by_amount_count = 0 
    
    # Note: Logic for "filtered_by_X_count" is slightly ambiguous.
    # Is it "how many were removed by this filter" or "how many passed this filter"?
    # The example output shows:
    # 'filtered_by_region': 20
    # 'filtered_by_amount': 10
    # 'final_count': 65
    # This suggests it might be the count of items MATCHING the filter, or REMOVED.
    # Let's assume it means "count of transactions remaining AFTER this filter step" or "count of transactions excluded".
    # But usually summary stats like "filtered_by_region: 20" implies 20 items were *filtered out* or *kept*.
    # Looking at the numbers: Total input 100, Invalid 5. Valid candidates = 95.
    # Final count 65.
    # If 20 were filtered by region and 10 by amount, 95 - 20 - 10 = 65.
    # So it likely means "Number of records REMOVED by this filter".
    
    initial_valid_count = len(temp_valid_transactions)
    current_transactions = temp_valid_transactions
    
    # Filter by Region
    if region:
        next_transactions = [t for t in current_transactions if t['Region'] == region]
        filtered_by_region_count = len(current_transactions) - len(next_transactions)
        current_transactions = next_transactions
        print(f"Records after region filter: {len(current_transactions)}")
    
    # Filter by Amount
    # min_amount and max_amount check "Quantity * UnitPrice"
    if min_amount is not None or max_amount is not None:
        next_transactions = []
        for t in current_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            passed = True
            if min_amount is not None and amount < min_amount:
                passed = False
            if max_amount is not None and amount > max_amount:
                passed = False
            
            if passed:
                next_transactions.append(t)
                
        filtered_by_amount_count = len(current_transactions) - len(next_transactions)
        current_transactions = next_transactions
        print(f"Records after amount filter: {len(current_transactions)}")
        
    filtered_transactions = current_transactions
    
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region_count,
        'filtered_by_amount': filtered_by_amount_count,
        'final_count': len(filtered_transactions)
    }
    
    return filtered_transactions, invalid_count, filter_summary
