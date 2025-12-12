class CacheLine:
    def __init__(self, block):
        self.block = block
        self.time = 0


class AssociativeCache:
    def __init__(self, size):
        self.size = size
        self.cache = []
        self.timer = 0

    def access(self, block):
        self.timer += 1

        for line in self.cache:
            if line.block == block:
                line.time = self.timer
                print(f"HIT → {block}")
                return

        print(f"MISS → {block}")

        if len(self.cache) < self.size:
            new_line = CacheLine(block)
            new_line.time = self.timer
            self.cache.append(new_line)
            return

        self.replace(block)

    def replace(self, block):
        print("Cache FULL → applying LRU replacement")
        lru_line = min(self.cache, key=lambda x: x.time)
        self.cache.remove(lru_line)
        new_line = CacheLine(block)
        new_line.time = self.timer
        self.cache.append(new_line)

    def display(self):
        print("\nCurrent Cache State:")
        for line in self.cache:
            print(f"[Block={line.block}, time={line.time}]")
        print("")


size = int(input("Enter cache size: "))
cache = AssociativeCache(size)

sequence = list(map(int, input("Enter block access sequence (space separated): ").split()))

for blk in sequence:
    cache.access(blk)
    cache.display()
