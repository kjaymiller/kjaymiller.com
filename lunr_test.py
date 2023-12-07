import json
from lunr import lunr

with open('output/corpus.json') as f:
    data = json.load(f)

idx = lunr(ref='url', fields=['title', 'content'], documents=data)

print(idx.serialize())