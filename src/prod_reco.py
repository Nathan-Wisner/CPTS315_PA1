from itertools import combinations
from multiprocessing import Pool

# Global variables. Could be used as config params
IN_FILE = "../pa1/data/browsing-data.txt"
OUT_FILE = "./output.txt"
SUPPORT = 100


# Read in the file
def read_input():
    with open(IN_FILE, "r") as text_file:
        all_lines = text_file.readlines()

    return all_lines


def groom_imported_data(imported_data):

    return [[data_point for data_point in line.split()] for line in imported_data]


def apriori_pass_1(data_set, s):

    item_counts = {}

    for basket in data_set:
        for item in basket:
            if item_counts.get(item):
                item_counts[item] = item_counts[item] + 1
            else:
                item_counts[item] = 1

    return {key: value for (key, value) in item_counts.items() if value >= s}


def apriori_pass_2(frequent_items, data_set, s):
    item_counts = {}
    line_count = 0

    candidates = [list(elem) for elem in combinations(frequent_items, 2)]

    for line in data_set:
        line_count += 1
        print(f"Line #{line_count} of {len(data_set)}\n")
        for candidate in candidates:
            if set(candidate).issubset(line):
                key = tuple(candidate)

                if item_counts.get(key):
                    item_counts[key] = item_counts[key] + 1
                else:
                    item_counts[key] = 1




    # for line in data_set:

    #     line_combinations = set(combinations(line, 2))

    #     for combination in line_combinations:
    #         if combination[0] in frequent_items and combination[1] in frequent_items:

    #             if item_counts.get(combination):
    #                 item_counts[combination] = item_counts[combination] + 1
    #             else:
    #                 item_counts[combination] = 1

    return {key: value for (key, value) in item_counts.items() if value >= s}


def apriori_pass_3(frequent_items, data_set, s):
    item_counts = {}

    for line in data_set:

        tripples = set(combinations(line, 3))

        for combination in tripples:
            if combination[0] in frequent_items and combination[1] in frequent_items and combination[2] in frequent_items:

                if item_counts.get(combination):
                    item_counts[combination] = item_counts[combination] + 1
                else:
                    item_counts[combination] = 1

    return {key: value for (key, value) in item_counts.items() if value >= s}


def compute_pairs_confidence(frequent_singles, frequent_pairs):
    confidences = {}

    for pair in frequent_pairs.keys():
        confidences[pair] = frequent_pairs[pair] / frequent_singles[pair[0]]

    return sorted(confidences.items(), key=lambda x: x[1], reverse=True)


def generate_group(item_set, group_size):

    return [list(group) for group in combinations(item_set, group_size)]


# file dumping
def dump_output():
    with open(OUT_FILE, "w") as text_file:
        pass
    return


def main():

    # Read the input file
    all_lines = read_input()

    # Groom the data to a lists of lists of strings
    groomed_data = groom_imported_data(all_lines)

    pool = Pool(processes=4)

    # Find frequent singles
    support_singles = apriori_pass_1(groomed_data, SUPPORT)
    # support_singles = pool.apply_async(apriori_pass_1, [groomed_data, SUPPORT]).get()

    keys = list(support_singles.keys())
    

    support_pairs = pool.starmap(apriori_pass_2(
            list(support_singles.keys()), groomed_data, SUPPORT))

    # answer = support_pairs.get(timeout= None)

    # Find frequest pairs
    # support_pairs = pool.map(apriori_pass_2(
    #     list(support_singles.keys()), groomed_data, SUPPORT))
    
    # support_triples = apriori_pass_3(
    #     list(chain(*support_pairs.keys())), groomed_data, SUPPORT)

    # # Compute confidences for pairs
    # pairs_confidence = compute_pairs_confidence(support_singles, support_pairs)
    # print(support_pairs)
    # dump_output()


if __name__ == '__main__':
    main()

    # text_file.write("OUTPUT A\n")
    # text_file.write("FRO11987 FRO12685 0.4325\n")
    # text_file.write("FRO11987 ELE11375 0.4225\n")
    # text_file.write("FRO11987 GRO94758 0.4125\n")
    # text_file.write("FRO11987 SNA80192 0.4025\n")
    # text_file.write("FRO11987 FRO18919 0.4015\n")
    # text_file.write("OUTPUT B\n")
    # text_file.write("FRO11987 FRO12685 DAI95741 0.4325\n")
    # text_file.write("FRO11987 ELE11375 GRO73461 0.4225\n")
    # text_file.write("FRO11987 GRO94758 ELE26917 0.4125\n")
    # text_file.write("FRO11987 SNA80192 ELE28189 0.4025\n")
    # text_file.write("FRO11987 FRO18919 GRO68850 0.4015\n")
