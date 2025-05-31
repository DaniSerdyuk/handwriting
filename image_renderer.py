from PIL import Image, ImageDraw
import os

class ImageRenderer:
    def __init__(self, text_blocks, formatter, font, config):
        self.text_blocks = text_blocks
        self.formatter = formatter
        self.font = font
        self.config = config
        self.block_index = 0
        self.output_index = 1

        os.makedirs(config['output_dir'], exist_ok=True)

    def render_images(self):
        image_dir = self.config.get('image_dir', '.')
        for filename in sorted(os.listdir(image_dir)):
            if not filename.endswith(".jpg") or filename.count("_") != 8:
                continue

            try:
                name = os.path.splitext(filename)[0]
                x1, y1, x2, y2, x3, y3, x4, y4, line_height = map(int, name.split("_"))
            except Exception as e:
                print(f"⚠️ Skipped: {filename}: {e}")
                continue

            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(image)

            max_width = abs(x2 - x1) - 10
            avg_top_y = (y1 + y2) / 2
            avg_bottom_y = (y3 + y4) / 2
            total_lines = int((avg_bottom_y - avg_top_y) // line_height)

            i = 0
            while i < total_lines and self.block_index < len(self.text_blocks):
                t = i / total_lines
                x = int((1 - t) * x1 + t * x3) + self.config['text_x_offset']
                y = int((1 - t) * y1 + t * y3)

                current_block = self.text_blocks[self.block_index]

                if current_block == ["__BLANK__"]:
                    i += 1
                    self.block_index += 1
                    continue

                fitted = self.formatter.fit_words(current_block, max_width)

                if not fitted:
                    print(f"⛔ Line {i+1}/{total_lines} | y={int(y)} | ❗ Word too long: \"{current_block[0]}\"")
                    self.block_index += 1
                    continue

                draw_x = x
                for word in fitted:
                    draw.text((draw_x, y), word, font=self.font, fill=self.config['ink_color'])
                    draw_x += self.font.getlength(word) + self.config['word_spacing']

                self.text_blocks[self.block_index] = current_block[len(fitted):]

                if not self.text_blocks[self.block_index]:
                    self.block_index += 1

                i += 1

            out_path = os.path.join(self.config['output_dir'], f"{self.output_index}.jpg")
            image.save(out_path)
            print(f"💾 Saved: {out_path}")
            self.output_index += 1

            if self.block_index >= len(self.text_blocks):
                print("✅ Done.")
                break
