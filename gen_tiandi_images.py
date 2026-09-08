# -*- coding: utf-8 -*-
"""生成天地伟业设备密码重置操作方法 6 张步骤示意图，替换空白占位图。"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"D:\嘉驰蓝海项目\博客发布\images\天地伟业设备密码重置操作方法"
os.makedirs(OUT, exist_ok=True)

W, H = 1000, 560
BG       = (244, 247, 251)
CARD     = (255, 255, 255)
HEADER   = (38, 110, 224)
HEADER2  = (26, 80, 168)
ACCENT   = (64, 150, 255)
DARK     = (28, 40, 58)
GRAY     = (108, 120, 135)
LINE     = (210, 220, 232)
GREEN    = (46, 160, 90)
ORANGE   = (226, 138, 38)
RED      = (210, 70, 70)

FONT_BOLD = r"C:\Windows\Fonts\simhei.ttf"
FONT_REG  = r"C:\Windows\Fonts\msyh.ttc"  # index 0

def fb(size): return ImageFont.truetype(FONT_BOLD, size)
def fr(size): return ImageFont.truetype(FONT_REG, size, index=0)

def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def wrap(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def draw_header(img, d, step_label, title):
    rr(d, [0, 0, W, 88], 0, fill=HEADER)
    rr(d, [0, 60, W, 88], 0, fill=HEADER2)
    # 左侧步骤徽标
    rr(d, [32, 22, 100, 66], 12, fill=(255, 255, 255))
    text(d, (66, 46), step_label, fb(22), HEADER, anchor="mm")
    text(d, (120, 44), title, fb(26), (255, 255, 255), anchor="lm")

def draw_caption(d, lines):
    y = H - 70
    for ln in lines:
        for i, seg in enumerate(wrap(ln, 26)):
            text(d, (40, y + i*26), seg, fr(17), GRAY, anchor="lm")
        y += 26 * len(wrap(ln, 26)) + 2

def base(step_label, title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    rr(d, [24, 100, W-24, H-100], 16, fill=CARD, outline=LINE, width=2)
    draw_header(img, d, step_label, title)
    return img, d

def draw_phone(d, cx, top, w=210, h=400, screen_fill=(235, 242, 252)):
    left = cx - w//2
    rr(d, [left, top, left+w, top+h], 26, fill=(255,255,255), outline=DARK, width=4)
    rr(d, [left+10, top+14, left+w-10, top+h-14], 16, fill=screen_fill, outline=LINE, width=2)
    # 听筒
    d.ellipse([cx-14, top+6, cx+14, top+16], fill=DARK)
    return left, top, w, h

def draw_qr(d, x, y, cell=8, n=21):
    # 背景白
    rr(d, [x-6, y-6, x+n*cell+6, y+n*cell+6], 6, fill=(255,255,255), outline=LINE, width=2)
    import random
    rnd = random.Random(20260908)
    grid = [[False]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            grid[r][c] = rnd.random() > 0.5
    # finder patterns
    def finder(r0, c0):
        for r in range(7):
            for c in range(7):
                edge = r in (0,6) or c in (0,6)
                inner = 2 <= r <= 4 and 2 <= c <= 4
                grid[r0+r][c0+c] = edge or inner
    finder(0,0); finder(0,n-7); finder(n-7,0)
    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                d.rectangle([x+c*cell, y+r*cell, x+c*cell+cell-1, y+r*cell+cell-1], fill=DARK)
    return x, y, n*cell

# ---------- image1 步骤一 ----------
img, d = base("步骤一", "下载并安装「设备管理应用软件」")
_, _, _, ph = draw_phone(d, 300, 130)
text(d, (300, 150), "应用商店", fb(18), DARK, anchor="mm")
# 下载云
d.polygon([(640,200),(720,200),(720,250),(640,250)], fill=ACCENT)
text(d, (680, 225), "下载", fb(20), (255,255,255), anchor="mm")
d.line([(470,330),(610,330)], fill=GREEN, width=4)
d.polygon([(610,318),(610,342),(628,330)], fill=GREEN)
text(d, (680, 330), "搜索安装", fb(20), DARK, anchor="lm")
# 步骤说明卡
rr(d, [560, 380, 940, 470], 12, fill=(232,242,253), outline=ACCENT, width=2)
text(d, (580, 405), "在手机应用商店搜索", fr(18), DARK, anchor="lm")
text(d, (580, 432), "「设备管理应用软件」并完成安装", fr(18), DARK, anchor="lm")
draw_caption(d, ["说明：该 APP 用于生成设备安全码、找回/重置密码，是后续步骤的入口。"])
img.save(os.path.join(OUT, "image1.png"))

# ---------- image2 步骤二 ----------
img, d = base("步骤二", "设备与电脑接入同一局域网")
# 电脑
rr(d, [120, 200, 300, 290], 10, fill=(230,238,250), outline=DARK, width=3)
d.rectangle([140, 215, 280, 270], fill=(255,255,255), outline=LINE, width=2)
text(d, (210, 255), "电脑", fb(18), DARK, anchor="mm")
# 路由器/交换机
rr(d, [430, 215, 560, 270], 10, fill=(230,238,250), outline=DARK, width=3)
for i in range(4):
    d.rectangle([448+i*26, 230, 462+i*26, 244], fill=GREEN)
text(d, (495, 258), "交换机/路由器", fb(15), DARK, anchor="mm")
# 摄像头
rr(d, [720, 195, 860, 250], 10, fill=(230,238,250), outline=DARK, width=3)
d.ellipse([820, 205, 852, 240], fill=ACCENT)
text(d, (790, 290), "天地伟业IPC", fb(16), DARK, anchor="mm")
# 连接线
d.line([(300,245),(430,245)], fill=GRAY, width=3)
d.line([(560,245),(720,225)], fill=GRAY, width=3)
# 提示便签
rr(d, [560, 360, 940, 470], 12, fill=(255,247,232), outline=ORANGE, width=2)
text(d, (580, 385), "注意：老版本 EASY7 设备", fb(18), ORANGE, anchor="lm")
text(d, (580, 415), "可免密码直接修改 IP，无需走安全码流程", fr(17), DARK, anchor="lm")
draw_caption(d, ["说明：确保电脑与摄像机在同一网段，软件才能搜索到设备并生成二维码。"])
img.save(os.path.join(OUT, "image2.png"))

# ---------- image3 步骤三 ----------
img, d = base("步骤三", "软件生成二维码，扫码获取安全码")
# 左：设备管理APP生成二维码
_, _, _, ph = draw_phone(d, 270, 130)
qs = 21*8
qx, qy, qs = draw_qr(d, 270-qs//2, 165)
text(d, (270, 150), "设备管理APP", fb(15), DARK, anchor="mm")
text(d, (270, 165+qs+24), "安全码二维码", fb(15), GRAY, anchor="mm")
# 右：微信/APP扫码
_, _, _, ph = draw_phone(d, 730, 130)
text(d, (730, 150), "微信/APP", fb(15), DARK, anchor="mm")
# 扫描框
rr(d, [665, 175, 795, 305], 10, fill=(235,242,252), outline=ACCENT, width=3)
d.line([(665,235),(695,235)], fill=RED, width=3)
d.line([(665,235),(665,265)], fill=RED, width=3)
d.line([(795,235),(765,235)], fill=RED, width=3)
d.line([(795,235),(795,265)], fill=RED, width=3)
text(d, (730, 340), "扫一扫", fb(15), GRAY, anchor="mm")
# 中间箭头
d.line([(400,330),(600,330)], fill=GREEN, width=4)
d.polygon([(600,318),(600,342),(618,330)], fill=GREEN)
rr(d, [560, 380, 940, 475], 12, fill=(232,242,253), outline=ACCENT, width=2)
text(d, (580, 405), "公众号【技术服务】→【密码找回】", fr(17), DARK, anchor="lm")
text(d, (580, 435), "或 APP【我的】→【设备密码找回】扫码", fr(17), DARK, anchor="lm")
draw_caption(d, ["说明：二维码由设备管理软件生成，微信或APP扫描后获取本机安全码。"])
img.save(os.path.join(OUT, "image3.png"))

# ---------- image4 步骤四 ----------
img, d = base("步骤四", "输入安全码，设置新密码完成重置")
# 对话框
dx, dy, dw, dh = 330, 150, 360, 320
rr(d, [dx, dy, dx+dw, dy+dh], 14, fill=(255,255,255), outline=DARK, width=3)
text(d, (dx+dw//2, dy+26), "设备密码重置", fb(20), HEADER, anchor="mm")
d.line([(dx, dy+48),(dx+dw, dy+48)], fill=LINE, width=2)
# 字段
fields = [("安全码", "**** ****"), ("新密码", "********"), ("确认新密码", "********")]
fy = dy+70
for lab, val in fields:
    text(d, (dx+24, fy), lab, fr(16), DARK, anchor="lm")
    rr(d, [dx+110, fy-6, dx+dw-24, fy+22], 6, fill=(244,247,251), outline=LINE, width=2)
    text(d, (dx+124, fy+8), val, fr(15), GRAY, anchor="lm")
    fy += 56
# 确定按钮
rr(d, [dx+dw//2-60, dy+dh-56, dx+dw//2+60, dy+dh-20], 10, fill=GREEN)
text(d, (dx+dw//2, dy+dh-38), "确 定", fb(18), (255,255,255), anchor="mm")
rr(d, [560, 380, 940, 470], 12, fill=(232,242,253), outline=ACCENT, width=2)
text(d, (580, 405), "输入软件提供的安全码，", fr(17), DARK, anchor="lm")
text(d, (580, 435), "设置新密码后点「确定」即完成重置", fr(17), DARK, anchor="lm")
draw_caption(d, ["说明：安全码有时效，请在生成后及时填写，避免失效需重新获取。"])
img.save(os.path.join(OUT, "image4.png"))

# ---------- image5 提示1&2 ----------
img, d = base("温馨提示", "收不到短信 / 无二维码：走人工")
rr(d, [560, 130, 940, 300], 12, fill=(255,247,232), outline=ORANGE, width=2)
text(d, (580, 158), "提示 1 · 手机号收不到短信", fb(18), ORANGE, anchor="lm")
text(d, (580, 190), "在软件中导出「秘钥文件」，", fr(16), DARK, anchor="lm")
text(d, (580, 214), "连同设备信息发给人工客服处理", fr(16), DARK, anchor="lm")
text(d, (580, 256), "提示 2 · 设备无二维码", fb(18), ORANGE, anchor="lm")
text(d, (580, 288), "提供 SN / 工厂ID / 运行时间", fr(16), DARK, anchor="lm")
text(d, (580, 312), "给人工客服，由客服协助生成", fr(16), DARK, anchor="lm")
# 左：人工客服图标
rr(d, [120, 200, 360, 300], 12, fill=(232,242,253), outline=ACCENT, width=2)
d.ellipse([200, 215, 280, 295], fill=ACCENT)
text(d, (240, 255), "人", fb(28), (255,255,255), anchor="mm")
text(d, (240, 330), "人工客服", fb(16), DARK, anchor="mm")
draw_caption(d, ["说明：以上两种情况均无法自助扫码，需联系天地伟业人工客服线下协助。"])
img.save(os.path.join(OUT, "image5.png"))

# ---------- image6 提示3 ----------
img, d = base("温馨提示", "非本人手机号：人工获取安全码")
rr(d, [120, 180, 420, 320], 12, fill=(232,242,253), outline=ACCENT, width=2)
text(d, (270, 210), "绑定手机号", fb(18), HEADER, anchor="mm")
text(d, (270, 245), "非本人实名", fb(16), RED, anchor="mm")
text(d, (270, 280), "无法自助收码", fr(16), DARK, anchor="mm")
# 流程箭头
d.line([(420,250),(560,250)], fill=GRAY, width=3)
d.polygon([(560,238),(560,262),(578,250)], fill=GRAY)
rr(d, [560, 180, 880, 320], 12, fill=(255,247,232), outline=ORANGE, width=2)
text(d, (600, 210), "走人工「获取安全码」", fb(18), ORANGE, anchor="lm")
text(d, (600, 245), "向客服说明设备归属情况，", fr(16), DARK, anchor="lm")
text(d, (600, 269), "由客服核实后协助发放安全码", fr(16), DARK, anchor="lm")
text(d, (600, 300), "再回到步骤三 / 四完成重置", fr(16), DARK, anchor="lm")
draw_caption(d, ["说明：设备绑定手机号非本人时，自助流程受限，须人工介入获取安全码。"])
img.save(os.path.join(OUT, "image6.png"))

print("生成完成：", OUT)
for i in range(1,7):
    p = os.path.join(OUT, f"image{i}.png")
    print(p, os.path.getsize(p), "bytes")
