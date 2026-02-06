"""
B+ Tree Data Structure Implementation
Used for indexing documents by doc_id with metadata storage.
This is a simplified in-memory implementation.
"""


class LeafNode:
    """
    Leaf node in B+ Tree that stores actual key-value pairs (doc_id -> metadata).
    """
    
    def __init__(self, order):
        """
        Initialize a leaf node.
        
        Args:
            order (int): Maximum number of keys in the node.
        """
        self.order = order
        self.keys = []  # List of doc_ids (sorted)
        self.values = []  # List of metadata dictionaries (corresponding to keys)
        self.next_leaf = None  # Pointer to next leaf node (for range queries)
    
    def is_full(self):
        """Check if the leaf node is full."""
        return len(self.keys) >= self.order
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the leaf node.
        
        Args:
            key: The doc_id to insert.
            value: The metadata dictionary to associate with the key.
            
        Returns:
            tuple: (None, None) if no split needed, or (new_key, new_node) if split occurred.
        """
        # Find the insertion position
        pos = 0
        while pos < len(self.keys) and self.keys[pos] < key:
            pos += 1
        
        # If key already exists, update the value
        if pos < len(self.keys) and self.keys[pos] == key:
            self.values[pos] = value
            return None, None
        
        # Insert the key-value pair
        self.keys.insert(pos, key)
        self.values.insert(pos, value)
        
        # Check if split is needed
        if self.is_full():
            return self._split()
        
        return None, None
    
    def _split(self):
        """
        Split the leaf node when it's full.
        
        Returns:
            tuple: (middle_key, new_right_node)
        """
        mid = len(self.keys) // 2
        new_node = LeafNode(self.order)
        
        # Move the right half to the new node
        new_node.keys = self.keys[mid:]
        new_node.values = self.values[mid:]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        
        # Update next pointers
        new_node.next_leaf = self.next_leaf
        self.next_leaf = new_node
        
        # Return the first key of the new node and the new node itself
        return new_node.keys[0], new_node
    
    def search(self, key):
        """
        Search for a key in the leaf node.
        
        Args:
            key: The doc_id to search for.
            
        Returns:
            dict or None: The metadata dictionary if found, None otherwise.
        """
        try:
            idx = self.keys.index(key)
            return self.values[idx]
        except ValueError:
            return None


class InternalNode:
    """
    Internal node in B+ Tree that stores keys and pointers to child nodes.
    """
    
    def __init__(self, order):
        """
        Initialize an internal node.
        
        Args:
            order (int): Maximum number of keys in the node.
        """
        self.order = order
        self.keys = []  # List of keys (sorted)
        self.children = []  # List of child nodes (one more than keys)
    
    def is_full(self):
        """Check if the internal node is full."""
        return len(self.keys) >= self.order
    
    def find_child_index(self, key):
        """
        Find the index of the child node that should contain the given key.
        
        Args:
            key: The key to search for.
            
        Returns:
            int: Index of the child node.
        """
        idx = 0
        while idx < len(self.keys) and self.keys[idx] <= key:
            idx += 1
        return idx
    
    def insert(self, key, value, child_node=None):
        """
        Insert a key into the internal node or propagate insertion to child.
        
        Args:
            key: The key to insert.
            value: The value (only used for leaf nodes).
            child_node: The new child node created from a split (if any).
            
        Returns:
            tuple: (None, None) if no split needed, or (new_key, new_node) if split occurred.
        """
        if child_node is None:
            # This is a leaf insertion, find the appropriate child
            idx = self.find_child_index(key)
            result = self.children[idx].insert(key, value)
            
            if result[0] is not None:
                # Child was split, need to insert the new key and child
                new_key, new_child = result
                self.keys.insert(idx, new_key)
                self.children.insert(idx + 1, new_child)
                
                # Check if this node needs to split
                if self.is_full():
                    return self._split()
            
            return None, None
        else:
            # This is a split propagation from a child
            idx = self.find_child_index(key)
            self.keys.insert(idx, key)
            self.children.insert(idx + 1, child_node)
            
            if self.is_full():
                return self._split()
            
            return None, None
    
    def _split(self):
        """
        Split the internal node when it's full.
        
        Returns:
            tuple: (middle_key, new_right_node)
        """
        mid = len(self.keys) // 2
        new_node = InternalNode(self.order)
        
        # Move the right half to the new node
        new_node.keys = self.keys[mid + 1:]
        new_node.children = self.children[mid + 1:]
        
        # The middle key goes up to the parent
        middle_key = self.keys[mid]
        
        # Keep the left half in this node
        self.keys = self.keys[:mid]
        self.children = self.children[:mid + 1]
        
        return middle_key, new_node
    
    def search(self, key):
        """
        Search for a key by traversing to the appropriate child.
        
        Args:
            key: The doc_id to search for.
            
        Returns:
            dict or None: The metadata dictionary if found, None otherwise.
        """
        idx = self.find_child_index(key)
        return self.children[idx].search(key)


class BPlusTree:
    """
    Simplified in-memory B+ Tree implementation for document indexing.
    Stores doc_id as key and metadata dictionary as value.
    """
    
    def __init__(self, order=4):
        """
        Initialize the B+ Tree.
        
        Args:
            order (int): Maximum number of keys per node. Default is 4.
        """
        self.order = order
        self.root = LeafNode(order)  # Start with a leaf node as root
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the B+ Tree.
        
        Args:
            key: The doc_id to insert.
            value (dict): The metadata dictionary containing title, file_path, etc.
        """
        result = self.root.insert(key, value)
        
        if result[0] is not None:
            # Root was split, create a new root
            new_key, new_node = result
            new_root = InternalNode(self.order)
            new_root.keys = [new_key]
            new_root.children = [self.root, new_node]
            self.root = new_root
    
    def search(self, key):
        """
        Search for a key in the B+ Tree.
        
        Args:
            key: The doc_id to search for.
            
        Returns:
            dict or None: The metadata dictionary if found, None otherwise.
        """
        return self.root.search(key)
