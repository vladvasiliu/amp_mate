def response_splitter(response: str, end: str, separator: str) -> (str, str):
    return response.strip(end).split(separator)
