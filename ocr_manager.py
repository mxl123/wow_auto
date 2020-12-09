from PIL import ImageGrab, Image, ImageEnhance

# 裁剪
def cut_image(in_image_path, out_img_path, coordinate):
    """
        根据坐标位置剪切图片
    :param img: 原始图片路径
    :param out_img_name: 剪切输出图片路径(str)
    :param coordinate: 原始图片上的坐标(tuple) egg:(x, y, w, h) ---> x,y为矩形左上角坐标, w,h为右下角坐标
    :return:
    """
    image = Image.open(in_image_path)
    region = image.crop(coordinate)
    # region = ImageEnhance.Contrast(region).enhance(1.0)
    region.save(out_img_path)
    return region

# 图片转文字
def ocr_image(img):
    text = pytesseract.image_to_string(img)
    return text
