import random

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
    valid = not any([True for buchstabe in yellows for i in yellows[buchstabe] if word[i] == buchstabe])
    for i, s in enumerate(word):
        if s in yellows:
            if i in yellows[s]:
                valid = False

    for i in yellows:
        if i not in word:
            valid = False

    print("filtering for yellow condition")


    return valid


def check_blacks(word, blacks):
    valid = not any([True for buchstabe in blacks if buchstabe in word])
    print(valid)

    return valid


def check(alph_pos, greens, yellows, blacks, words):
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


def apply_potential_count(alph_pos, key):
    for position in alph_pos[key]:
        if alph_pos[key][position] != 'locked':
            lock = [i for i in alph_pos[key] if alph_pos[key][i] == 'locked']
            alph_pos[key][position] = len(alph_pos[key])-len([i for i in alph_pos[key] if alph_pos[key][i] == 'locked'])


def apply_greens(alph_pos, greens):
    print("applying green to: ")
    print(alph_pos)
    for green in greens:
        indizes = greens[green]
        for i in indizes:
            if i in alph_pos[green]:
                alph_pos[green][i] = 'locked'
        apply_potential_count(alph_pos, green)
    print("green applied:")
    print(alph_pos)


def apply_yellows(alph_pos, yellows):
    print("applying yellow to: ")
    print(alph_pos)
    print(yellows)
    for yellow in yellows:
        indizes = yellows[yellow]
        for i in indizes:
            if i in alph_pos[yellow]:
                if alph_pos[yellow][i] != 'locked':
                    del alph_pos[yellow][i]

        apply_potential_count(alph_pos, yellow)
    print("yellow applied: ")
    print(alph_pos)


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
    alph_pos = {}
    n = len(words_input[0])
    for b in alph:
        alph_pos.update({b: {i : n for i in range(n)}})
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
        #apply_greens(alph_pos, greens)
        #apply_yellows(alph_pos, yellows)
        #apply_blacks(alph_pos, blacks)

        words_dict = check(alph_pos, greens, yellows, blacks, words_dict)
        print(words_dict)
        print("keyboard")
        print(greens)
        print(new_greens)
        print(yellows)
        print(blacks)


def play(words_dict):
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alph_pos = {}
    word_input = input("word: ")
    green_input = input("greens: ")
    n = len(word_input)
    for b in alph:
        alph_pos.update({b: {i: n for i in range(n)}})
    greens, yellows, blacks = {}, {}, {}

    while len(words_dict) >= 1:

        new_greens = green_input
        new_greens = [int(s) for s in new_greens.split(" ") if len(new_greens) != 0]
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
        print(new_yellows)
        {val_append(blacks, s.lower(), i) for i, s in enumerate(word_input) if
         (s.islower() and s not in [word_input[new_g].lower() for new_g in new_greens]) and (s.lower() not in new_yellows)}

        print(blacks)
        word_input = word_input.lower()
        for g in new_greens:
            print("!!!")
            print(g)
            print(word_input[g])
            if word_input[g] in yellows:
                del yellows[word_input[g]]
        # apply_greens(alph_pos, greens)
        # apply_yellows(alph_pos, yellows)
        # apply_blacks(alph_pos, blacks)

        words_dict = check(alph_pos, greens, yellows, blacks, words_dict)
        print(words_dict)
        if len(words_dict) == 1:
            print("solution: "+words_dict.pop())
            exit()
        word_input = input("word: ")
        green_input = input("greens: ")



if __name__ == '__main__':
    starters = ['louse', 'ahead', 'house']
    #test = ['aunts', 'mIght', 'bRIck', 'PRIdE']
    #greens = ['' , '', '1 2', '0 1 2 4']
    test = ['eAGle', 'AmONG', 'prize', 'suCks', 'biNit']
    greens = ['', '', '', '', '2']

    english_words = load_words()
    words_dict = {word: 1 for word in english_words if len(word) == 5}

    play(words_dict)
    #simulate(test, greens, words_dict)







