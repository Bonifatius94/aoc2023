from typing import List


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def predict_series(series: List[int]) -> int:
    cache = []
    for a, b in zip(series[:-1], series[1:]):
        cache.append(b - a)
    if all([c == 0 for c in cache]):
        return series[-1]
    else:
        delta = predict_series(cache)
        return series[-1] + delta


def main():
    lines = [l for l in read_lines() if l != ""]
    series = [[int(c.strip()) for c in line.split(" ") if c != ""] for line in lines]
    preds = [predict_series(s) for s in series]
    print("sum of predictions is", sum(preds))


if __name__ == "__main__":
    main()
