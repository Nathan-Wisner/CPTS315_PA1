from itertools import combinations, chain
from multiprocessing import Pool

# Global variables. Could be used as config params
IN_FILE = "../pa1/data/browsing-data.txt"
OUT_FILE = "./output.txt"
SUPPORT = 15


# Read in the file
def read_input():
    with open(IN_FILE, "r") as text_file:
        all_lines = text_file.readlines()

    return all_lines


def groom_imported_data(imported_data):

    # Format each line into list form
    # and
    # return the list of lists
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
    milestone = int(len(data_set) / 10)

    candidates = set(combinations(frequent_items, 2))

    print(f"A-Priori pass 2 completion: {'{:.0%}'.format(line_count / len(data_set))}")

    for line in data_set:

        for candidate in candidates:
            if candidate[0] in line and candidate[1] in line:

                if item_counts.get(candidate):
                    item_counts[candidate] = item_counts[candidate] + 1
                else:
                    item_counts[candidate] = 1

        line_count += 1
        if line_count % milestone == 0:
            print(
                f"A-Priori pass 2 completion: {'{:.0%}'.format(line_count / len(data_set))}")

    return {key: value for (key, value) in item_counts.items() if value >= s}


def apriori_pass_3(frequent_items, data_set, s):
    item_counts = {}
    line_count = 0
    milestone = int(len(data_set) / 50)

    triples = set(combinations(frequent_items, 3))
    print(f"A-Priori pass 3 completion: {'{:.0%}'.format(line_count / len(data_set))}")
    

    for line in data_set:

        for combination in triples:
            if combination[0] in line and combination[1] in line and combination[2] in line:

                if item_counts.get(combination):
                    item_counts[combination] = item_counts[combination] + 1
                else:
                    item_counts[combination] = 1

        line_count += 1
        if line_count % milestone == 0:
            print(f"A-Priori pass 3 completion: {'{:.0%}'.format(line_count / len(data_set))}")

    return {key: value for (key, value) in item_counts.items() if value >= s}


def compute_pairs_confidence(frequent_singles, frequent_pairs):
    confidences = {}

    for pair in frequent_pairs.keys():
        # {X} --> Y
        confidences[(pair[0], pair[1])] = frequent_pairs[pair] / \
            frequent_singles[pair[0]]

        # {Y} --> X
        confidences[(pair[1], pair[0])] = frequent_pairs[pair] / \
            frequent_singles[pair[1]]

    # Sort data and return
    return sorted(confidences.items(), key=lambda x: x[1], reverse=True)


def compute_triples_confidence(frequent_singles, frequent_pairs, frequent_triples):
    confidences = {}

    for triple in frequent_triples.keys():
        # {X, Y} --> Z
        denominator = frequent_pairs.get((triple[0], triple[1])) or \
            frequent_pairs.get((triple[1], triple[0]))

        confidences[(triple[0], triple[1], triple[2])] = \
            frequent_triples[triple] / denominator

        # {X, Z} --> Y
        denominator = frequent_pairs.get((triple[0], triple[2])) or \
            frequent_pairs.get((triple[2], triple[0]))

        confidences[(triple[0], triple[2], triple[1])] = \
            frequent_triples[triple] / denominator

        # {Y, Z} --> X
        denominator = frequent_pairs.get((triple[1], triple[2])) or \
            frequent_pairs.get((triple[2], triple[1]))

        confidences[(triple[1], triple[2], triple[0])] = \
            frequent_triples[triple] / denominator

    # Sort data and return
    return sorted(confidences.items(), key=lambda x: x[1], reverse=True)


# file dumping
def dump_output(pairs_results, triples_results):
    with open(OUT_FILE, "w") as text_file:
        
        # Write the pairs + association
        text_file.write("OUTPUT A\n")
        for result in pairs_results:
            text_file.write(f"{result[0][0]} {result[0][1]} {result[1]}\n")
        
        # Write the triples + association
        text_file.write("OUTPUT B\n")
        for result in triples_results:
            text_file.write(f"{result[0][0]} {result[0][1]} {result[0][2]} {result[1]}\n")

    return


def main():

    # Read the input file
    all_lines = read_input()

    # Groom the data to a lists of lists of strings
    groomed_data = groom_imported_data(all_lines)

    # Find frequent singles
    print("Finding frequent singles")
    support_singles = apriori_pass_1(groomed_data, SUPPORT)
    print("Done")

    # Find frequent pairs
    singles = list(support_singles.keys())
    print("Finding frequent pairs")
    support_pairs = apriori_pass_2(
        singles, groomed_data, SUPPORT)
    print("Done")

    # Find frequent triples
    print("Finding frequent triples")
    frequent_items = set(chain.from_iterable(support_pairs))
    support_triples = apriori_pass_3(frequent_items, groomed_data, SUPPORT)
    print("Done")

    # Calculate association confidences of pairs
    print("Calculating pairs confidences")
    pairs_confidences = compute_pairs_confidence(
        support_singles, support_pairs)

    # Calculate association confidences of triples
    print("Calculating triples confidences")
    triples_confidences = compute_triples_confidence(
        support_singles, support_pairs, support_triples)

    pairs_results = pairs_confidences[:5]
    triples_results = triples_confidences[:5]

    # Dump the results
    dump_output(pairs_results, triples_results)

    print(f"Results data written! Please see {OUT_FILE} for results.")


if __name__ == '__main__':
    main()