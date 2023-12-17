
def read_input() -> str:
    with open("data.txt", "r") as file:
        return file.readline()[:-1]


def hash(instruction: str) -> int:
    code = 0
    for c in map(ord, instruction):
        code = ((code + c) * 17) % 256
    return code


def main():
    line = read_input()
    instructions = line.split(",")
    instr_hashes = [hash(instr) for instr in instructions]
    print("sum of hashes is", sum(instr_hashes))


if __name__ == "__main__":
    main()
