import unittest
from io import BytesIO
from PIL import Image
from cloud_renderer import render_cloud


class CloudTests(unittest.TestCase):
    def test_dimensions_transparency_and_color(self):
        png = render_cloud({'mar': 3, 'luz': 2}, 1200, 430, '#914C51', 30)
        with Image.open(BytesIO(png)) as image:
            self.assertEqual(image.size, (1200, 430))
            self.assertEqual(image.getpixel((0, 0))[3], 0)
        png = render_cloud({'mar': 3}, 300, 200, '#914C51', 30, '#FCE5D9')
        with Image.open(BytesIO(png)) as image:
            self.assertEqual(image.getpixel((0, 0)), (252, 229, 217, 255))

    def test_photo_background(self):
        photo = BytesIO()
        Image.new('RGB', (100, 100), '#123456').save(photo, 'PNG')
        png = render_cloud({'mar': 3}, 300, 200, '#FFFFFF', 30, photo=photo.getvalue())
        with Image.open(BytesIO(png)) as image:
            self.assertEqual(image.getpixel((0, 0)), (18, 52, 86, 255))

    def test_tiny_canvas_is_recoverable(self):
        with self.assertRaises(ValueError):
            render_cloud({'mar': 3}, 1, 1, '#FFFFFF', 30)


if __name__ == '__main__':
    unittest.main()
