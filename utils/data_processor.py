
import os
from datetime import datetime

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    
    Returns: float (total revenue)
    """
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    
    Returns: dictionary with region statistics
    Format: {
        'North': {'total_sales': float, 'transaction_count': int, 'percentage': float},
        ...
    }
    """
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    if total_revenue == 0:
        return {}

    # Aggregate data
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
            
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
        
    # Calculate percentage and format
    final_stats = {}
    for region, stats in region_stats.items():
        percentage = (stats['total_sales'] / total_revenue) * 100
        stats['percentage'] = round(percentage, 2)
        stats['total_sales'] = round(stats['total_sales'], 2) # rounding for cleanliness
        final_stats[region] = stats
        
    # Sort by total_sales descending
    # Dictionary insertion order is preserved in modern Python (3.7+)
    sorted_stats = dict(sorted(final_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    
    return sorted_stats

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    
    Returns: list of tuples
    Format: [('ProductName', TotalQuantity, TotalRevenue), ...]
    """
    product_stats = {}
    
    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if p_name not in product_stats:
            product_stats[p_name] = {'quantity': 0, 'revenue': 0.0}
            
        product_stats[p_name]['quantity'] += qty
        product_stats[p_name]['revenue'] += revenue
        
    # Convert to list of tuples
    product_list = [
        (name, data['quantity'], data['revenue']) 
        for name, data in product_stats.items()
    ]
    
    # Sort by TotalQuantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    
    Returns: dictionary of customer statistics
    Format: {
        'C001': {
            'total_spent': float, 
            'purchase_count': int, 
            'avg_order_value': float, 
            'products_bought': list
        }, ...
    }
    """
    customer_stats = {}
    
    for t in transactions:
        c_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        p_name = t['ProductName']
        
        if c_id not in customer_stats:
            customer_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_set': set() # using set for unique products
            }
            
        customer_stats[c_id]['total_spent'] += amount
        customer_stats[c_id]['purchase_count'] += 1
        customer_stats[c_id]['products_set'].add(p_name)
        
    # Calculate avg and finalize structure
    final_stats = {}
    for c_id, stats in customer_stats.items():
        avg_value = stats['total_spent'] / stats['purchase_count'] if stats['purchase_count'] > 0 else 0
        
        final_stats[c_id] = {
            'total_spent': round(stats['total_spent'], 2),
            'purchase_count': stats['purchase_count'],
            'avg_order_value': round(avg_value, 2),
            'products_bought': list(stats['products_set']) # convert set back to list
        }
        
    # Sort by total_spent descending
    sorted_stats = dict(sorted(final_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))
    
    return sorted_stats

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Returns: dictionary sorted by date
    Format: {
        '2024-12-01': {
            'revenue': float,
            'transaction_count': int,
            'unique_customers': int
        }, ...
    }
    """
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        c_id = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0, 
                'transaction_count': 0, 
                'customers_set': set()
            }
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers_set'].add(c_id)
        
    # Finalize stats
    final_stats = {}
    for date, stats in daily_stats.items():
        final_stats[date] = {
            'revenue': round(stats['revenue'], 2),
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers_set'])
        }
        
    # Sort by Date ascending
    sorted_stats = dict(sorted(final_stats.items(), key=lambda item: item[0]))
    
    return sorted_stats

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_stats = daily_sales_trend(transactions)
    
    if not daily_stats:
        return None
        
    # Find max by revenue
    # daily_stats items are (date, stats_dict)
    peak_day = max(daily_stats.items(), key=lambda item: item[1]['revenue'])
    
    date = peak_day[0]
    revenue = peak_day[1]['revenue']
    count = peak_day[1]['transaction_count']
    
    return (date, revenue, count)

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("==========================================\n")
        f.write("          SALES ANALYTICS REPORT\n")
        f.write(f"          Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"          Records Processed: {len(transactions)}\n")
        f.write("==========================================\n\n")
        
        # 2. OVERALL SUMMARY
        total_revenue = calculate_total_revenue(transactions)
        total_transactions = len(transactions)
        avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
        
        dates = [t['Date'] for t in transactions]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
        
        f.write("OVERALL SUMMARY\n")
        f.write("------------------------------------------\n")
        f.write(f"Total Revenue:       ${total_revenue:,.2f}\n")
        f.write(f"Total Transactions:  {total_transactions}\n")
        f.write(f"Average Order Value: ${avg_order_value:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")
        
        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("------------------------------------------\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Transactions':<15}\n")
        region_stats = region_wise_sales(transactions)
        for region, stats in region_stats.items():
            f.write(f"{region:<15} ${stats['total_sales']:<14,.2f} {stats['percentage']:<14}% {stats['transaction_count']:<15}\n")
        f.write("\n")
        
        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Product Name':<30} {'Quantity':<10} {'Revenue':<15}\n")
        top_products = top_selling_products(transactions, n=5)
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<5} {name:<30} {qty:<10} ${rev:<15,.2f}\n")
        f.write("\n")
        
        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<20} {'Order Count':<10}\n")
        cust_stats = customer_analysis(transactions)
        top_customers = list(cust_stats.items())[:5]
        for i, (c_id, stats) in enumerate(top_customers, 1):
            f.write(f"{i:<5} {c_id:<15} ${stats['total_spent']:<19,.2f} {stats['purchase_count']:<10}\n")
        f.write("\n")
        
        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("------------------------------------------\n")
        f.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<20}\n")
        daily_stats = daily_sales_trend(transactions)
        for date, stats in daily_stats.items():
            f.write(f"{date:<15} ${stats['revenue']:<19,.2f} {stats['transaction_count']:<14} {stats['unique_customers']:<20}\n")
        f.write("\n")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("------------------------------------------\n")
        
        # Best selling day
        peak = find_peak_sales_day(transactions)
        best_day_str = f"{peak[0]} (${peak[1]:,.2f} with {peak[2]} txns)" if peak else "N/A"
        f.write(f"Best Selling Day: {best_day_str}\n")
        
        # Low performing products (bottom 3)
        # Using logic similar to top_selling but taking bottom
        product_sales = {}
        for t in transactions:
            pid = t['ProductName']
            product_sales[pid] = product_sales.get(pid, 0) + t['Quantity']
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1])
        low_performers = sorted_products[:3]
        f.write("Low Performing Products (Bottom 3 by Qty):\n")
        for name, qty in low_performers:
            f.write(f"  - {name}: {qty} units\n")
            
        # Avg transaction value per region
        f.write("Avg Transaction Value per Region:\n")
        for region, stats in region_stats.items():
            avg_val = stats['total_sales'] / stats['transaction_count'] if stats['transaction_count'] else 0
            f.write(f"  - {region}: ${avg_val:,.2f}\n")
        f.write("\n")
        
        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("------------------------------------------\n")
        
        total_enriched = sum(1 for t in enriched_transactions if t.get('enriched', False))
        success_rate = (total_enriched / len(transactions)) * 100 if transactions else 0
        
        f.write(f"Total Products Enriched: {total_enriched}\n")
        f.write(f"Success Rate:            {success_rate:.2f}%\n")
        f.write("Unenriched Products (Sample IDs):\n")
        
        unenriched_ids = set()
        for t in enriched_transactions:
            if not t.get('enriched', False):
                unenriched_ids.add(t['ProductID'])
        
        for pid in list(unenriched_ids)[:10]: # Limit sample to 10
            f.write(f"  - {pid}\n")
        
        if len(unenriched_ids) > 10:
            f.write(f"  ... (+{len(unenriched_ids)-10} more)\n")
            
    print(f"Report successfully generated at: {output_file}")
