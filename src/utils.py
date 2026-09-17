def read_file(file_path: str) -> str:
    data: str = ""
    with open(file_path, "r", encoding="utf-8") as fd:
        data = fd.read()
    return data
