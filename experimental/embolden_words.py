def add_bold_to_words(sentence, percentage):
    words = sentence.split()
    bolded_sentence = []

    for word in words:
        # Skip words starting with 'href=' or '<a'
        if word.startswith('href=') or word.startswith('<a'):
            print("here")
            bolded_sentence.append(word)
            continue

        bolded_chars = int(len(word) * percentage)
        bolded_word = f"<strong>{word[:bolded_chars]}</strong>{word[bolded_chars:]}"
        bolded_sentence.append(bolded_word)

    return ' '.join(bolded_sentence)