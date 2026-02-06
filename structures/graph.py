"""
Graph Data Structure Implementation
Used for modeling document relationships and calculating PageRank scores.
"""


class DocumentGraph:
    """
    Directed graph representing document citations/links.
    Uses adjacency list representation for efficient edge operations.
    """
    
    def __init__(self):
        """Initialize an empty graph with no nodes or edges."""
        self.adjacency_list = {}  # Maps doc_id -> list of doc_ids it links to
        self.incoming_links = {}  # Maps doc_id -> list of doc_ids that link to it
        self.pagerank_scores = {}  # Maps doc_id -> PageRank score
    
    def add_node(self, doc_id):
        """
        Add a node (document) to the graph if it doesn't exist.
        
        Args:
            doc_id: The document identifier.
        """
        if doc_id not in self.adjacency_list:
            self.adjacency_list[doc_id] = []
            self.incoming_links[doc_id] = []
    
    def add_link(self, from_doc, to_doc):
        """
        Create a directed edge from one document to another (citation).
        
        Args:
            from_doc: The source document identifier.
            to_doc: The target document identifier.
        """
        # Ensure both nodes exist
        self.add_node(from_doc)
        self.add_node(to_doc)
        
        # Add the edge (avoid duplicates)
        if to_doc not in self.adjacency_list[from_doc]:
            self.adjacency_list[from_doc].append(to_doc)
            self.incoming_links[to_doc].append(from_doc)
    
    def calculate_pagerank(self, damping_factor=0.85, max_iterations=100, tolerance=1e-6):
        """
        Calculate PageRank scores for all documents using the iterative algorithm.
        PageRank represents the "Authority Score" based on incoming links.
        
        Args:
            damping_factor (float): Probability of following links (default 0.85).
            max_iterations (int): Maximum number of iterations (default 100).
            tolerance (float): Convergence threshold (default 1e-6).
            
        Returns:
            dict: Mapping of doc_id to PageRank score.
        """
        if not self.adjacency_list:
            return {}
        
        num_nodes = len(self.adjacency_list)
        
        # Initialize all nodes with equal PageRank (1/N)
        current_scores = {doc_id: 1.0 / num_nodes for doc_id in self.adjacency_list}
        
        # Iterative PageRank calculation
        for iteration in range(max_iterations):
            new_scores = {}
            
            # Calculate new score for each node
            for doc_id in self.adjacency_list:
                # Base score from random jump
                score = (1 - damping_factor) / num_nodes
                
                # Add contributions from incoming links
                for incoming_doc in self.incoming_links[doc_id]:
                    out_degree = len(self.adjacency_list[incoming_doc])
                    if out_degree > 0:
                        score += damping_factor * current_scores[incoming_doc] / out_degree
                    else:
                        # Handle dangling nodes (nodes with no outgoing links)
                        score += damping_factor * current_scores[incoming_doc] / num_nodes
                
                new_scores[doc_id] = score
            
            # Check for convergence
            max_diff = max(abs(new_scores[doc_id] - current_scores[doc_id]) 
                          for doc_id in self.adjacency_list)
            
            if max_diff < tolerance:
                break
            
            current_scores = new_scores
        
        # Store and return the final scores
        self.pagerank_scores = current_scores
        return self.pagerank_scores
    
    def get_authority_score(self, doc_id):
        """
        Get the PageRank (authority) score for a specific document.
        
        Args:
            doc_id: The document identifier.
            
        Returns:
            float: The PageRank score, or 0.0 if document not found.
        """
        return self.pagerank_scores.get(doc_id, 0.0)
    
    def get_all_scores(self):
        """
        Get all PageRank scores.
        
        Returns:
            dict: Mapping of doc_id to PageRank score.
        """
        return self.pagerank_scores.copy()
