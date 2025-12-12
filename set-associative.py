class CacheSet:
    def __init__(self, ways):
        self.ways = ways
        self.blocks = []
        self.usage = []
        self.freq = {}

    def access_fifo(self, block):
        if block in self.blocks:
            return True

        if len(self.blocks) < self.ways:
            self.blocks.append(block)
        else:
            self.blocks.pop(0)
            self.blocks.append(block)
        return False

    def access_lru(self, block):
        if block in self.blocks:
            self.usage.remove(block)
            self.usage.append(block)
            return True

        if len(self.blocks) < self.ways:
            self.blocks.append(block)
            self.usage.append(block)
        else:
            lru = self.usage.pop(0)
            self.blocks.remove(lru)
            self.blocks.append(block)
            self.usage.append(block)
        return False

    def access_lfu(self, block):
        if block in self.blocks:
            self.freq[block] += 1
            return True

        if len(self.blocks) < self.ways:
            self.blocks.append(block)
            self.freq[block] = 1
        else:
            lfu = min(self.freq, key=self.freq.get)
            self.blocks.remove(lfu)
            self.freq.pop(lfu)
            self.blocks.append(block)
            self.freq[block] = 1
        return False


class SetAssociativeCache:
    def __init__(self, num_sets, ways, policy):
        self.num_sets = num_sets
        self.ways = ways
        self.policy = policy.lower()
        self.sets = [CacheSet(ways) for _ in range(num_sets)]
        self.hits = 0
        self.misses = 0

    def map_block(self, block):
        return block % self.num_sets

    def access(self, block):
        set_index = self.map_block(block)
        target_set = self.sets[set_index]

        if self.policy == "fifo":
            hit = target_set.access_fifo(block)
        elif self.policy == "lru":
            hit = target_set.access_lru(block)
        elif self.policy == "lfu":
            hit = target_set.access_lfu(block)
        else:
            raise ValueError("Invalid policy")

        if hit:
            self.hits += 1
            print(f"Block {block} → HIT")
        else:
            self.misses += 1
            print(f"Block {block} → MISS")

        self.display_cache()

    def display_cache(self):
        print("Cache:")
        for i, s in enumerate(self.sets):
            print(f" Set {i}: {s.blocks}")
        print()

    def summary(self):
        print("\n=== FINAL SUMMARY ===")
        print("Hits:", self.hits)
        print("Misses:", self.misses)
        total = self.hits + self.misses
        print("Hit Ratio:", round(self.hits/total, 2))
        print("=====================")


# --------------------------
# USER INPUT SECTION
# --------------------------

num_sets = int(input("Enter number of sets: "))
ways = int(input("Enter number of ways (lines per set): "))
policy = input("Enter replacement policy (FIFO / LRU / LFU): ")

cache = SetAssociativeCache(num_sets, ways, policy)

# input sequence of references
ref_input = input("Enter memory block sequence (space separated): ")
references = list(map(int, ref_input.split()))

print("\n=== STARTING SIMULATION ===\n")

for block in references:
    cache.access(block)

cache.summary()
