import re
def clean(value:str):
    value = value.replace("https://","")
    value = value.replace("http://","")
    # value = value.replace("www.","")
    # value = value.rstrip(".")
    value = value.lower
    return value


def clean(value: str) -> str:
    value = value.replace("https://", "")
    value = value.replace("http://", "")
    value = value.replace("www.", "")


    # حذف / های تکراری مثل ////page///test
    value = re.sub(r"/+", "/", value)
    value = value.rstrip(".")
    value = value.rstrip("/")
    return value

print(clean("https://www.example.com////test///"))