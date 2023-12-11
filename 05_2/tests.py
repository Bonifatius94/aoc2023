from main import map_range


def test_can_map_range():
    mappings = [
        (120, -5, 10), # -5-5 map to 120-130
        (60, 20, 10),  # 20-30 map to 60-70
        (20, 35, 10),  # 35-45 map to 20-30
        (100, 48, 10), # 48-58 map to 100-110
    ]
    range_to_map = (0, 50)
    ranges = map_range(range_to_map, mappings)

    assert ranges == [(125, 5), (5, 15), (60, 10), (30, 5), (20, 10), (45, 3), (100, 2)]


if __name__ == "__main__":
    test_can_map_range()
