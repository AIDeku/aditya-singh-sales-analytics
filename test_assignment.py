
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
import os

def test_assignment_part1():
    print("=== Testing Assignment 3 Part 1 ===")
    
    # 1. Test Read
    filename = 'data/sales_data.txt'
    # Ensure raw strings for path compatibility if needed, but forward slash works in python on windows usually.
    # Using absolute path logic or relative to cwd.
    
    print(f"\n1. Testing read_sales_data('{filename}')...")
    raw_lines = read_sales_data(filename)
    print(f"Read {len(raw_lines)} lines.")
    assert len(raw_lines) > 0, "Failed to read any lines"
    # Basic check on first line
    print(f"First line sample: {raw_lines[0]}")
    
    # 2. Test Parse
    print(f"\n2. Testing parse_transactions...")
    transactions = parse_transactions(raw_lines)
    print(f"Parsed {len(transactions)} transactions.")
    
    if transactions:
        t1 = transactions[0]
        print(f"Sample transaction: {t1}")
        assert isinstance(t1['Quantity'], int), "Quantity should be int"
        assert isinstance(t1['UnitPrice'], float), "UnitPrice should be float"
        
        # Check for comma removal in Product Name if applicable
        # The sample data has "Mouse,Wireless" -> "Mouse Wireless"
        for t in transactions:
            if "," in t['ProductName']:
                print(f"WARNING: Comma found in ProductName: {t['ProductName']}")
                
    # 3. Test Validation and Filtering
    print(f"\n3. Testing validate_and_filter...")
    
    # Test 3a: No filters
    valid, invalid, summary = validate_and_filter(transactions)
    print(f"No Filter Summary: {summary}")
    
    # Test 3b: Filter by Region 'North'
    print("\nApplying Region='North'...")
    valid_north, invalid_north, summary_north = validate_and_filter(transactions, region='North')
    print(f"North Filter Summary: {summary_north}")
    for t in valid_north:
        assert t['Region'] == 'North', "Region filter failed"
        
    # Test 3c: Filter by Min Amount 5000
    print("\nApplying MinAmount=5000...")
    valid_high, invalid_high, summary_high = validate_and_filter(transactions, min_amount=5000)
    print(f"High Value Summary: {summary_high}")
    for t in valid_high:
        assert t['Quantity'] * t['UnitPrice'] >= 5000, "Min amount filter failed"

    # === PART 2 TESTS ===
    from utils.data_processor import (
        calculate_total_revenue, 
        region_wise_sales, 
        top_selling_products, 
        customer_analysis, 
        daily_sales_trend
    )

    print("\n--- Part 2: Data Processing Tests ---")
    
    # Use valid transactions for analysis (assuming we want to analyze valid data only)
    # The assignment doesn't explicitly say "filter first", but analysis usually runs on clean data.
    # We'll use the 'valid' list from Test 3a.
    analysis_data = valid 
    
    # 4. Test Total Revenue
    print("\n4. Testing calculate_total_revenue...")
    total_revenue = calculate_total_revenue(analysis_data)
    print(f"Total Revenue: {total_revenue}")
    assert total_revenue > 0, "Total revenue should be positive"
    
    # 5. Test Region Wise Sales
    print("\n5. Testing region_wise_sales...")
    region_stats = region_wise_sales(analysis_data)
    print(f"Regions found: {list(region_stats.keys())}")
    if region_stats:
        first_region = list(region_stats.keys())[0]
        print(f"Top Region Stats ({first_region}): {region_stats[first_region]}")
        # Verify sorting (descending revenue)
        revenues = [d['total_sales'] for d in region_stats.values()]
        assert revenues == sorted(revenues, reverse=True), "Region stats not sorted by sales"

    # 6. Test Top Selling Products
    print("\n6. Testing top_selling_products...")
    top_products = top_selling_products(analysis_data, n=3)
    print(f"Top 3 Products: {top_products}")
    assert len(top_products) <= 3, "Should return at most n products"
    # Verify sorting (descending quantity) - second element in tuple
    quantities = [p[1] for p in top_products]
    assert quantities == sorted(quantities, reverse=True), "Top products not sorted by quantity"

    # 7. Test Customer Analysis
    print("\n7. Testing customer_analysis...")
    cust_stats = customer_analysis(analysis_data)
    print(f"Analyzed {len(cust_stats)} customers.")
    if cust_stats:
        top_customer = list(cust_stats.keys())[0]
        print(f"Top Customer ({top_customer}): {cust_stats[top_customer]}")
        # Verify sorting (descending spend)
        spends = [d['total_spent'] for d in cust_stats.values()]
        assert spends == sorted(spends, reverse=True), "Customer stats not sorted by spend"
        
    # 8. Test Daily Trend
    print("\n8. Testing daily_sales_trend...")
    daily_stats = daily_sales_trend(analysis_data)
    print(f"Days analyzed: {len(daily_stats)}")
    dates = list(daily_stats.keys())
    # Verify sorting (ascending date)
    assert dates == sorted(dates), "Daily stats not sorted by date"
    if dates:
        print(f"Stats for {dates[0]}: {daily_stats[dates[0]]}")

    # 9. Test Peak Sales Day
    from utils.data_processor import find_peak_sales_day
    print("\n9. Testing find_peak_sales_day...")
    peak_day = find_peak_sales_day(analysis_data)
    print(f"Peak Sales Day: {peak_day}")
    if peak_day:
        assert isinstance(peak_day, tuple), "Should return a tuple"
        assert len(peak_day) == 3, "Tuple should have 3 elements"
        # Logic check: Verify it is indeed the max
        max_rev = 0
        for d, stats in daily_stats.items():
            if stats['revenue'] > max_rev:
                max_rev = stats['revenue']
        assert peak_day[1] == max_rev, "Returned revenue matches calculated max"

        assert peak_day[1] == max_rev, "Returned revenue matches calculated max"

    # === PART 3 TESTS ===
    from utils.api_handler import fetch_all_products, create_product_mapping
    print("\n--- Part 3: API Integration Tests ---")
    
    # 10. Test Fetch Products
    print("\n10. Testing fetch_all_products...")
    api_products = fetch_all_products()
    print(f"Fetched {len(api_products)} products.")
    
    if api_products:
        print(f"Sample API Product: {api_products[0]}")
        assert 'id' in api_products[0], "Product should have ID"
        assert 'title' in api_products[0], "Product should have title"
        
        # 11. Test Product Mapping
        print("\n11. Testing create_product_mapping...")
        product_map = create_product_mapping(api_products)
        print(f"Mapped {len(product_map)} products.")
        
        first_id = list(product_map.keys())[0]
        mapped_item = product_map[first_id]
        print(f"Mapped Item ID {first_id}: {mapped_item}")
        
        assert 'title' in mapped_item, "Mapped item should have title"
        assert 'rating' in mapped_item, "Mapped item should have rating"
    else:
        print("WARNING: API fetch returned empty. Check internet connection or API status.")
        # We don't fail the test here because network issues can happen, 
        # allowing the script to pass "conceptually" is verified by the try-except block design.

    # === PART 4 TESTS ===
    from utils.data_processor import generate_sales_report
    import os
    print("\n--- Part 4: Report Generation Tests ---")
    
    # 12. Test Report Generation
    print("\n12. Testing generate_sales_report...")
    # Mock enriched data (just valid transactions with a dummy enriched flag)
    mock_enriched = []
    for t in analysis_data:
        x = t.copy()
        x['enriched'] = False # Default to False for test logic
        mock_enriched.append(x)
        
    test_output = 'output/test_report.txt'
    generate_sales_report(analysis_data, mock_enriched, test_output)
    
    if os.path.exists(test_output):
        print(f"Report created at {test_output}")
        with open(test_output, 'r') as f:
            content = f.read()
            assert "SALES ANALYTICS REPORT" in content, "Report header missing"
            assert "OVERALL SUMMARY" in content, "Summary section missing"
            print("Report content verified.")
    else:
        print("Error: Report file was not created.")
        assert False, "Report file missing"

    print("\n=== All Tests Passed (conceptually) ===")

if __name__ == "__main__":
    test_assignment_part1()
