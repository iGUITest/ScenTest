import os
import json

from MobileKG.PicAnalysis.utils.Strategy import *
import cv2 as cv
from MobileKG.PicAnalysis.utils.tools import draw_rectangle_show_save, clean_dir
from MobileKG.WidAnalysis import WidAnalysis


class ExtractPic:
    def __init__(self, config, enum):
        self.C = config
        self.option = enum

    def init(self):
        clean_dir(self.C.OUTPUT_PATH)

    def component_extract(self, image_path):
        component_algorithm = get_component_algorithm(self.C)
        text_algorithm = get_text_algorithm(self.C)
        merge_algorithm = get_merge_algorithm(self.C)
        component_bboxs = component_algorithm(self.C, image_path)
        text_bboxes = text_algorithm(self.C, image_path)
        res_bbox = merge_algorithm(component_bboxs, text_bboxes)
        return res_bbox

    def run_widget_ext(self, image_path, output_path):
        self.init()
        image = cv.imread(image_path)
        res_bbox = self.component_extract(image_path)
        draw_rectangle_show_save(image, res_bbox, output_path)
        return

    def generate_widget_info(self, image_path):
        self.init()
        image = cv.imread(image_path)
        res_bbox = self.component_extract(image_path)
        output_path = image_path.replace('origin', 'widget_res')
        output_path = output_path.replace('jpg', 'png')
        draw_rectangle_show_save(image, res_bbox, output_path)
        res_path = image_path.replace('origin', 'widget_res')
        res_path = res_path[:res_path.rindex('/')]
        name = image_path.split('/')[-1][:-4] + '.json'
        if not os.path.exists(res_path):
            os.mkdir(res_path)
        res = []
        for bbox in res_bbox:
            res_i = {}
            x1, y1, x2, y2 = bbox.get_coordinates()
            res_i['x1'] = x1
            res_i['y1'] = y1
            res_i['x2'] = x2
            res_i['y2'] = y2
            component = image[y1:y2, x1:x2]
            res_i["category"] = WidAnalysis.get_classification(component)
            res_i["ocr"] = bbox.get_ocr_text()
            res.append(res_i)
        res_file = open(res_path + '/' + name, mode='w', encoding='utf-8')
        res_file.write(json.dumps(res, ensure_ascii=False, indent=4))
        res_file.close()
        return {"components": res}
