
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day
)
import os

def main():
    print("==========================================")
    print("      Sales Data Analytics System")
    print("==========================================\n")

    # --- Step 1: File Operations ---
    file_path = 'data/sales_data.txt'
    print(f"[INFO] Reading file: {file_path}")
    
    raw_lines = read_sales_data(file_path)
    if not raw_lines:
        print("[ERROR] No data found. Exiting.")
        return

    print(f"[INFO] Read {len(raw_lines)} raw lines.\n")

    # --- Step 2: Data Cleaning & Parsing ---
    print("[INFO] Parsing and Cleaning data...")
    all_transactions = parse_transactions(raw_lines)
    
    # --- Step 3: Validation & Filtering ---
    # We pass None to region/amount to keep all valid data for the general report
    valid_transactions, invalid_count, filter_summary = validate_and_filter(all_transactions)
    
    print(f"\n[INFO] Data Validation Summary:")
    print(f"   - Total Parsed: {filter_summary['total_input']}")
    print(f"   - Invalid Rows: {filter_summary['invalid']}")
    print(f"   - Valid Rows:   {filter_summary['final_count']}")
    
    if not valid_transactions:
        print("[ERROR] No valid transactions to analyze. Exiting.")
        return

    # --- Step 4: Data Analysis ---
    print("\n==========================================")
    print("           ANALYTICS REPORT")
    print("==========================================\n")

    # 4.1 Total Revenue
    revenue = calculate_total_revenue(valid_transactions)
    print(f"1. Total Revenue: ${revenue:,.2f}")

    # 4.2 Region Analysis
    print("\n2. Sales by Region:")
    region_stats = region_wise_sales(valid_transactions)
    for region, stats in region_stats.items():
        print(f"   - {region}: ${stats['total_sales']:,.2f} ({stats['percentage']}%) | {stats['transaction_count']} txns")

    # 4.3 Top Products
    print("\n3. Top 5 Selling Products:")
    top_products = top_selling_products(valid_transactions, n=5)
    for i, (name, qty, rev) in enumerate(top_products, 1):
        print(f"   {i}. {name}: {qty} units sold (${rev:,.2f})")

    # 4.4 Peak Sales Day
    print("\n4. Peak Sales Day:")
    peak_data = find_peak_sales_day(valid_transactions)
    if peak_data:
        date, peak_rev, count = peak_data
        print(f"   - Date: {date}")
        print(f"   - Revenue: ${peak_rev:,.2f}")
        print(f"   - Transactions: {count}")
    else:
        print("   - N/A")

    # 4.5 Customer Insights (Top 3 Spenders)
    print("\n5. Top 3 Customers (by Spend):")
    cust_stats = customer_analysis(valid_transactions)
    top_3_customers = list(cust_stats.items())[:3]
    for c_id, stats in top_3_customers:
        print(f"   - {c_id}: ${stats['total_spent']:,.2f} (Bought {len(stats['products_bought'])} unique items)")

    # --- Step 5: API Enrichment ---
    print("\n[INFO] Fetching real-time product data from API...")
    from utils.api_handler import fetch_all_products, create_product_mapping
    
    api_products = fetch_all_products()
    product_map = create_product_mapping(api_products)
    print(f"[INFO] Created mapping for {len(product_map)} products.")
    
    # Enrich transactions
    print("[INFO] Enriching transactions with API data...")
    enriched_transactions = []
    for t in valid_transactions:
        # Create a copy to enrich
        enriched_t = t.copy()
        
        # Logic to match ProductID to API ID
        # Our data has 'P101', 'P102', etc. API has numeric IDs or strings '1', '2'.
        # Attempt to strip 'P' and match, or match directly.
        # This is a heuristic attempt.
        pid_clean = t['ProductID'].replace('P', '')
        
        # Try finding in map assuming integer keys
        matched_info = None
        try:
            pid_int = int(pid_clean)
            matched_info = product_map.get(pid_int)
        except ValueError:
            matched_info = product_map.get(t['ProductID'])
            
        if matched_info:
            enriched_t.update(matched_info)
            enriched_t['enriched'] = True
        else:
            enriched_t['enriched'] = False
            
        enriched_transactions.append(enriched_t)

    # --- Step 5.5: Save Enriched Data (Checklist Item) ---
    enriched_file = 'output/enriched_sales_data.txt'
    print(f"[INFO] Saving enriched data to {enriched_file}...")
    os.makedirs(os.path.dirname(enriched_file), exist_ok=True)
    with open(enriched_file, 'w', encoding='utf-8') as f:
        # Write Header
        # Base keys + new keys from API
        if enriched_transactions:
            keys = list(enriched_transactions[0].keys())
            f.write('|'.join(keys) + '\n')
            for t in enriched_transactions:
                values = [str(t.get(k, '')) for k in keys]
                f.write('|'.join(values) + '\n')

    # --- Step 6: Report Generation ---
    print("\n[INFO] Generating comprehensive report...")
    from utils.data_processor import generate_sales_report
    output_report_path = 'output/sales_report.txt'
    generate_sales_report(valid_transactions, enriched_transactions, output_report_path)

    print("\n==========================================")
    print("           System Finished")
    print("==========================================")

if __name__ == "__main__":
    main()
