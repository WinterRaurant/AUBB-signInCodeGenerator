def split_string_to_dict(input_str):
    result_dict = {}
    pairs = input_str.split('; ')
    for pair in pairs:
        key, value = pair.split('=', 1)
        result_dict[key] = value
    return result_dict