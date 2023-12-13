from typing import List, Tuple


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def lines_of_section(all_lines: List[str], section_name: str) -> List[str]:
    start = [i for i, l in enumerate(all_lines) if section_name in l][0] + 1
    if any(map(lambda l: l == "", all_lines[start:])):
        end = [i for i, l in enumerate(all_lines[start:]) if l == ""][0] + start
    else:
        end = len(all_lines)
    return all_lines[start:end]


def parse_mappings(lines: List[str]) -> List[Tuple[int, int, int]]:
    return [[int(d.strip()) for d in l.split(" ")] for l in lines]


def map_range(
        range_to_map: Tuple[int, int],
        mappings: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:

    source_lowers = [(i, s_low) for i, (_, s_low, _) in enumerate(mappings)]
    source_lowers = sorted(source_lowers, key=lambda x: x[1])

    res = []
    lower_bound, length = range_to_map

    while length > 0:
        mapping = next(iter([(d, s, l) for d, s, l in mappings
                             if s <= lower_bound < s + l]), None)
        if mapping:
            d_low, s_low, m_len = mapping
            offset = lower_bound - s_low
            upper_bound = min(lower_bound + length, s_low + m_len)
            delta_len = upper_bound - lower_bound
            res.append((d_low + offset, delta_len))
            length -= delta_len
            lower_bound += delta_len
        else:
            next_map_id = next(iter([i for i, s_low in source_lowers
                                     if s_low >= lower_bound]), None)
            if next_map_id is not None:
                d_low, s_low, m_len = mappings[next_map_id]
                delta_len = min(length, s_low - lower_bound)
                res.append((lower_bound, delta_len))
                length -= delta_len
                lower_bound += delta_len
            else:
                res.append((lower_bound, length))
                length = 0

    if sum([l for _, l in res]) != range_to_map[1]:
        print(range_to_map, res)

    return res


def maps_to(
        ranges: List[Tuple[int, int]],
        mappings: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    print("new mapping")
    return [res for r in ranges for res in map_range(r, mappings)]


def main():
    lines = read_lines()
    seed_ids = [int(d.strip()) for d in lines[0][7:].split(" ")]
    seed_ranges = list(zip(seed_ids[::2], seed_ids[1::2]))
    seed_to_soil = parse_mappings(lines_of_section(lines, "seed-to-soil"))
    soil_to_fertilizer = parse_mappings(lines_of_section(lines, "soil-to-fertilizer"))
    fertilizer_to_water = parse_mappings(lines_of_section(lines, "fertilizer-to-water"))
    water_to_light = parse_mappings(lines_of_section(lines, "water-to-light"))
    light_to_temperature = parse_mappings(lines_of_section(lines, "light-to-temperature"))
    temperature_to_humidity = parse_mappings(lines_of_section(lines, "temperature-to-humidity"))
    humidity_to_location = parse_mappings(lines_of_section(lines, "humidity-to-location"))

    soils = maps_to(seed_ranges, seed_to_soil)
    fertilizers = maps_to(soils, soil_to_fertilizer)
    waters = maps_to(fertilizers, fertilizer_to_water)
    lights = maps_to(waters, water_to_light)
    temperatures = maps_to(lights, light_to_temperature)
    humidities = maps_to(temperatures, temperature_to_humidity)
    locations = maps_to(humidities, humidity_to_location)

    loc_starts = [l for l, _ in locations]
    print("closest location is", min(loc_starts))


if __name__ == "__main__":
    main()
