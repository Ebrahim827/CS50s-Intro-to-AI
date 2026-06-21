import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #defined variables
    N = len(corpus)
    probabilities = {}
    
    # Base probability for all pages
    base = (1 - damping_factor) / N
    
    # If page has no links will be treated as linking to all pages
    if len(corpus[page]) == 0:
        for p in corpus:
            probabilities[p] = 1 / N
        return probabilities
    
    # Given every page base probability
    for p in corpus:
        probabilities[p] = base
    
    # Added extra probability for linked pages
    extra = damping_factor / len(corpus[page])
    for linked_page in corpus[page]:
        probabilities[linked_page] += extra
    
    return probabilities

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize counts for all pages
    counts = {page: 0 for page in corpus}
    
    # Start on random page
    current = random.choice(list(corpus.keys()))
    counts[current] += 1
    
    # Generate n-1 more samples
    for _ in range(n - 1):
        # Get probability distribution for next page
        model = transition_model(corpus, current, damping_factor)
        
        # Choose next page based on probabilities
        pages = list(model.keys())
        weights = list(model.values())
        current = random.choices(pages, weights=weights)[0]
        counts[current] += 1
    
    # Convert counts to proportions
    pagerank = {page: counts[page] / n for page in counts}
    
    return pagerank
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    
    # Start with equal ranks
    pagerank = {page: 1 / N for page in corpus}
    
    # Handle pages with no links
    # Treat them as linking to all pages
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())
    
    # Keep iterating until convergence
    while True:
        new_pagerank = {}
        
        for page in corpus:
            # (1-d)/N part
            rank = (1 - damping_factor) / N
            
            # d * sum(PR(i)/NumLinks(i)) part
            for other_page in corpus:
                if page in corpus[other_page]:
                    rank += damping_factor * (pagerank[other_page] / len(corpus[other_page]))
            
            new_pagerank[page] = rank
        
        # Check if converged
        converged = True
        for page in pagerank:
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False
                break
        
        pagerank = new_pagerank
        
        if converged:
            break
    
    return pagerank
    raise NotImplementedError


if __name__ == "__main__":
    main()
