"""Aggregate mock read results through the same validated dispatcher."""
import json
from main import dispatch

def stock_and_quote(sku, quantity):
    calls = [('stock', 'catalog.lookup_stock', {'sku': sku}),
             ('quote', 'catalog.quote_price', {'sku': sku, 'quantity': quantity})]
    results = {key: dispatch({'call_id': key, 'name': name,
                            'arguments': json.dumps(args)}) for key, name, args in calls}
    failures = {key: result['error'] for key, result in results.items() if not result['ok']}
    if failures:
        return {'ok': False, 'errors': failures, 'reservation_made': False}
    return {'ok': True, 'sku': sku, 'quantity': quantity,
            'available_at_lookup': results['stock']['data']['available'] >= quantity,
            'total_cents': results['quote']['data']['total_cents'],
            'reservation_made': False}

if __name__ == '__main__':
    assert stock_and_quote('lamp', 2)['total_cents'] == 5000
    assert stock_and_quote('lamp', 5)['available_at_lookup'] is False
    assert stock_and_quote('missing', 2)['errors'] == {'stock': 'not_found', 'quote': 'not_found'}
    assert stock_and_quote('lamp', True)['errors'] == {'quote': 'invalid_arguments'}
    print(json.dumps(stock_and_quote('lamp', 2), indent=2))
