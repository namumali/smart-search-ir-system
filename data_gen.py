"""
Data Generation Script
Creates dummy HTML/text files with Computer Science content for the search engine.
"""

import os
import random

def generate_data_files():
    """
    Generate 10 dummy HTML/text files with Computer Science content.
    Files will be saved in the data/ directory.
    """
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Computer Science topics and content snippets
    topics = [
        {
            "title": "Introduction to Tries",
            "url": "https://cs.example.com/tries",
            "content": [
                "Tries are efficient data structures for string storage and retrieval.",
                "A trie is a tree-like data structure that stores strings character by character.",
                "Tries provide fast prefix matching and autocomplete functionality.",
                "Each node in a trie represents a character in the string.",
                "Tries are commonly used in search engines and spell checkers.",
                "The time complexity for searching in a trie is O(m) where m is the length of the string.",
                "Tries can be more space-efficient than hash tables for certain applications.",
                "Prefix trees enable rapid word lookups and pattern matching in text processing."
            ]
        },
        {
            "title": "B+ Trees in Databases",
            "url": "https://cs.example.com/bplus-trees",
            "content": [
                "B+ Trees are used in databases for indexing and storage.",
                "B+ Trees maintain sorted data and allow efficient insertion and deletion.",
                "Internal nodes in B+ Trees store keys and pointers to child nodes.",
                "Leaf nodes in B+ Trees store actual data records.",
                "B+ Trees are balanced tree structures that minimize disk I/O operations.",
                "Database systems like MySQL and PostgreSQL use B+ Trees for indexing.",
                "B+ Trees provide logarithmic time complexity for search operations.",
                "The structure of B+ Trees makes them ideal for range queries and sequential access."
            ]
        },
        {
            "title": "Graph Algorithms Overview",
            "url": "https://cs.example.com/graph-algorithms",
            "content": [
                "Graph algorithms are fundamental in computer science.",
                "Graphs represent relationships between entities using nodes and edges.",
                "Common graph algorithms include BFS, DFS, and shortest path algorithms.",
                "PageRank is a graph algorithm used to rank web pages by importance.",
                "Graph traversal algorithms help explore all nodes in a graph.",
                "Weighted graphs assign values to edges representing distances or costs.",
                "Graph algorithms are used in social networks, routing, and recommendation systems.",
                "Network analysis relies heavily on graph theory and algorithmic techniques."
            ]
        },
        {
            "title": "Merge Sort Algorithm",
            "url": "https://cs.example.com/merge-sort",
            "content": [
                "Merge Sort is a divide and conquer sorting algorithm.",
                "Merge Sort has a time complexity of O(n log n) in all cases.",
                "The algorithm divides the array into halves recursively.",
                "Merge Sort is stable, meaning it preserves the relative order of equal elements.",
                "The merge step combines two sorted subarrays into one sorted array.",
                "Merge Sort requires additional space for the merging process.",
                "Merge Sort is efficient for large datasets and external sorting.",
                "The recursive nature of merge sort makes it predictable and reliable."
            ]
        },
        {
            "title": "Search Engine Architecture",
            "url": "https://cs.example.com/search-engines",
            "content": [
                "Search engines use inverted indexes to map terms to documents.",
                "Tokenization is the process of breaking text into individual words.",
                "Term frequency measures how often a word appears in a document.",
                "Document ranking combines multiple signals like relevance and authority.",
                "Search engines use various data structures for efficient retrieval.",
                "Crawling and indexing are key components of search engine systems.",
                "Relevance scoring helps determine which documents match a query best.",
                "Modern search engines process billions of queries daily using distributed systems."
            ]
        },
        {
            "title": "Data Structures Fundamentals",
            "url": "https://cs.example.com/data-structures",
            "content": [
                "Data structures organize and store data efficiently.",
                "Arrays provide constant-time access but fixed size.",
                "Linked lists allow dynamic memory allocation.",
                "Trees enable hierarchical data organization.",
                "Hash tables provide fast key-value lookups.",
                "Choosing the right data structure depends on the use case.",
                "Time and space complexity analysis guides data structure selection.",
                "Understanding data structures is essential for writing efficient algorithms."
            ]
        },
        {
            "title": "Information Retrieval Systems",
            "url": "https://cs.example.com/information-retrieval",
            "content": [
                "Information retrieval systems help users find relevant documents.",
                "Boolean retrieval uses AND, OR, and NOT operators.",
                "Vector space models represent documents as vectors.",
                "TF-IDF weighting balances term frequency and inverse document frequency.",
                "Precision and recall measure retrieval system performance.",
                "Query expansion improves search results by adding related terms.",
                "Ranking algorithms determine the order of search results.",
                "Machine learning techniques enhance modern information retrieval systems."
            ]
        },
        {
            "title": "Tree Data Structures",
            "url": "https://cs.example.com/trees",
            "content": [
                "Binary trees have at most two children per node.",
                "Binary search trees maintain sorted order for efficient searching.",
                "AVL trees are self-balancing binary search trees.",
                "Red-black trees provide balanced tree operations.",
                "B-trees are optimized for disk storage and databases.",
                "Tree traversal includes preorder, inorder, and postorder methods.",
                "Tree structures are fundamental in computer science algorithms.",
                "Trees provide efficient hierarchical data organization and search capabilities."
            ]
        },
        {
            "title": "Algorithm Complexity Analysis",
            "url": "https://cs.example.com/complexity",
            "content": [
                "Big O notation describes algorithm time complexity.",
                "Time complexity measures how runtime grows with input size.",
                "Space complexity measures memory usage of algorithms.",
                "Best case, average case, and worst case scenarios differ.",
                "Amortized analysis considers average performance over operations.",
                "Complexity analysis helps compare algorithm efficiency.",
                "Optimization often involves trading time for space or vice versa.",
                "Understanding complexity is crucial for scalable software design."
            ]
        },
        {
            "title": "Database Indexing Techniques",
            "url": "https://cs.example.com/database-indexing",
            "content": [
                "Indexes speed up database query performance.",
                "Primary indexes are built on the primary key of a table.",
                "Secondary indexes are built on non-key attributes.",
                "B+ Trees are commonly used for database indexing.",
                "Hash indexes provide fast equality lookups.",
                "Composite indexes combine multiple columns.",
                "Index maintenance requires balancing query speed and update cost.",
                "Proper indexing strategies significantly improve database performance."
            ]
        }
    ]
    
    # Generate 10 files (mix of HTML and text)
    for i, topic in enumerate(topics, 1):
        # Alternate between HTML and text files
        if i % 2 == 0:
            filename = f"data/doc_{i:02d}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"<!DOCTYPE html>\n<html>\n<head><title>{topic['title']}</title></head>\n<body>\n")
                f.write(f"<h1>{topic['title']}</h1>\n")
                f.write(f"<p>URL: <a href='{topic['url']}'>{topic['url']}</a></p>\n")
                f.write("<div>\n")
                for line in topic['content']:
                    f.write(f"<p>{line}</p>\n")
                f.write("</div>\n</body>\n</html>")
        else:
            filename = f"data/doc_{i:02d}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{topic['title']}\n\n")
                f.write(f"URL: {topic['url']}\n\n")
                for line in topic['content']:
                    f.write(f"{line}\n")
        
        print(f"Generated: {filename}")
    
    print(f"\nSuccessfully generated {len(topics)} files in the data/ directory.")

if __name__ == "__main__":
    generate_data_files()
