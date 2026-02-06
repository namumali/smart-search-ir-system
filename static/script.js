/**
 * Frontend JavaScript for Live Autocomplete and Search
 */

// DOM Elements
const searchInput = document.getElementById('search-input');
const searchForm = document.getElementById('search-form');
const autocompleteDropdown = document.getElementById('autocomplete-dropdown');
const resultsSection = document.getElementById('results-section');
const resultsContainer = document.getElementById('results-container');
const emptyState = document.getElementById('empty-state');

// State
let selectedIndex = -1;
let currentSuggestions = [];
let autocompleteTimeout = null;

// Event Listeners
searchInput.addEventListener('keyup', handleInput);
searchInput.addEventListener('keydown', handleKeyDown);
searchForm.addEventListener('submit', handleSearch);
searchInput.addEventListener('focus', handleFocus);
document.addEventListener('click', handleDocumentClick);

/**
 * Handle input changes for live autocomplete
 */
function handleInput(event) {
    const query = searchInput.value.trim();
    
    // Clear previous timeout
    if (autocompleteTimeout) {
        clearTimeout(autocompleteTimeout);
    }
    
    // Hide dropdown if input is empty
    if (query.length === 0) {
        hideAutocomplete();
        return;
    }
    
    // Debounce autocomplete requests (wait 200ms after user stops typing)
    autocompleteTimeout = setTimeout(() => {
        fetchAutocomplete(query);
    }, 200);
}

/**
 * Handle keyboard navigation in autocomplete dropdown
 */
function handleKeyDown(event) {
    if (!autocompleteDropdown.classList.contains('show')) {
        return;
    }
    
    switch(event.key) {
        case 'ArrowDown':
            event.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, currentSuggestions.length - 1);
            updateAutocompleteSelection();
            break;
        case 'ArrowUp':
            event.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateAutocompleteSelection();
            break;
        case 'Enter':
            if (selectedIndex >= 0 && currentSuggestions[selectedIndex]) {
                event.preventDefault();
                searchInput.value = currentSuggestions[selectedIndex];
                hideAutocomplete();
                performSearch(currentSuggestions[selectedIndex]);
            }
            break;
        case 'Escape':
            hideAutocomplete();
            break;
    }
}

/**
 * Handle search form submission
 */
function handleSearch(event) {
    event.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
        hideAutocomplete();
        performSearch(query);
    }
}

/**
 * Handle input focus - show autocomplete if there's text
 */
function handleFocus() {
    const query = searchInput.value.trim();
    if (query.length > 0) {
        fetchAutocomplete(query);
    }
}

/**
 * Handle clicks outside the search container
 */
function handleDocumentClick(event) {
    if (!event.target.closest('.search-container')) {
        hideAutocomplete();
    }
}

/**
 * Fetch autocomplete suggestions from the backend
 */
async function fetchAutocomplete(prefix) {
    try {
        const response = await fetch('/autocomplete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prefix: prefix })
        });
        
        if (!response.ok) {
            throw new Error('Autocomplete request failed');
        }
        
        const suggestions = await response.json();
        currentSuggestions = suggestions;
        selectedIndex = -1;
        displayAutocomplete(suggestions, prefix);
        
    } catch (error) {
        console.error('Error fetching autocomplete:', error);
        hideAutocomplete();
    }
}

/**
 * Display autocomplete suggestions in the dropdown
 */
function displayAutocomplete(suggestions, prefix) {
    if (suggestions.length === 0) {
        hideAutocomplete();
        return;
    }
    
    autocompleteDropdown.innerHTML = '';
    
    suggestions.forEach((suggestion, index) => {
        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.dataset.index = index;
        
        // Highlight the prefix in the suggestion
        const highlighted = highlightPrefix(suggestion, prefix);
        item.innerHTML = highlighted;
        
        // Add click handler
        item.addEventListener('click', () => {
            searchInput.value = suggestion;
            hideAutocomplete();
            performSearch(suggestion);
        });
        
        // Add hover handler
        item.addEventListener('mouseenter', () => {
            selectedIndex = index;
            updateAutocompleteSelection();
        });
        
        autocompleteDropdown.appendChild(item);
    });
    
    autocompleteDropdown.classList.add('show');
}

/**
 * Highlight the prefix in a suggestion
 */
function highlightPrefix(suggestion, prefix) {
    const lowerSuggestion = suggestion.toLowerCase();
    const lowerPrefix = prefix.toLowerCase();
    const prefixIndex = lowerSuggestion.indexOf(lowerPrefix);
    
    if (prefixIndex === -1) {
        return suggestion;
    }
    
    const before = suggestion.substring(0, prefixIndex);
    const match = suggestion.substring(prefixIndex, prefixIndex + prefix.length);
    const after = suggestion.substring(prefixIndex + prefix.length);
    
    return `${before}<span class="highlight">${match}</span>${after}`;
}

/**
 * Update visual selection in autocomplete dropdown
 */
function updateAutocompleteSelection() {
    const items = autocompleteDropdown.querySelectorAll('.autocomplete-item');
    items.forEach((item, index) => {
        if (index === selectedIndex) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

/**
 * Hide autocomplete dropdown
 */
function hideAutocomplete() {
    autocompleteDropdown.classList.remove('show');
    autocompleteDropdown.innerHTML = '';
    selectedIndex = -1;
    currentSuggestions = [];
}

/**
 * Perform search and display results
 */
async function performSearch(query) {
    // Show loading state
    resultsContainer.innerHTML = '<div class="loading">Searching...</div>';
    resultsSection.style.display = 'block';
    emptyState.classList.add('hidden');
    
    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Search request failed');
        }
        
        const data = await response.json();
        displayResults(data.results, query);
        
    } catch (error) {
        console.error('Error performing search:', error);
        resultsContainer.innerHTML = '<div class="loading">Error performing search. Please try again.</div>';
    }
}

/**
 * Display search results
 */
function displayResults(results, query) {
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="loading">
                <p>No results found for "${query}"</p>
                <p style="margin-top: 10px; font-size: 14px; color: #70757a;">
                    Try different keywords or check your spelling.
                </p>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = '';
    
    results.forEach(result => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        
        resultItem.innerHTML = `
            <div class="result-url">
                <a href="${result.url}" target="_blank">${result.url}</a>
            </div>
            <div class="result-title">
                <a href="${result.url}" target="_blank">${result.title}</a>
            </div>
            <div class="result-snippet">${escapeHtml(result.snippet)}</div>
            <div class="result-score">Relevance Score: ${result.score}</div>
        `;
        
        resultsContainer.appendChild(resultItem);
    });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
