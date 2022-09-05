
def load_words(l = 5):
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


def search(words,greens, yellows, blacks):
    print(greens, yellows, blacks)
    print([yellows[b] for b in yellows])
    one = {word for word in words if len([yellows[b] for b in yellows if b in word]) == len(yellows)}
    two = {word for word in words if len([b for b in blacks if len([i for i in range(len(blacks[b])) if word[blacks[b][i] != b]]) == len(blacks[b])]) == len(blacks)}
    three = {word for word in words if len([b for b in greens if len([i for i in range(len(greens[b])) if word[greens[b][i]] == b]) == len(greens[b])]) == len(greens)}

    print(one)

    res = {word for word in words
           if len([b for b in yellows if b in word]) == len(yellows)
           and len([b for b in blacks if len([i for i in range(len(blacks[b])) if word[blacks[b][i] != b]]) == len(blacks[b])]) == len(blacks)
           and len([b for b in greens if len([i for i in range(len(greens[b])) if word[greens[b][i]] == b]) == len(greens[b])]) == len(greens)}
    return res


def check_greens(word, greens):
    valid = not any([True for buchstabe in greens for i in greens[buchstabe] if word[i] != buchstabe])
    return valid


def check_yellows(word, yellows):
    print('yellowss:', yellows)
    print(word)
    valid = not any([True for buchstabe in yellows for i in yellows[buchstabe] if word[i] == buchstabe])
    for i, s in enumerate(word):
        if s in yellows:
            if i in yellows[s]:
                valid = False

    for i in yellows:
        if i not in word:
            valid = False

    print("filtering for yellow condition")
    print(valid)


    return valid


def check_blacks(word, blacks):
    valid = not any([True for buchstabe in blacks if buchstabe in word])

    return valid


def check(alpha_pos, greens, yellows, blacks, words):
    valid_words = {word for word in words if check_greens(word, greens) and check_yellows(word, yellows) and check_blacks(word, blacks)}

    return valid_words


def val_append(dict_obj, key, value):
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            # converting key to list type
            dict_obj[key] = [dict_obj[key]]
        # Append the key's value in list
        if value in dict_obj[key]:
            return
        dict_obj[key].append(value)
    else:
        dict_obj.update({key: [value]})


def apply_potential_count(alpha_pos, key):
    for position in alpha_pos[key]:
        if alpha_pos[key][position] != 'locked':
            lock = [i for i in alpha_pos[key] if alpha_pos[key][i] == 'locked']
            alpha_pos[key][position] = len(alpha_pos[key]) - len([i for i in alpha_pos[key] if alpha_pos[key][i] == 'locked'])


def apply_greens(alpha_pos, greens):
    print("applying green to: ")
    print(alpha_pos)
    for green in greens:
        indizes = greens[green]
        for i in indizes:
            if i in alpha_pos[green]:
                alpha_pos[green][i] = 'locked'
        apply_potential_count(alpha_pos, green)
    print("green applied:")
    print(alpha_pos)


def apply_yellows(alpha_pos, yellows):
    print("applying yellow to: ")
    print(alpha_pos)
    print(yellows)
    for yellow in yellows:
        indizes = yellows[yellow]
        for i in indizes:
            if i in alpha_pos[yellow]:
                if alpha_pos[yellow][i] != 'locked':
                    del alpha_pos[yellow][i]

        apply_potential_count(alpha_pos, yellow)
    print("yellow applied: ")
    print(alpha_pos)


def apply_blacks(alpha_pos, blacks):
    print("applying black to: ")
    print(alpha_pos)
    for black in blacks:
        indizes = blacks[black]
        for i in indizes:
            if i in alpha_pos[black]:
                if alpha_pos[black][i] != 'locked':
                    del alpha_pos[black][i]

    print("black applied: ")
    print(alpha_pos)


def simulate(words_input, greens_input, words_dict):
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alpha_pos = {}
    n = len(words_input[0])
    for b in alph:
        alpha_pos.update({b: {i : n for i in range(n)}})
    greens, yellows, blacks = {}, {}, {}
    forbidden = {}
    for word_input, green_input in zip(words_input, greens_input):
        print(word_input)
        new_greens = green_input
        new_greens = [int(s) for s in new_greens.split(" ") if len(new_greens) != 0]
        {val_append(greens, s.lower(), i) for i, s in enumerate(word_input) if i in new_greens}
        {val_append(yellows, s.lower(), i) for i, s in enumerate(word_input) if s.isupper() and i not in new_greens}

        new_yellows = [s.lower() for i, s in enumerate(word_input) if s.isupper() and i not in new_greens]
        {val_append(blacks, s.lower(), i) for i, s in enumerate(word_input) if s.islower() and i not in new_greens and i not in new_yellows}

        word_input = word_input.lower()
        for g in new_greens:
            print("!!!")
            print(g)
            print(word_input[g])
            if word_input[g] in yellows:
                del yellows[word_input[g]]
        apply_greens(alpha_pos, greens)
        apply_yellows(alpha_pos, yellows)
        apply_blacks(alpha_pos, blacks)

        words_dict = check(alpha_pos, greens, yellows, blacks, words_dict)
        print(words_dict)
        print("keyboard")
        print(greens)
        print(new_greens)
        print(yellows)
        print(blacks)


def play(words_dict, word_input, green_input):
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alpha_pos = {}

    n = len(word_input)
    for b in alph:
        alpha_pos.update({b: {i: n for i in range(n)}})
    greens, yellows, blacks = {}, {}, {}


    while len(words_dict) >= 1:

        new_greens = green_input
        #new_greens = [int(s) for s in new_greens.split(" ") if len(new_greens) != 0]
        {val_append(greens, s.lower(), i) for i, s in enumerate(word_input) if i in new_greens}
        {val_append(yellows, s.lower(), i) for i, s in enumerate(word_input) if s.isupper() and i not in new_greens}

        new_yellows = [s.lower() for i, s in enumerate(word_input) if s.isupper() and i not in new_greens]
        print("before")
        print(word_input)
        print(blacks)
        for i, s in enumerate(word_input):
            print(i)
            print(s)
            print(i not in new_greens)
            print(i not in new_yellows)
        {val_append(blacks, s.lower(), i) for i, s in enumerate(word_input) if
         (s.islower() and s not in [word_input[new_g].lower() for new_g in new_greens] and i not in new_yellows)}

        print(blacks)
        word_input = word_input.lower()
        for g in new_greens:
            print("!!!")
            print(g)
            print(word_input[g])
            if word_input[g] in yellows:
                del yellows[word_input[g]]
        apply_greens(alpha_pos, greens)
        apply_yellows(alpha_pos, yellows)
        apply_blacks(alpha_pos, blacks)
        print('G Y B', greens, yellows, blacks)

        words_dict = check(alpha_pos, greens, yellows, blacks, words_dict)

        guess_list = [word for word in words_dict]

        sorted_by_vowels = sorted(guess_list, key = lambda word: sum(ch in 'aeiou' for ch in word), reverse = True)

        relevancy_dict = relevancy_score(guess_list)

        output = ('sorted by vowels: ', sorted(sorted_by_vowels,
                                        key = lambda word: sum(ch in 'aeiou' for ch in word if ch not in greens)))

        output_relevant = compare_guess(guess_list, relevancy_dict)


        print(output)
        print(output_relevant)
        print(len(words_dict) + len(output))


        if len(words_dict) == 1:
            print("solution: "+words_dict.pop())
            exit()
        word_input = input("word: ")
        green_input = input("greens: ")




def relevancy_score(input_dict):
    import csv

    with open('word_frequency.csv', mode='r') as inp:
        word_frequency = csv.reader(inp)
        dict_from_csv = {int(rows[0]): rows[1] for rows in word_frequency}

    #print(dict_from_csv)

# filter dict 5 letter words
    relevancy_dict = {}

    for (key, value) in dict_from_csv.items():
        # Check if len == 5
        if len(value) == 5:
            relevancy_dict[key] = value
    #print("Sortiert nach Relevanz: ", relevancy_dict)
    return relevancy_dict



def compare_guess(guess_list, relevancy_dict):

    solution_list = [word for (key, word) in relevancy_dict.items() if word in guess_list]

    return solution_list


def pre_processing():
    english_words = load_words()
    words_dict = {word: 1 for word in english_words if len(word) == 5}
    guess_list = [word for word in words_dict]
    relevancy_dict = relevancy_score(words_dict)
    return words_dict, guess_list



if __name__ == '__main__':
    words_dict, guess_list = pre_processing()

    print(play(words_dict, "lOool", [1]))

    '''
   # run relevancy_score:
    english_words = load_words()
    words_dict = {word: 1 for word in english_words if len(word) == 5}
    guess_list = [word for word in words_dict]
    sorted_by_vowels = guess_list
    relevancy_dict = relevancy_score(words_dict)


    print(compare_guess(guess_list, relevancy_dict))


    '''

    '''# run wordle:

    starters = ['louse', 'ahead', 'house']
    #test = ['aunts', 'mIght', 'bRIck', 'PRIdE']
    #greens = ['' , '', '1 2', '0 1 2 4']
    test = ['eAGle', 'AmONG', 'prize', 'suCks', 'biNit']
    greens = ['', '', '', '', '2']


    english_words = load_words()
    words_dict = {word: 1 for word in english_words if len(word) == 5}
    guess_list = [word for word in words_dict]
    relevancy_dict = relevancy_score(words_dict)
    solution_list = compare_guess(guess_list, relevancy_dict)

    play(words_dict, guess_list)
    #simulate(test, greens, words_dict)
    '''





