from collections import defaultdict
from flask import Flask, request, send_from_directory

app = Flask(__name__)

class Node:

    children = None
    is_final = False

    def __init__(self):
        self.children = defaultdict(Node)

class Trie:

    root = None
    words = []
    WORD_LIMIT = 2

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

    def __collect_available_words(self, phrase, node):

        if node.is_final:
            self.words.append(phrase)

        if node.children is None or len(self.words) == self.WORD_LIMIT:
            return # break

        for letter in node.children.keys():
            self.__collect_available_words(phrase + letter, node.children[letter])

    def autocomplete(self, phrase):
       self.words = [] # not a huge fan of having a class level variable to manage and reset ... 
       print(f'\n--- Autocomplete suggestions for phrase (${phrase}) ---')
       node = self.__move_to_node(phrase)
       self.__collect_available_words(phrase, node)
       print(self.words)
       print()


root = Trie()

root.insert('apple')
root.insert('apply')
root.insert('about')
root.insert('able')
root.insert('abled')
root.insert('ability')

root.insert('car')
root.insert('call')
root.insert('cartesian')
root.insert('canada')
root.insert('candle')
root.insert('cantaloupe')
root.insert('canopy')

root.autocomplete('ab') # should print able, about, abled, ability ( no limit )
root.autocomplete('can') # should print canada, candle, cantaloupe, canopy ( no limit )


@app.route("/")
def root():
    return f"Welcome to Autocomplete!"

# search?query=ab
@app.route("/search")
def search():
    query = request.args.get('query')
    return f"Query: {query}!"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()