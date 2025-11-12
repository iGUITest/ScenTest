import os
import cv2
from MobileKG.LayoutAnalysis.LayoutExtract import *
from MobileKG.PicAnalysis.utils.tools import draw_rectangle_show_save
from MobileKG.PicAnalysis.utils.Bbox import Bbox

"""
add exolanataion
"""
def create_dir(path):
    if os.path.exists(path):
        return
    os.mkdir(path)
    return


def draw_layout_pic(image_path):
    create_dir('test_draw')
    create_dir('test_draw/layout')
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    groups = layout(canny_ocr.extract(image_path), (w, h))
    for g in groups:
        cv2.rectangle(image, (0, g[1]), (w, g[2]), (0, 0, 255), 3)
        # for row in g[0]:
        #     for col in row[0]:
        #         cv2.rectangle(image,(col[0],row[1]),(col[1],row[2]),(0, 0, 255), 3)
    name_index = image_path.rfind('/')
    name = ''
    if name_index == -1:
        name = image_path
    else:
        name = image_path[name_index + 1:]
    print(name)
    cv2.imwrite('./test_draw/layout/' + name, image)


def draw_com_ocr_bbox(json_path, pic_path):
    create_dir('test_draw')
    create_dir('test_draw/czf')
    image = cv2.imread(pic_path)
    com_ocr = json.loads(open(json_path, 'r', encoding='utf-8').read())
    for c_o in com_ocr:
        cv2.rectangle(image, (c_o['x1'], c_o['y1']), (c_o['x2'], c_o['y2']), (0, 0, 255), 1)
    cv2.imwrite('./test_draw/czf/01.jpg', image)


def draw_kg_result(image_path, res, path):
    create_dir('test_draw')
    create_dir('test_draw/kg_result')
    bboxs = []
    for data in res['data']:
        bboxs.append(Bbox(data['x1'], data['y1'], data['x2'], data['y2']))
    pic = cv2.imread(image_path)
    draw_rectangle_show_save(pic, bboxs, path)


def clip(image_path, num, image_index):
    create_dir('test_draw')
    create_dir('test_draw/clip')
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    groups = layout(canny_ocr.extract(image_path), (w, h))
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for i in range(0, len(groups)):
        if i == num - 1:
            g = groups[i]
            x1 = 0
            x2 = w
            y1 = g[1]
            y2 = g[2]
            break
    copped = image[y1:y2, x1:x2]

    name_index = image_path.rfind('/')
    name = ''
    if name_index == -1:
        name = image_path
    else:
        name = image_path[name_index + 1:]
    cv2.imwrite('./test_draw/clip/email-' + image_index + '.png', copped)

draw_com_ocr_bbox('email/test07.json', 'email/test07.jpg')

# kg_result={'status': 'success', 'data': [{'category': 'TextView', 'ocr': '收件人：nandodu@163.com', 'operation': '输入', 'cnt': '收件人', 'cnt_id': 3, 'x1': 46, 'y1': 382, 'x2': 623, 'y2': 425, 'state': 'M'}, {'category': 'ImageButton', 'ocr': '主题：', 'operation': '点击', 'cnt': '主题输入框', 'cnt_id': 4, 'x1': 46, 'y1': 521, 'x2': 149, 'y2': 565, 'state': 'M'}]}
#
# draw_kg_result('email/test06.jpg',kg_result, './test_draw/kg_result/01.jpg')

#draw_layout_pic('login/alipay_login/screenshots/alipay3.jpg')
