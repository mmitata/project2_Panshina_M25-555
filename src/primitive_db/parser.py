def parse_command(phrase):
    if phrase is None:
        return None
    key, value = phrase.split(' = ')
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return {key: int(value)}
    if value.lower() == "true":
        return {key: True}
    if value.lower() == "false":
        return {key: False}
    return {key: value}
