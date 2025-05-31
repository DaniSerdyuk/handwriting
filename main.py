from PIL import ImageFont
from text_reader import TextReader
from text_formatter import TextFormatter
from image_renderer import ImageRenderer

if __name__ == "__main__":
    CONFIG = {
        'font_path': "fonts/Rozovii_Chulok.ttf",
        'font_size': 28,
        'text_file': "text.txt",
        'ink_color': (26, 42, 94),
        'text_x_offset': 5,
        'word_spacing': 10,
        'output_dir': "results",
        "image_dir": "images",
    }

    font = ImageFont.truetype(CONFIG['font_path'], CONFIG['font_size'])
    reader = TextReader(CONFIG['text_file'])
    blocks = reader.read_blocks()

    formatter = TextFormatter(font, CONFIG['word_spacing'])
    renderer = ImageRenderer(blocks, formatter, font, CONFIG)
    renderer.render_images()