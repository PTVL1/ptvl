"""Render word clouds with Pillow without allocating NumPy occupancy arrays."""
import random
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def render_cloud(frequencies, width, height, color, limit, background=None, photo=None):
    if not 1 <= width <= 2048 or not 1 <= height <= 2048:
        raise ValueError("Dimensões fora do intervalo permitido.")
    font_path = Path(__file__).parent / "assets" / "cloud-font.ttf"
    # Pillow ships a scalable default font; no system font or NumPy is required.
    def font(size):
        return ImageFont.truetype(str(font_path), size) if font_path.exists() else ImageFont.load_default(size=size)

    with Image.new("RGBA", (width, height), background or (0, 0, 0, 0)) as canvas:
        if photo:
            with Image.open(BytesIO(photo)) as source:
                if source.width * source.height > 16_000_000:
                    raise ValueError("Escolhe uma imagem de fundo até 16 megapíxeis.")
                source.thumbnail((2048, 2048))
                with ImageOps.exif_transpose(source) as oriented:
                    with ImageOps.fit(oriented, (width, height)) as fitted:
                        canvas.paste(fitted, (0, 0))
        draw = ImageDraw.Draw(canvas)
        entries = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:limit]
        if not entries:
            raise ValueError("Não há palavras para representar.")
        occupied = []
        rng = random.Random(42)
        largest = entries[0][1]
        for word, count in entries:
            size = max(8, int(min(height * .28, width * .14, 150) * (.45 + .55 * count / largest)))
            placed = False
            while size >= 8 and not placed:
                face = font(size)
                box = draw.textbbox((0, 0), word, font=face)
                w, h = box[2] - box[0], box[3] - box[1]
                if w + 6 <= width and h + 6 <= height:
                    for attempt in range(180):
                        if not occupied and attempt == 0:
                            x, y = (width - w) // 2, (height - h) // 2
                        else:
                            x, y = rng.randint(3, width - w - 3), rng.randint(3, height - h - 3)
                        bounds = (x - 3, y - 3, x + w + 3, y + h + 3)
                        if all(bounds[2] <= a or bounds[0] >= c or bounds[3] <= b or bounds[1] >= d for a, b, c, d in occupied):
                            draw.text((x - box[0], y - box[1]), word, fill=color, font=face)
                            occupied.append(bounds)
                            placed = True
                            break
                size -= max(1, size // 6)
        if not occupied:
            raise ValueError("Aumenta as dimensões para caberem as palavras.")
        with BytesIO() as buffer:
            canvas.save(buffer, format="PNG")
            return buffer.getvalue()
