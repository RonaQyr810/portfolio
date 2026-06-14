from PIL import Image, ImageDraw, ImageFilter


def cover_fill(img: Image.Image, size=(1600, 1000), bg=None) -> Image.Image:
    rgb = img.convert("RGB")
    ow, oh = size
    if bg is None:
        bg = rgb.getpixel((0, 0))
    scale = max(ow / rgb.width, oh / rgb.height)
    nw, nh = int(rgb.width * scale), int(rgb.height * scale)
    fitted = rgb.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", size, bg)
    canvas.paste(fitted, ((ow - nw) // 2, (oh - nh) // 2))
    return canvas


def gradient_bg(size, top, bottom):
    w, h = size
    canvas = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(canvas)
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return canvas


def build_lixiang_cover(src_home, dst):
    phone = Image.open(src_home).convert("RGB")
    w, h = 1600, 1000
    canvas = gradient_bg((w, h), (236, 226, 248), (210, 198, 232))

    target_h = 960
    target_w = int(phone.width * target_h / phone.height)
    phone = phone.resize((target_w, target_h), Image.LANCZOS)

    radius = 42
    mask = Image.new("L", phone.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=radius, fill=255)

    x = (w - target_w) // 2
    y = (h - target_h) // 2 + 10

    shadow = Image.new("RGBA", (target_w + 48, target_h + 48), (0, 0, 0, 0))
    sh_mask = Image.new("L", shadow.size, 0)
    ImageDraw.Draw(sh_mask).rounded_rectangle(
        [18, 18, target_w + 30, target_h + 30], radius=radius + 8, fill=180
    )
    shadow.putalpha(sh_mask.filter(ImageFilter.GaussianBlur(12)))
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(shadow, (x - 24, y - 16))
    canvas.paste(phone, (x, y), mask)
    canvas.convert("RGB").save(dst, "PNG", optimize=True)


def build_moyan_cover(src_ui, dst):
    ui = Image.open(src_ui).convert("RGB")
    ui = ui.crop((420, 0, ui.width - 20, min(700, ui.height)))
    canvas = Image.new("RGB", (1600, 1000), (247, 242, 232))
    target_w = int(1600 * 0.9)
    target_h = int(ui.height * target_w / ui.width)
    if target_h > 940:
        target_h = 940
        target_w = int(ui.width * target_h / ui.height)
    ui = ui.resize((target_w, target_h), Image.LANCZOS)
    canvas.paste(ui, ((1600 - target_w) // 2, (1000 - target_h) // 2))
    canvas.save(dst, "PNG", optimize=True)


if __name__ == "__main__":
    root = r"c:\Users\echo9\Desktop\个人主页\assets\portfolio"
    build_lixiang_cover(
        rf"{root}\lixiang\home.png",
        rf"{root}\lixiang\cover.png",
    )
    build_moyan_cover(
        r"c:\Users\echo9\AppData\Local\Temp\cursor\screenshots\moyan-cover.png",
        rf"{root}\moyan-cover.png",
    )
    print("covers rebuilt")
