import re

def selector_formatting(text: str, options: dict = {}) -> str:

    if options.get('selector') == 'xpath':
        return text
    
    contains = options.get('contains', False)
    pattern = r'^(id|title|class|name|tag|placeholder|value)=(.*)'
    match = re.match(pattern, text)
    if match:
        selector = f'@{match.group(1)}'
        value = match.group(2)
    else:
        selector = 'text()'
        value = text
    
    if contains:
        return f'//*[contains({selector}, "{value}")]'
    else:
        return f'//*[{selector}="{value}"]'