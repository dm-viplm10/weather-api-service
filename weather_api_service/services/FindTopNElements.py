from collections import Counter

def FindTopN(rows, n):
    return Counter(rows).most_common(n)