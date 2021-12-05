FILENAME = "day3_data.txt"


def read_data(filename: str) -> list[str]:
    with open(file=filename, mode="r") as read_file:
        return [line.strip() for line in read_file]


def flip(binary: str) -> str:
    return "".join(("0" if bit == "1" else "1") for bit in binary)


def most_common_binary_number(binarys: list[str]) -> str:
    transposed_bits = list(zip(*binarys))
    common_binary_number: str = ""
    for bit_column in transposed_bits:
        bit_column: tuple[str]
        zeros = bit_column.count("0")
        ones = bit_column.count("1")
        common_binary_number += "0" if zeros > ones else "1"
    return common_binary_number


def power_consumption(binarys: list[str]) -> int:
    most_comon = most_common_binary_number(binarys)
    least_common = flip(most_comon)
    return int(most_comon, 2) * int(least_common, 2)


def oxygen_rating(binarys: list[str], index: int = 0) -> int:
    if len(binarys) == 1:
        return int(binarys[0], 2)
    most_comon = most_common_binary_number(binarys)
    filtered_binarys: list[str] = []
    for binary in binarys:
        if binary[index] == most_comon[index]:
            filtered_binarys.append(binary)
    return oxygen_rating(filtered_binarys, index + 1)


def co2_rating(binarys: list[str], index: int = 0) -> int:
    if len(binarys) == 1:
        return int(binarys[0], 2)
    most_comon = most_common_binary_number(binarys)
    least_common = flip(most_comon)
    filtered_binarys: list[str] = []
    for binary in binarys:
        if binary[index] == least_common[index]:
            filtered_binarys.append(binary)
    return co2_rating(filtered_binarys, index + 1)


def life_support_rating(binarys: list[str]) -> int:
    oxygen = oxygen_rating(binarys)
    c02 = co2_rating(binarys)
    return oxygen * c02


def main():
    binarys = read_data(FILENAME)
    print(power_consumption(binarys))
    print(life_support_rating(binarys))


if __name__ == "__main__":
    main()
