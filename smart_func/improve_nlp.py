"""
Additional improvements to NLP scoring based on failure analysis.
"""

# This file contains improvements that will be integrated into nlp.py

IMPROVEMENTS = {
    'exact_name_matching': {
        'description': 'Better exact function name matching',
        'priority': 'HIGH',
        'status': 'implemented'
    },
    'language_detection': {
        'description': 'Detect language from query and filter',
        'priority': 'HIGH',
        'status': 'implemented'
    },
    'synonym_handling': {
        'description': 'Handle synonyms (locate->find, smallest->minimum)',
        'priority': 'HIGH',
        'status': 'implemented'
    },
    'function_name_parts': {
        'description': 'Match function name parts (capitalize + string)',
        'priority': 'HIGH',
        'status': 'implemented'
    }
}

# Additional keyword synonyms to add
SYNONYM_MAPPINGS = {
    'locate': 'find',
    'get': 'find',
    'retrieve': 'find',
    'smallest': 'minimum',
    'lowest': 'minimum',
    'largest': 'maximum',
    'highest': 'maximum',
    'biggest': 'maximum',
    'capital': 'capitalize',
    'title': 'capitalize',
    'first': 'short',
    'take': 'short',
    'limit': 'short',
    'slice': 'short',
}
