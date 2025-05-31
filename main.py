from PIL import ImageFont
from text_reader import TextReader
from text_formatter import TextFormatter
from image_renderer import ImageRenderer

if __name__ == "__main__":
    CONFIG = {
        'font_paths': [
            "fonts/Rozovii_Chulok.ttf",
            # "fonts/BetinaScriptCTT.ttf",
            # "fonts/Peach Cream.ttf",
            # "fonts/mr_GuardianCircusG.otf",
            # "fonts/Alistair Signature.ttf",
            "fonts/rabbits-elf.ttf",
        ],
        'font_size': 28,
        'text_file': "text.txt",
        'ink_color': (26, 42, 94),
        'text_x_offset': 5,
        'word_spacing': 10,
        'output_dir': "results",
        "image_dir": "images",
    }

    font = ImageFont.truetype(CONFIG['font_paths'][0], CONFIG['font_size'])
    reader = TextReader(CONFIG['text_file'])
    blocks = reader.read_blocks()

    formatter = TextFormatter(CONFIG['word_spacing'])
    renderer = ImageRenderer(blocks, formatter, CONFIG)
    renderer.render_images()