from PIL import Image, ImageDraw

ico_path = "apps_icon.ico"
img = Image.new("RGBA", (256, 256), (30, 120, 200, 255))
d = ImageDraw.Draw(img)
d.ellipse((32, 32, 224, 224), fill=(255, 255, 255, 255))
img.save(
    ico_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
)
print("WROTE", ico_path)
