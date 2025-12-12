def direct_cache_mapping_interactive():
    try:
        cache_size_str = input("Enter cache size (number of lines): ").strip()
        if not cache_size_str:
            print("No cache size entered. Exiting.")
            return
        cache_size = int(cache_size_str)
        if cache_size <= 0:
            print("Cache size must be positive.")
            return

        n_str = input("Enter number of memory references: ").strip()
        if not n_str:
            print("No number of references entered. Exiting.")
            return
        n = int(n_str)
        if n <= 0:
            print("Number of references must be positive.")
            return

        print("Enter memory block references (space-separated):")
        refs_line = input().strip()
        if not refs_line:
            print("No references entered. Exiting.")
            return

        references = list(map(int, refs_line.split()))
        if len(references) < n:
            print(f"Warning: you asked for {n} references but provided only {len(references)}. Will process provided references.")
        elif len(references) > n:
            print(f"Note: you provided {len(references)} references but asked for {n}. Will process all provided references.")

        # Use all provided references (safer), or you could use references[:n] to enforce n.
        return direct_cache_mapping(cache_size, references)

    except ValueError as e:
        print("Invalid integer input:", e)
    except EOFError:
        print("No input available (EOF). If running in a non-interactive environment, run the non-interactive example instead.")
    except Exception as e:
        print("Unexpected error:", e)


def direct_cache_mapping(cache_size, references, verbose=True):
    cache = [-1] * cache_size
    hits = 0
    misses = 0

    if verbose:
        print("\n--- Direct Mapped Cache Simulation ---\n")

    if not references:
        if verbose:
            print("No references to process.")
        return hits, misses

    for step, block in enumerate(references, start=1):
        index = block % cache_size
        if cache[index] == block:
            hits += 1
            if verbose:
                print(f"Step {step}: Accessing Block {block}: HIT (index {index})")
        else:
            misses += 1
            if verbose:
                print(f"Step {step}: Accessing Block {block}: MISS (placed at index {index})")
            cache[index] = block

        if verbose:
            print("Cache State:", cache)

    if verbose:
        print("\nSimulation Complete!")
        print(f"Total References: {len(references)}")
        print(f"Total Hits: {hits}")
        print(f"Total Misses: {misses}")
        print(f"Hit Ratio: {hits / len(references):.2f}")
        print(f"Miss Ratio: {misses / len(references):.2f}")

    return hits, misses


if __name__ == "__main__":
    # Run interactive by default. If you want non-interactive testing, comment the next line
    direct_cache_mapping_interactive()

    # --- Non-interactive example usage (uncomment to test) ---
    # Example:
    # cache_size = 4
    # references = [1, 2, 3, 1, 4, 2, 1]
    # direct_cache_mapping(cache_size, references)
