# used on the Cambridge English Vocabulary List

# format word list
formatted_words : list = []
with open("word_list.txt") as f:
    for line in f.readlines():
        # break point
        if "--" in line:
            break
        # remove bullet points
        if "â€¢" in line:
            continue

        # remove line with / such as a/an
        if "/" in line:
            continue

        # remove synonyms
        if line[0] == "(":
            continue

        # remove poorly formatted words
        if "(" not in line and ")" not in line:
            continue

        # remove /n
        line = line[:-1]

        # remove badly formatted lines such as trailing word types (n) or trailing descriptions
        if line[-1] in ".!?":
            continue

        # remove alphabet titles e.g (A,B,C,D,E)
        if len(line) == 1:
            continue

        # remove american english type from british english line
        if "Am Eng:" in line:
            line = line.replace(" (Am Eng:", "")
        # remove british english type from american english line
        elif "Br Eng:" in line:
            line = line.replace(" (Br Eng:", "")

        # remove poor language type formatting
        if line[-2:] == "Br":
            line = line.replace("(Br", "")
        if line[-2:] == "Am":
            line = line.replace("(Am", "")

        # remove poorly formatted words as a result of language specifiction in example text
        if not "(" in line:
            continue

        # add " " to remaining lines where there is no " " due to poor formatting
        if not " " in line:
            line = line.replace("(", " (")

        # split into word and unformatted types
        word, types = line.split(" ", 1)

        # remove 1 and 2 length words
        if len(word) < 3:
            continue
        # format types
        map = str.maketrans({
            " " : "",
            "(" : "",
            ")" : "",
            "&" : ","
        })
        types = types.translate(map).split(",")
        formatted_words.append((word, types))

words = {
    "adjectives" : {},
    "nouns" : {},
    "verbs" : {},
    "adverbs" : {}
}

# insert words into dictionary

for word, types in formatted_words:
    for type in types:
        match type:
            case "abbrev":
                try: words["acronyms"][len(word)].append(word)
                except: words["acronyms"][len(word)] = [word]
            case "adj":
                try: words["adjectives"][len(word)].append(word)
                except: words["adjectives"][len(word)] = [word]
            case "adv":
                try: words["adverbs"][len(word)].append(word)
                except: words["adverbs"][len(word)] = [word]
            case "noun":
                try: words["nouns"][len(word)].append(word)
                except: words["nouns"][len(word)] = [word]
            case "singular":
                try: words["singulars"][len(word)].append(word)
                except: words["singulars"][len(word)] = [word]
            case "verb":
                try: words["verbs"][len(word)].append(word)
                except: words["verbs"][len(word)] = [word]