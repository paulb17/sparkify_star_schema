def camel_to_snake_case(camel_case):
    """
    Function to convert camel case letters to snake case
    """
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel_case]).lstrip('_')
