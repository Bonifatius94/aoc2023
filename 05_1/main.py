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


def maps_to(key: int, mappings: List[Tuple[int, int, int]]) -> int:
    mapped = [d + key - s for d, s, l in mappings if s <= key < s + l]
    return min(mapped) if mapped else key


def main():
    lines = read_lines()
    seed_ids = [int(d.strip()) for d in lines_of_section(lines, "seeds")[0].split(" ")]
    seed_to_soil = parse_mappings(lines_of_section(lines, "seed-to-soil"))
    soil_to_fertilizer = parse_mappings(lines_of_section(lines, "soil-to-fertilizer"))
    fertilizer_to_water = parse_mappings(lines_of_section(lines, "fertilizer-to-water"))
    water_to_light = parse_mappings(lines_of_section(lines, "water-to-light"))
    light_to_temperature = parse_mappings(lines_of_section(lines, "light-to-temperature"))
    temperature_to_humidity = parse_mappings(lines_of_section(lines, "temperature-to-humidity"))
    humidity_to_location = parse_mappings(lines_of_section(lines, "humidity-to-location"))

    def find_location(seed: int) -> int:
        soil = maps_to(seed, seed_to_soil)
        fertilizer = maps_to(soil, soil_to_fertilizer)
        water = maps_to(fertilizer, fertilizer_to_water)
        light = maps_to(water, water_to_light)
        temperature = maps_to(light, light_to_temperature)
        humidity = maps_to(temperature, temperature_to_humidity)
        location = maps_to(humidity, humidity_to_location)
        # print(seed, soil, fertilizer, water, light, temperature, humidity, location)
        return location

    locations = [find_location(s) for s in seed_ids]
    # print(locations)
    print("closest location is", min(locations))


if __name__ == "__main__":
    main()
