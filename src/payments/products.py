from django.conf import settings

TEST_PRODUCT_CHECKOUT_CONFIG = {
    'payment_method_types': ['card'],
    'line_items': [
        {
            'price': '<YOUR_TEST_PRICE>',
            'quantity': 1,
        },
    ],
    'mode': 'payment',
}

TEST_SUBSCRIPTION_CHECKOUT_CONFIG = {
    'payment_method_types': ['card'],
    'line_items': [
        {
            'price': '<YOUR_TEST_PRICE>',
            'quantity': 1,
        },
    ],
    'mode': 'subscription',
}

if settings.DEBUG:
    # Development
    PRICE_CHECKOUT_MAPPING = {
        'boilerplate_rapidsaas': TEST_PRODUCT_CHECKOUT_CONFIG,
        'euro_grille_subscription': TEST_SUBSCRIPTION_CHECKOUT_CONFIG,
    }
else:
    # Production
    PRICE_CHECKOUT_MAPPING = {}
