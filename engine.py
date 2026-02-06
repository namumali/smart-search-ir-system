"""
Search Engine Implementation
Main logic for indexing documents, processing queries, and ranking results.
"""

import os
import re
import random
from collections import defaultdict
from structures.trie import Trie
from structures.b_plus_tree import BPlusTree
from structures.graph import DocumentGraph
from utils.sorter import sort_results


class SearchEngine:
    """
    Main search engine class that integrates all data structures.
    Handles document indexing, query processing, and result ranking.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize the search engine.
        
        Args:
            data_dir (str): Directory containing text files to index.
        """
        self.data_dir = data_dir
        self.trie = Trie()
        self.b_plus_tree = BPlusTree()
        self.graph = DocumentGraph()
        self.inverted_index = defaultdict(set)  # Maps word -> set of doc_ids
        self.doc_term_frequency = defaultdict(dict)  # Maps doc_id -> {word: frequency}
        self.doc_ids = []
        
        # Load and index documents
        self._load_documents()
        self._generate_citations()
        self._calculate_authority_scores()
    
    def _tokenize(self, text):
        """
        Tokenize text into words (lowercase, alphanumeric only).
        
        Args:
            text (str): The text to tokenize.
            
        Returns:
            list: List of tokenized words.
        """
        # Convert to lowercase and extract words (alphanumeric)
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return words
    
    def _extract_text_from_html(self, html_content):
        """
        Extract plain text from HTML content by removing tags.
        
        Args:
            html_content (str): HTML content.
            
        Returns:
            str: Plain text extracted from HTML.
        """
        import re
        # Remove script and style elements
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Decode HTML entities (basic)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        return text
    
    def _extract_snippet(self, content, query_term, max_length=150):
        """
        Extract a snippet from content containing the query term.
        
        Args:
            content (str): The full content.
            query_term (str): The search term to highlight.
            max_length (int): Maximum length of snippet.
            
        Returns:
            str: A snippet of text containing the query term.
        """
        content_lower = content.lower()
        term_lower = query_term.lower()
        
        # Find the first occurrence of the term
        idx = content_lower.find(term_lower)
        
        if idx == -1:
            # Term not found, return beginning of content
            return content[:max_length] + "..." if len(content) > max_length else content
        
        # Extract snippet around the term
        start = max(0, idx - 50)
        end = min(len(content), idx + max_length - 50)
        
        snippet = content[start:end]
        
        # Ensure snippet doesn't break words
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet.strip()
    
    def _load_documents(self):
        """
        Load all text and HTML files from the data directory and index them.
        """
        if not os.path.exists(self.data_dir):
            print(f"Warning: Data directory '{self.data_dir}' not found.")
            return
        
        # Get all text and HTML files in the data directory
        files = sorted([f for f in os.listdir(self.data_dir) 
                       if f.endswith('.txt') or f.endswith('.html')])
        
        if not files:
            print(f"Warning: No text/HTML files found in '{self.data_dir}' directory.")
            return
        
        print(f"Loading {len(files)} documents...")
        
        for filename in files:
            file_path = os.path.join(self.data_dir, filename)
            doc_id = len(self.doc_ids) + 1  # Start doc_id from 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract plain text (handle HTML files)
                if filename.endswith('.html'):
                    plain_text = self._extract_text_from_html(content)
                else:
                    plain_text = content
                
                # Extract title and URL
                lines = plain_text.split('\n')
                title = lines[0].strip() if lines else filename
                
                # Try to extract URL (look for "URL: " pattern)
                url = file_path  # Default to file path
                for line in lines[:5]:  # Check first few lines
                    if 'url:' in line.lower():
                        url = line.split(':', 1)[1].strip()
                        break
                
                # If no URL found, create a virtual URL
                if url == file_path:
                    url = f"https://cs.example.com/{filename.replace('.txt', '').replace('.html', '')}"
                
                # Tokenize the content
                words = self._tokenize(plain_text)
                
                # Calculate term frequencies for this document
                term_freq = defaultdict(int)
                for word in words:
                    term_freq[word] += 1
                    self.inverted_index[word].add(doc_id)
                
                # Store term frequencies
                self.doc_term_frequency[doc_id] = dict(term_freq)
                
                # Insert words into Trie
                for word in set(words):  # Insert unique words only
                    self.trie.insert(word)
                
                # Index document in B+ Tree
                metadata = {
                    'title': title,
                    'file_path': file_path,
                    'url': url,
                    'word_count': len(words),
                    'content': plain_text  # Store content for snippet generation
                }
                self.b_plus_tree.insert(doc_id, metadata)
                
                self.doc_ids.append(doc_id)
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        print(f"Successfully indexed {len(self.doc_ids)} documents.")
    
    def _generate_citations(self):
        """
        Randomly generate citations between documents to populate the graph.
        Each document randomly cites 2-4 other documents.
        """
        if len(self.doc_ids) < 2:
            return
        
        print("Generating document citations...")
        
        for from_doc in self.doc_ids:
            # Each document cites 2-4 other documents
            num_citations = random.randint(2, min(4, len(self.doc_ids) - 1))
            
            # Randomly select documents to cite (excluding self)
            possible_targets = [d for d in self.doc_ids if d != from_doc]
            cited_docs = random.sample(possible_targets, min(num_citations, len(possible_targets)))
            
            for to_doc in cited_docs:
                self.graph.add_link(from_doc, to_doc)
        
        print(f"Generated citations between documents.")
    
    def _calculate_authority_scores(self):
        """
        Calculate PageRank scores for all documents.
        """
        print("Calculating PageRank authority scores...")
        self.graph.calculate_pagerank()
        print("Authority scores calculated.")
    
    def _calculate_term_frequency(self, doc_id, term):
        """
        Calculate term frequency for a term in a document.
        
        Args:
            doc_id: The document identifier.
            term (str): The search term.
            
        Returns:
            float: Term frequency (normalized by document length).
        """
        if doc_id not in self.doc_term_frequency:
            return 0.0
        
        term_freq_dict = self.doc_term_frequency[doc_id]
        term_count = term_freq_dict.get(term.lower(), 0)
        doc_length = sum(term_freq_dict.values())
        
        # Normalize by document length
        if doc_length > 0:
            return term_count / doc_length
        return 0.0
    
    def search(self, query):
        """
        Search for documents containing the query term.
        Results are ranked by: Term Frequency + Authority Score.
        
        Args:
            query (str): The search query (single term).
            
        Returns:
            list: Sorted list of result dictionaries, each containing:
                - doc_id: Document identifier
                - title: Document title
                - file_path: Path to the document
                - score: Calculated relevance score
                - term_frequency: TF component of the score
                - authority_score: PageRank component of the score
        """
        if not query or not query.strip():
            return []
        
        # Tokenize query (take first word if multiple words)
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        
        # Use the first term for search
        search_term = query_terms[0].lower()
        
        # Find documents containing the term using inverted index
        matching_docs = self.inverted_index.get(search_term, set())
        
        if not matching_docs:
            return []
        
        # Calculate scores for each matching document
        results = []
        for doc_id in matching_docs:
            # Get metadata from B+ Tree
            metadata = self.b_plus_tree.search(doc_id)
            if not metadata:
                continue
            
            # Calculate term frequency
            tf = self._calculate_term_frequency(doc_id, search_term)
            
            # Get authority score from graph
            authority = self.graph.get_authority_score(doc_id)
            
            # Combined score: TF + Authority
            score = tf + authority
            
            # Generate snippet
            content = metadata.get('content', '')
            snippet = self._extract_snippet(content, search_term)
            
            results.append({
                'doc_id': doc_id,
                'title': metadata['title'],
                'url': metadata.get('url', metadata.get('file_path', '')),
                'snippet': snippet,
                'score': score,
                'term_frequency': tf,
                'authority_score': authority
            })
        
        # Sort results using merge sort
        sorted_results = sort_results(results)
        
        return sorted_results
    
    def autocomplete(self, prefix):
        """
        Get autocomplete suggestions for a given prefix.
        
        Args:
            prefix (str): The prefix to search for.
            
        Returns:
            list: List of words starting with the prefix (max 5).
        """
        if not prefix or not prefix.strip():
            return []
        
        return self.trie.autocomplete(prefix.strip(), limit=5)
    
    def get_suggestions(self, prefix):
        """
        Wrapper method for autocomplete (for Flask API compatibility).
        
        Args:
            prefix (str): The prefix to search for.
            
        Returns:
            list: List of word suggestions (max 5).
        """
        return self.autocomplete(prefix)
