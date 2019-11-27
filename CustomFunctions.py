import re, glob, os

def CombineResults(result):
    replace = r'(^([a-zA-Z][a-zA-Z][a-zA-Z]){1}[a-zA-Z]*$)|(^[a-zA-Z]{3,}$)'
    found = []
    for i in result['regions']:
        for j in i['lines']:
            for k in j['words']:
                if not re.match(replace, k['text']):
                    found.append(k['text'])
    return ''.join(found)

def ClearImages():
    test = 'ImagesTaken/*'
    r = glob.glob(test)
    for i in r:
        os.remove(i)