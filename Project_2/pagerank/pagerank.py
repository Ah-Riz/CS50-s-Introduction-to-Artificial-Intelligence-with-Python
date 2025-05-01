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
    prob_distr = dict()
    num_links = len(corpus[page])
    num_pages = len(corpus)
    prob = (1 - damping_factor) / num_pages
    if num_links == 0:
        for p in corpus:
            prob_distr[p] = prob
    else:
        for p in corpus:
            if p in corpus[page]:
                prob_distr[p] = (damping_factor / num_links) + prob
            else:
                prob_distr[p] = prob
    print("prob", prob)
    print("prob_distr", prob_distr)
    return prob_distr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    get_random = ""
    sample = dict()
    sample = {page: 0 for page in corpus}

    for sample_num in range(n):
        # Choose a random page to start
        if sample_num == 0:
            get_random = random.choice(list(corpus.keys()))
        else:
            prob_distr = transition_model(corpus, get_random, damping_factor)
            val_prob_distr = list(prob_distr.values())

            get_random = random.choices(tuple(sample), weights=val_prob_distr)[0]
            sample[get_random] = sample.get(get_random, 0) + 1
    for p in sample:
        sample[p] = sample.get(p) / n
    return sample

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    
    # Initialize PageRank values
    page_rank = {page: 1/num_pages for page in corpus}
    
    # Create a modified corpus where pages with no links link to all pages
    modified_corpus = corpus.copy()
    for page in corpus:
        if not corpus[page]:
            modified_corpus[page] = set(corpus.keys())

    while True:
        new_rank = dict()
        
        for page in corpus:
            # Calculate random surfer probability
            random_surfer = (1 - damping_factor) / num_pages
            
            # Calculate sum of incoming PageRanks
            sum_pr = 0
            for linking_page in corpus:
                # Check if the current page is linked to by linking_page
                if page in modified_corpus[linking_page]:
                    sum_pr += page_rank[linking_page] / len(modified_corpus[linking_page])
            
            # Update PageRank value
            new_rank[page] = random_surfer + damping_factor * sum_pr
            
        # Check for convergence
        all_page = []
        for page in new_rank:
            all_page.append(abs(new_rank[page] - page_rank[page]) < 0.001)
        if all(all_page):
            return new_rank
            
        page_rank = new_rank.copy()

if __name__ == "__main__":
    main()
