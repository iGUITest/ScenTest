import os
import json
from MobileKG.GenerateKG.po.Widget import Widget
from MobileKG.GenerateKG.po.Opt import Opt
from MobileKG.GenerateKG.po.OCRTex import OCRTex
from MobileKG.GenerateKG.po.Content import Content
from MobileKG.GenerateKG.operation.MessageCompare import MessageCompare
from MobileKG.Neo4j.GraphAdd import GraphAdd

class GenerateGraph:
    """
    知识图谱生成器主类
    负责从JSON数据文件生成知识图谱，包含组件、操作、OCR文本和内容节点
    """
    def __init__(self, dir):
        """
        初始化生成器
        
        Args:
            dir: 数据文件目录路径，包含widgets.json, opts.json, ocrs.json等文件
        """
        self.__widgets = {}  # 存储组件对象的字典，key为英文名
        self.__opts = {}     # 存储操作对象的字典，key为操作名
        self.__ocrs: list[OCRTex] = [] # 存储OCR文本对象的列表
        self.__dir = dir     # 数据文件目录
        return

    def execute(self):
         """
        执行知识图谱生成流程
        按顺序生成组件、操作、OCR文本和内容节点
        """
        self.__generate_widget()
        self.__generate_operation()
        self.__generate_ocr()
        self.__generate_cnt()
        return

    def __generate_widget(self):
        """从widgets.json文件生成组件节点并添加到图谱"""
        GraphAdd.current_scene = 'widgets'  # 设置当前场景为组件
        file = open(self.__dir + 'widgets.json', 'r', encoding='utf-8')
        data = json.loads(file.read())  # 读取并解析JSON数据
        self.__widgets = {}
        for wid_dic in data:
            temp = Widget(0, '', '')  # 创建临时组件对象
            temp.from_dic(wid_dic)    # 从字典加载数据
            self.__widgets[temp.english] = temp  # 按英文名存储到字典
        GraphAdd.create_widgets(self.__widgets)  # 在图谱中创建所有组件节点

    def __generate_operation(self):
        """从opts.json文件生成操作节点并添加到图谱"""
        GraphAdd.current_scene = 'opts'
        file = open(self.__dir + 'opts.json', 'r', encoding='utf-8')
        data = json.loads(file.read())
        self.__opts = {}
        for opt_dic in data:
            temp = Opt(0, '', '')
            temp.from_dic(opt_dic)
            self.__opts[temp.name] = temp
        GraphAdd.create_opts(self.__opts)

    def __generate_ocr(self):
        """从ocrs.json文件生成OCR文本节点并建立相似关系"""
        GraphAdd.current_scene = 'ocrs'
        file = open(self.__dir + 'ocrs.json', 'r', encoding='utf-8')
        data = json.loads(file.read())
        self.__ocrs = []
        for ocr_dic in data:
            temp = OCRTex(0, '', [])
            temp.from_dic(ocr_dic)
            self.__ocrs.append(temp)
        GraphAdd.create_ocrs(self.__ocrs)
        for ocr in self.__ocrs:
            for sim in ocr.similar:
                GraphAdd.create_ocr_ocr(ocr, sim)
        return

    def __generate_cnt(self):
         """
        生成内容节点并建立完整的关系链
        处理除widgets.json, opts.json, ocrs.json外的所有场景文件
        """
        scenes = os.listdir(self.__dir)
        cnt_seq = []
        scene_names = []

        # 读取所有场景文件
        for scene in scenes:
            if scene not in ['widgets.json', 'opts.json', 'ocrs.json']:
                scene_names.append(scene)
                file = open(self.__dir + scene, 'r', encoding='utf-8')
                data = json.loads(file.read())
                cnts = []
                for cnt_dic in data:
                    temp = Content(0, '', '', [], None, None, None, None)
                    temp.from_dic(cnt_dic)
                    cnts.append(temp)
                cnt_seq.append(cnts)

        deduplicate = MessageCompare()

        # 处理每个场景的内容序列
        for i in range(0, len(cnt_seq)):
            GraphAdd.current_scene=scene_names[i]
            seq = cnt_seq[i]
            last = None
            for c in seq:
                same, similar = deduplicate.get_similar_cnts(c)
                next = None
                if same is None:
                    GraphAdd.add_new_content(c)
                    for sim in similar:
                        GraphAdd.create_cnt_sim_cnt(c, sim)
                    next = c
                else:
                    self.__update_cnt(c, same)
                    next = same

                if last is not None:
                    GraphAdd.create_cnt_next_cnt(last, next)
                else:
                    GraphAdd.tag_cnt_head(next)

                last = next
            GraphAdd.tag_cnt_tail(last)
        return

    def __update_cnt(self, new_cnt, original_cnt):
         """
        更新内容节点与组件、操作、OCR的关系
        
        Args:
            new_cnt: 新的内容节点
            original_cnt: 已存在的原始内容节点
        """
        # 检查并打印可能的空值情况
        if new_cnt.widget is None or new_cnt.opt is None or new_cnt.ocr is None:
            print(new_cnt.to_dic())

        # 更新操作关系（如果不同）
        if original_cnt.opt is None or original_cnt.opt.id != new_cnt.opt.id:
            GraphAdd.create_cnt_opt(original_cnt, new_cnt.opt)

        # 更新组件关系（如果不同）
        if original_cnt.widget is None or original_cnt.widget.id != new_cnt.widget.id:
            GraphAdd.create_cnt_wdg(original_cnt, new_cnt.widget)

        # 更新OCR关系（如果不同）
        if original_cnt.ocr is None or original_cnt.ocr.id != new_cnt.ocr.id:
            GraphAdd.create_cnt_ocr(original_cnt, new_cnt.ocr)
