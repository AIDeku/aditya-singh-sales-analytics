
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"
    
    try:
        response = requests.get(url, timeout=10) # 10s timeout is good practice
        response.raise_for_status() # Raise API errors
        
        data = response.json()
        products = data.get('products', [])
        
        print(f"Successfully fetched {len(products)} products from API.")
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    
    Parameters: api_products from fetch_all_products()
    
    Returns: dictionary mapping product IDs to info
    Format: { id: { 'title': ..., 'category': ..., 'brand': ..., 'rating': ... }, ... }
    """
    mapping = {}
    
    for p in api_products:
        p_id = p.get('id')
        if p_id is not None:
            mapping[p_id] = {
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'rating': p.get('rating')
            }
            
    return mapping
