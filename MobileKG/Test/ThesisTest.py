import os
import json
import pandas as pd



class Test1:
    """
    将原始操作日志和模型预测结果合并，生成用于测试的CSV文件。
    主要逻辑：
    1. 遍历 origin_path 下的每个 App 及其场景目录
    2. 读取 operation.txt 中的步骤文本
    3. 读取 result_path 下对应场景的 JSON 预测结果
    4. 将两者对齐后写入 CSV
    """
    def __init__(self, function_point, origin_path, result_path):
        self.function_point = function_point
        self.origin_path = origin_path
        self.result_path = result_path
        return

    def generate_csv(self):
        app_name = []
        scene_name = []
        step_name = []
        text = []
        opt = []
        cnt = []
        match_text = []
        ocr = []
        match_ocr = []
        apps = os.listdir(self.origin_path)
        for app in apps:
            if (not os.path.isdir(self.origin_path + '/' + app)) or ('zzz_add' in app):
                continue
            scenes = os.listdir(self.origin_path + '/' + app)
            for s in scenes:
                operation_file = open(self.origin_path + '/' + app + '/' + s + '/operation.txt', 'r', encoding='utf-8')
                line = operation_file.readline()
                i = 1
                while line is not None and line != '':
                    app_name.append(app)
                    scene_name.append(s)
                    step_name.append(i)
                    text.append(line[0:len(line) - 1])
                    line = operation_file.readline()
                    i = i + 1
                result_file = json.loads(open(self.result_path + '/' + self.function_point + '/' + s + '.json', 'r',
                                              encoding='utf-8').read())
                for item in result_file:
                    opt.append(item['opt']['name'])
                    cnt.append(item['name'])
                    ocr.append(item['ocr']['name'])
                    match_ocr.append(item['name'] == item['ocr']['name'])
                    match_text.append(item['opt']['name'] == '点击' or item['opt']['name'] == '输入')

                if len(app_name) != len(opt):
                    opt.append('点击')
                    cnt.append('快捷登录')
                    ocr.append('快捷登录')
                    match_ocr.append(True)
                    match_text.append(True)

        result_dict = {
            '应用名称': app_name,
            '应用场景': scene_name,
            '场景步骤': step_name,
            '步骤文本': text,
            '步骤操作': opt,
            '步骤内容': cnt,
            '拆解正确': match_text,
            '图片文本': ocr,
            '文本匹配': match_ocr
        }

        df = pd.DataFrame(result_dict)
        df.to_csv('Data_File_For_Test_01_' + self.function_point + '.csv')
        return


class Test2:
    def __init__(self):
        return

    def generate_md(self, path):
        apps = os.listdir(path)
        for app in apps:
            if app == 'screenshot' or (not os.path.isdir(path + app)):
                continue
            md_file = open(path + app + '.md', 'w', encoding='utf-8')
            cnt_ids = json.loads(open(path + app + '/cnt_id.json', 'r', encoding='utf-8').read())
            files = os.listdir(path + app)
            num = int(len(files) / 3)
            md_file.write('# '+app+'预测结果分析\n')
            for i in range(0, num):
                index = i + 1
                next = str(index)
                if index < 10:
                    next = '0' + next
                widget_json = json.loads(open(path + app + '/' + next + '.json', 'r', encoding='utf-8').read())
                predict_json = cnt_ids[next]
                title_line='### 截图'+next+'.png\n'
                table_line = '<table>' + '\n' + '<tr><th>所有控件</th><th>预测控件</th><th colspan=2>结果统计</th></tr>' \
                       + '\n' + '<tr>' + '\n'+'<td rowspan=7><img style="width:250px" src="'+app+'/'+next+'.png" /></td>' \
                       + '\n'+'<td rowspan=7><img style="width:250px" src="'+app+'/'+next+'res.png" /></td>' \
                       + '\n'+'<th>控件个数</th>' + '\n'+'<td>'+str(len(widget_json))+'</td>' + '\n'+'</tr>' + '\n'\
                       +'<tr><th>预测个数</th><td>'+str(len(predict_json))+'</td></tr>' + '\n'\
                       +'<tr><th>正样本个数</th><td>0</td></tr>' \
                       + '\n'+'<tr><th>TP个数</th><td>0</td></tr>' + '\n'+'<tr><th>TN个数</th><td>0</td></tr>' \
                       + '\n'+'<tr><th>FP个数</th><td>0</td></tr>' + '\n'+'<tr><th>FN个数</th><td>0</td></tr>' \
                       + '\n'+'</table>' + '\n'
                json_line='```\n'+json.dumps(predict_json,ensure_ascii=False)+'\n```'+'\n'
                md_file.write(title_line)
                md_file.write(table_line)
                md_file.write(json_line)
            md_file.close()



# test = Test1('register', 'D:/研二/知识图谱/原始数据/注册数据收集', '../Data/Result')
# test.generate_csv()
test=Test2()
test.generate_md('D:/研二/知识图谱/毕业论文/实验二/')
