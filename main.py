from PIL import Image, ImageDraw, ImageFont
import os

font_path = "Rozovii_Chulok.ttf"
font_size = 28
text_file = "text.txt"
ink_color = (26, 42, 94)
text_x_offset = 5
word_spacing_px = 10
output_dir = "results"

os.makedirs(output_dir, exist_ok=True)

with open(text_file, encoding='utf-8') as f:
    paragraphs = f.read().strip().split("\n\n")

text_blocks = []
for paragraph in paragraphs:
    lines = paragraph.strip().splitlines()
    for line in lines:
        words = line.strip().split()
        if words:
            text_blocks.append(words)
    text_blocks.append(["__BLANK__"])

font = ImageFont.truetype(font_path, font_size)

def fit_words_in_width(words, font, max_width):
    fitted = []
    width = 0
    for i, word in enumerate(words):
        word_width = font.getlength(word)
        space_width = word_spacing_px if i > 0 else 0
        if width + word_width + space_width <= max_width:
            fitted.append(word)
            width += word_width + space_width
        else:
            break
    return fitted

block_index = 0
output_index = 1

for filename in sorted(os.listdir(".")):
    if not filename.endswith(".jpg") or filename.count("_") != 8:
        continue

    try:
        name = os.path.splitext(filename)[0]
        x1, y1, x2, y2, x3, y3, x4, y4, line_height = map(int, name.split("_"))
    except Exception as e:
        print(f"⚠️ Skipped: {filename}: {e}")
        continue

    image = Image.open(filename).convert("RGB")
    draw = ImageDraw.Draw(image)

    max_text_width = abs(x2 - x1) - 10
    avg_top_y = (y1 + y2) / 2
    avg_bottom_y = (y3 + y4) / 2
    total_lines = int((avg_bottom_y - avg_top_y) // line_height)

    i = 0
    while i < total_lines and block_index < len(text_blocks):
        t = i / total_lines
        x = int((1 - t) * x1 + t * x3) + text_x_offset
        y = int((1 - t) * y1 + t * y3)

        current_block = text_blocks[block_index]

        if current_block == ["__BLANK__"]:
            i += 1
            block_index += 1
            continue

        fitted = fit_words_in_width(current_block, font, max_text_width)

        if not fitted:
            print(f"⛔ String {i+1}/{total_lines} | y={int(y)} | ❗ Words in block too long: \"{current_block[0]}\"")
            block_index += 1
            continue

        draw_x = x
        for word in fitted:
            draw.text((draw_x, y), word, font=font, fill=ink_color)
            draw_x += font.getlength(word) + word_spacing_px

        text_blocks[block_index] = current_block[len(fitted):]

        if not text_blocks[block_index]:
            block_index += 1

        i += 1

    out_path = os.path.join(output_dir, f"{output_index}.jpg")
    image.save(out_path)
    print(f"💾 Saved: {out_path}")
    output_index += 1

    if block_index >= len(text_blocks):
        print("✅ Done.")
        break
