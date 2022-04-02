import orjson

class json:
    def dumps(data) -> str:
        return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode('utf-8')
    
    def loads(data):
        return orjson.loads(data)

    def dump(file: str, data):
        with open(file, mode='wb') as in_file:
            in_file.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
            in_file.close()

    def load(file: str):
        with open(file, mode='r') as in_file:
            data = in_file.read()
            in_file.close()
        return orjson.loads(data)
