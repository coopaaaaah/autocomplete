# autocomplete

I had a question to myself about how autocomplete works on google and how many nodes would exist for an average word base. 

#### Cursory research:
- Average length of word is 5 characters long (depth of trie / word bank)

#### Early thoughts:
This will be a simple UI that provides a list of available words (from a-z).
The math on this is tricky to think about.

We'll use a `Trie` data structure. So an array of 26 nodes that each can point to 26 more nodes as we progress through the word.

#### flow
```
[nothing entered]
[a, b, c, d, ...]
[a entered]
a - [a, b, c, d, ...]
shows [able, abled, apple, apply, ...]
[b entered]
ab - [a, b, c, d, ...]
shows [able, abled, about, ability, ...]
[l entered]
abl - [a, b, c, d, ...]
shows [able, abled, ...]
[e entered]
able - [a, b, c, d, ...]
shows [able, abled, ...]
[d entered]
abled - [a, b, c, d, ...]
shows [abled, (probably nothing left)]
```


#### Additional thoughts / next steps
- Setup fastapi /GET /search?query=ab (debounce 100ms) to get list of words to show as suggestions
- Napkin math how much words I could keep in memory (manage backend list and just offload to FE on load for faster searching in memory, no longer making client requests)