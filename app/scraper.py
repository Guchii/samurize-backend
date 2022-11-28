import wikipedia

output = []


def getPara(title: str):
    wk = wikipedia.page(title)
    return wk.content
