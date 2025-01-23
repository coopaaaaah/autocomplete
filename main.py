from collections import defaultdict
from flask import Flask, request, send_from_directory
import requests

app = Flask(__name__)

class Node:

    children = None
    is_final = False

    def __init__(self):
        self.children = defaultdict(Node)

class Trie:

    root = None
    WORD_LIMIT = 10

    def __init__(self):
        self.root = Node()
    
    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children[char]  # Automatically creates new node if needed
        node.is_final = True

    def __move_to_node(self, phrase) -> Node:
        node = self.root
        for char in phrase:
            node = node.children[char]  # Automatically creates new node if needed
        return node

    def __collect_available_words(self, phrase, node, words):

        if len(words) >= self.WORD_LIMIT:
            return

        if node.is_final:
            words.append(phrase)

        if node.children is None:
            return # break

        for letter in node.children.keys():
            self.__collect_available_words(phrase + letter, node.children[letter], words)

    def autocomplete(self, phrase):
       words = [] # not a huge fan of having a class level variable to manage and reset ... 
       print(f'\n--- Autocomplete suggestions for phrase ({phrase}) ---')
       node = self.__move_to_node(phrase)
       self.__collect_available_words(phrase, node, words)
       print(words)
       print()
       return words


root = Trie()
mit_words = requests.get('https://www.mit.edu/~ecprice/wordlist.10000')
for word in list(mit_words.text.split()):
    root.insert(word)

# root.autocomplete('ab') # should print able, about, abled, ability ( no limit )
# root.autocomplete('can') # should print canada, candle, cantaloupe, canopy ( no limit )


@app.route("/")
def home():
    return f"Welcome to Autocomplete!"

# search?query=ab
@app.route("/search")
def search():
    query = request.args.get('query')
    words = root.autocomplete(query) 
    return f"Query: {query}\n Suggestions: {words}"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()