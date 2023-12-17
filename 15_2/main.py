from typing import List, Tuple


def read_input() -> str:
    with open("data.txt", "r") as file:
        return file.readline()[:-1]


def hash_func(instruction: str) -> int:
    code = 0
    for c in map(ord, instruction):
        code = ((code + c) * 17) % 256
    return code


def dispatch_lenses(instructions: List[str]) -> List[List[Tuple[str, int]]]:
    buckets = [[] for _ in range(256)]
    for instr in instructions:
        if "-" in instr:
            label = instr[:instr.index("-")]
            h = hash_func(label)
            i = next(iter([i for i, (l, _) in enumerate(buckets[h]) if l == label]), None)
            if i is not None:
                buckets[h].pop(i)
        else: # "=" in instr
            label = instr[:instr.index("=")]
            h = hash_func(label)
            focal_length = int(instr[instr.index("=")+1:])
            i = next(iter([i for i, (l, _) in enumerate(buckets[h]) if l == label]), None)
            if i is not None:
                buckets[h][i] = (buckets[h][i][0], focal_length)
            else:
                buckets[h].append((label, focal_length))
    return buckets


def focussing_power(bucket_id: int, bucket: List[Tuple[str, int]]) -> int:
    power = 0
    for slot_pos, (_, focal_length) in zip(range(1, len(bucket) + 1), bucket):
        power += bucket_id * slot_pos * focal_length
    return power


def main():
    line = read_input()
    instructions = line.split(",")
    buckets = dispatch_lenses(instructions)
    powers = [focussing_power(i+1, b) for i, b in enumerate(buckets)]
    print("focussing power is", sum(powers))


if __name__ == "__main__":
    main()
