
cache_size = int(input("Enter cache size: "))
reference = list(map(int, input("Enter reference string (space separated): ").split()))

cache = []
queue = []
hits = 0
misses = 0

print("\nCache status:")

for block in reference:
    if block in cache:
        hits += 1
        print(f"{block} → HIT  | Cache: {cache}")
    else:
        misses += 1
        if len(cache) == cache_size:
            oldest = queue.pop(0)
            cache.remove(oldest)
        cache.append(block)
        queue.append(block)
        print(f"{block} → MISS | Cache: {cache}")

print("\nFinal Result")
print("Hits:", hits)
print("Misses:", misses)
print("Hit Ratio:", hits / len(reference))
