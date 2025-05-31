class TextFormatter:
    def __init__(self, font, word_spacing):
        self.font = font
        self.word_spacing = word_spacing

    def fit_words(self, words, max_width):
        fitted = []
        width = 0

        for i, word in enumerate(words):
            word_width = self.font.getlength(word)
            space_width = self.word_spacing if i > 0 else 0
            if width + word_width + space_width <= max_width:
                fitted.append(word)
                width += word_width + space_width
            else:
                break

        return fitted