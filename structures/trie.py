"""
Trie Data Structure Implementation
Used for autocomplete functionality in the search engine.
"""


class TrieNode:
    """
    Represents a single node in the Trie data structure.
    Each node stores children nodes and a flag indicating if it's the end of a word.
    """
    
    def __init__(self):
        """Initialize a Trie node with empty children dictionary and end_of_word flag."""
        self.children = {}  # Dictionary mapping characters to child TrieNodes
        self.is_end_of_word = False  # True if this node represents the end of a word


class Trie:
    """
    Trie (Prefix Tree) implementation for efficient string storage and prefix matching.
    Supports insertion and autocomplete operations.
    """
    
    def __init__(self):
        """Initialize an empty Trie with a root node."""
        self.root = TrieNode()
    
    def insert(self, word):
        """
        Insert a word into the trie.
        
        Args:
            word (str): The word to insert into the trie.
        """
        node = self.root
        
        # Traverse the trie, creating nodes as needed
        for char in word.lower():  # Convert to lowercase for case-insensitive matching
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # Mark the end of the word
        node.is_end_of_word = True
    
    def _search_prefix(self, prefix):
        """
        Helper method to find the node corresponding to a prefix.
        
        Args:
            prefix (str): The prefix to search for.
            
        Returns:
            TrieNode or None: The node at the end of the prefix, or None if prefix doesn't exist.
        """
        node = self.root
        
        for char in prefix.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def _collect_words(self, node, prefix, words):
        """
        Recursively collect all words starting from a given node.
        
        Args:
            node (TrieNode): The current node to start collecting from.
            prefix (str): The prefix accumulated so far.
            words (list): List to store collected words.
        """
        # If current node marks the end of a word, add it to the list
        if node.is_end_of_word:
            words.append(prefix)
        
        # Recursively traverse all children
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)
    
    def autocomplete(self, prefix, limit=5):
        """
        Return a list of top N words in the trie that start with the given prefix.
        
        Args:
            prefix (str): The prefix to search for.
            limit (int): Maximum number of suggestions to return (default: 5).
            
        Returns:
            list: A list of up to 'limit' words starting with the prefix. Empty list if no matches found.
        """
        # Find the node corresponding to the prefix
        node = self._search_prefix(prefix)
        
        if node is None:
            return []
        
        # Collect all words starting from this node
        words = []
        self._collect_words(node, prefix.lower(), words)
        
        # Return top N suggestions (sorted alphabetically for consistency)
        words.sort()
        return words[:limit]
