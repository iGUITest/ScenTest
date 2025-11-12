import os
import json
from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.GenerateKG.po.OCRTex import OCRTex
from MobileKG.GenerateKG.po.Layout import Layout
from MobileKG.GenerateKG.operation.MessageCompare import MessageCompare
from MobileKG.WidAnalysis.WidAnalysis import get_classification
import cv2 as cv


class TextPicBound:
    def __init__(self, opts, widgets, opt_sim, input_sim, ocr_sim, result_path, time, exist_path):
        self.__widgets = widgets
        self.__opts = opts
        self.__ocr_sim = ocr_sim
        self.__opt_sim = opt_sim
        self.__input_sim = input_sim
        self.__result_path = result_path
        self.__time = time
        self.__exist_path = exist_path
        return

    def get_opts(self):
        return self.__opts

    def get_widgets(self):
        return self.__widgets

    def get_operation(self, scene_txt):
        opt_txt = scene_txt[0]
        opt = None
        try:
            opt = self.__opts[opt_txt]
        except KeyError as e:
            for o in self.__opts:
                if MessageCompare.txt_sim(o, opt_txt) >= self.__opt_sim:
                    opt = self.__opts[o]
                    break
            if opt is None:
                opt = Opt(len(self.__opts) + 1, opt_txt, '')
                self.__opts[opt_txt] = opt
        return opt

    def get_cnt(self, scene_txt):
        cnt = scene_txt[1]
        return cnt

    def get_widget(self, scene_pic, step, cnt_ocr_match, opt):
        com_file = open(scene_pic + '/component/' + step + '.json', 'r', encoding='utf-8')
        com_cnts = json.loads(com_file.read())['components']
        com_file.close()
        square, horizontal, vertical, center = 0, 0, 0, 0
        com_ocr_match = None
        if cnt_ocr_match is not None:
            for com_cnt in com_cnts:
                s, h, v, c = self.__find_relevant(
                    com_cnt['x1'], com_cnt['y1'], com_cnt['x2'], com_cnt['y2'],
                    cnt_ocr_match['location']['left'], cnt_ocr_match['location']['top'],
                    cnt_ocr_match['location']['left'] + cnt_ocr_match['location']['width'],
                    cnt_ocr_match['location']['top'] + cnt_ocr_match['location']['height']
                )
                if s > square:
                    square, horizontal, vertical, center = s, h, v, c
                    com_ocr_match = com_cnt
        widget = None
        if MessageCompare.txt_sim(opt.name, '输入') > self.__input_sim:
            widget = self.__widgets.get('EditText')
        elif com_ocr_match is not None:
            pic = cv.imread(scene_pic + '/component/result.jpg')
            classification = get_classification(
                pic[com_ocr_match['y1']:com_ocr_match['y2'], com_ocr_match['x1']:com_ocr_match['x2']])
            widget = self.__widgets.get(classification)
        return widget

    def get_layout(self):
        layout = Layout()
        return layout

    def get_ocr(self, scene_pic, cnt, step):
        ocr_file = open(scene_pic + '/ocr/' + step + '.json', 'r', encoding='utf-8')
        ocr_texts = json.loads(ocr_file.read())
        ocr_file.close()
        cnt_ocr_similarity = 0
        cnt_ocr_match = None
        for ocr_text in ocr_texts['words_result']:
            sim = MessageCompare.txt_sim(cnt, ocr_text['words'])
            if sim > cnt_ocr_similarity:
                cnt_ocr_similarity = sim
                cnt_ocr_match = ocr_text
        similar_ocr_objects = []
        same_ocr_object = None
        ocr = None
        stored_ocrs = self.__get_stored_ocrs()
        if cnt_ocr_match is not None:
            for ocr_object in stored_ocrs:
                if ocr_object.name == cnt_ocr_match['words']:
                    same_ocr_object = ocr_object
                    break
                sim = MessageCompare.txt_sim(ocr_object.name, cnt_ocr_match['words'])
                if sim >= self.__ocr_sim:
                    similar_ocr_objects.append(ocr_object)
            if same_ocr_object is None:
                ocr = OCRTex(len(stored_ocrs) + 1, cnt_ocr_match['words'], similar_ocr_objects)
                self.__save_ocr_to_stored_ocrs(ocr, stored_ocrs)
            else:
                ocr = same_ocr_object
        return cnt_ocr_match, ocr

    def __find_relevant(self, x1, y1, x2, y2, x3, y3, x4, y4):
        class rect:
            def __init__(self, x1, y1, x2, y2):
                self.x1 = x1
                self.x2 = x2
                self.y1 = y1
                self.y2 = y2
                return

        left = None
        right = None
        square = 0
        if x1 <= x3:
            left = rect(x1, y1, x2, y2)
            right = rect(x3, y3, x4, y4)
        else:
            right = rect(x1, y1, x2, y2)
            left = rect(x3, y3, x4, y4)

        if left.x2 < right.x1:
            square = 0
        elif left.y2 < right.y1 or left.y1 > right.y2:
            square = 0
        else:
            x_lu = max(left.x1, right.x1)
            y_lu = max(left.y1, right.y1)
            x_rd = min(left.x2, right.x2)
            y_rd = min(left.y2, right.y2)
            square = (x_rd - x_lu) * (y_rd - y_lu)

        return square, min(abs(x3 - x2), abs(x1 - x4)), min(abs(y3 - y2), abs(y1 - y4)), pow(
            pow(x3 + x4 - x1 - x2, 2) + pow(y3 + y4 - y1 - y2, 2), 0.5) / 2

    def __create_dir(self, path):
        if os.path.exists(path):
            return
        os.mkdir(path)
        return

    def __get_stored_ocrs(self):
        path = ''
        if self.__exist_path is not None:
            path = self.__exist_path + '/ocrs.json'
        else:
            path = self.__result_path + self.__time + '/ocrs.json'

        result = []
        if os.path.exists(path):
            file = open(path, 'r', encoding='utf-8')
            stored_ocrs = json.loads(file.read())
            for item in stored_ocrs:
                temp = OCRTex(1, None, None)
                temp.from_dic(item)
                result.append(temp)
            file.close()
        else:
            dir_path = self.__result_path + self.__time
            self.__create_dir(dir_path)
            file = open(path, 'w', encoding='utf-8')
            file.close()
        return result

    def __save_ocr_to_stored_ocrs(self, ocr: OCRTex, stored_ocrs):
        stored_ocrs.append(ocr)
        result = []
        for item in stored_ocrs:
            result.append(item.to_dic())
        path = ''
        if self.__exist_path is not None:
            path = self.__exist_path + '/ocrs.json'
        else:
            path = self.__result_path + self.__time + '/ocrs.json'
        file = open(path, 'w', encoding='utf-8')
        file.write(json.dumps(result, ensure_ascii=False))
        file.close()
        return
