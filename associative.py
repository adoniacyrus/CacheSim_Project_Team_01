class CacheLine:
    def __init__(self):
        self.block = None
        self.valid = False
        self.time = 0


class AssociativeCacheLRU:
    def __init__(self, size):
        self.size = size
        self.cache = [CacheLine() for _ in range(size)]
        self.timer = 0

    def access(self, block):
        self.timer += 1

        for line in self.cache:
            if line.valid and line.block == block:
                line.time = self.timer
                print(f"Block {block} → HIT")
                return

        print(f"Block {block} → MISS")

        for line in self.cache:
            if not line.valid:
                line.block = block
                line.valid = True
                line.time = self.timer
                return

        lru_line = min(self.cache, key=lambda x: x.time)
        replaced = lru_line.block
        lru_line.block = block
        lru_line.time = self.timer
        print(f"Replaced block {replaced} (LRU)")

    def display(self):
        print("Cache State:")
        for i, line in enumerate(self.cache):
            if line.valid:
                print(f" Line {i}: Block {line.block}")
            else:
                print(f" Line {i}: EMPTY")
        print("-" * 30)


def main():
    try:
        size = int(input("Enter cache size: "))
        sequence = list(map(int, input("Enter block access sequence: ").split()))
    except:
        print("Invalid input")
        return

    cache = AssociativeCacheLRU(size)

    for block in sequence:
        cache.access(block)
        cache.display()


if __name__ == "__main__":
    main()
