class TextReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_blocks(self):
        with open(self.filepath, encoding='utf-8') as f:
            paragraphs = f.read().strip().split("\n\n")

        blocks = []
        for paragraph in paragraphs:
            lines = paragraph.strip().splitlines()
            for line in lines:
                words = line.strip().split()
                if words:
                    blocks.append(words)
            blocks.append(["__BLANK__"])
        return blocks