"""
Main User Interface
Simple CLI loop for interacting with the search engine.
"""

from engine import SearchEngine


def print_separator():
    """Print a visual separator line."""
    print("-" * 70)


def print_results(results):
    """
    Print search results in a formatted way.
    
    Args:
        results (list): List of result dictionaries from the search engine.
    """
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} result(s):\n")
    
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result['title']}")
        print(f"    Document ID: {result['doc_id']}")
        print(f"    File: {result['file_path']}")
        print(f"    Relevance Score: {result['score']:.4f}")
        print(f"      - Term Frequency: {result['term_frequency']:.4f}")
        print(f"      - Authority Score: {result['authority_score']:.4f}")
        print()


def print_autocomplete_suggestions(suggestions):
    """
    Print autocomplete suggestions.
    
    Args:
        suggestions (list): List of suggested words.
    """
    if not suggestions:
        print("No suggestions found.")
        return
    
    print(f"\nFound {len(suggestions)} suggestion(s):")
    print(", ".join(suggestions))
    print()


def main():
    """Main CLI loop for the search engine."""
    print("=" * 70)
    print("Smart Search and Information Retrieval System")
    print("=" * 70)
    print("\nInitializing search engine...")
    print_separator()
    
    # Initialize the search engine
    try:
        engine = SearchEngine()
        print_separator()
        print("\nSearch engine ready!")
    except Exception as e:
        print(f"Error initializing search engine: {e}")
        return
    
    # Main menu loop
    while True:
        print("\n" + "=" * 70)
        print("Main Menu")
        print("=" * 70)
        print("[1] Search")
        print("[2] Autocomplete")
        print("[3] Exit")
        print_separator()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Search functionality
            print_separator()
            query = input("Enter search query: ").strip()
            
            if query:
                print(f"\nSearching for: '{query}'...")
                results = engine.search(query)
                print_results(results)
            else:
                print("Please enter a valid query.")
        
        elif choice == "2":
            # Autocomplete functionality
            print_separator()
            prefix = input("Enter prefix: ").strip()
            
            if prefix:
                print(f"\nFinding words starting with: '{prefix}'...")
                suggestions = engine.autocomplete(prefix)
                print_autocomplete_suggestions(suggestions)
            else:
                print("Please enter a valid prefix.")
        
        elif choice == "3":
            # Exit
            print_separator()
            print("Thank you for using the Search Engine. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
