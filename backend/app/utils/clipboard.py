from PIL import Image
import win32clipboard
import io
from pathlib import Path

def copy_image_to_clipboard(image_path: Path):
    image = Image.open(image_path)

    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # BMP header hack
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
