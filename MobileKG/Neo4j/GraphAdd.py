from py2neo import Graph, Node, Relationship, NodeMatcher
from MobileKG.Neo4j.GraphSearch import GraphSearch
import json


class GraphAdd:
    # Graph database connection
    graph = Graph('http://localhost:7474', auth=('neo4j', 'neo4j'))
    current_scene=''

    @classmethod
    def record_create(cls, cypher):
        # Record the created cypher query to a JSON file for tracking
        file=open('../Test/front_end/GraphAddRecord.json','r',encoding='utf-8')
        content=json.loads(file.read())
        file.close()
        if GraphAdd.current_scene in content.keys():
            content[GraphAdd.current_scene].append(cypher)
        else:
            content[GraphAdd.current_scene]=[cypher]
        file=open('../Test/front_end/GraphAddRecord.json','w',encoding='utf-8')
        file.write(json.dumps(content))
        file.close()
        return

    @classmethod
    def create_widget(cls, widget):
        if GraphSearch.get_widget(widget.id) is not None:
            return
        cypher = 'create (w:Widget ' + widget.get_str() + ')'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_widgets(cls, widgets):
        for w in widgets:
            GraphAdd.create_widget(widgets[w])
        return

    @classmethod
    def create_opt(cls, opt):
        if GraphSearch.get_opt(opt.id) is not None:
            return
        cypher = 'create (o:Operation ' + opt.get_str() + ')'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_opts(cls, opts):
        for o in opts:
            GraphAdd.create_opt(opts[o])
        return

    @classmethod
    def create_ocr(cls, ocr):
        if GraphSearch.get_ocr(ocr.id) is not None:
            return
        cypher = 'create (o:OCRText ' + ocr.get_str() + ')'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_ocrs(cls, ocrs):
        for o in ocrs:
            GraphAdd.create_ocr(o)
        return

    @classmethod
    def create_ocr_ocr(cls, ocr1, ocr2):
        if ocr1 is None or ocr2 is None:
            return
        if GraphSearch.exist_ocr_ocr(ocr1.id, ocr2.id):
            return
        cypher = 'match (o1:OCRText) where o1.id=' + str(
            ocr1.id) + '\n' + 'match (o2:OCRText) where o2.id=' + str(
            ocr2.id) + '\n' + 'create (o1)-[r1:OCR_REL{relation:"相似"}]->(o2)' + '\n' + 'create (o2)-[r2:OCR_REL{relation:"相似"}]->(o1)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_cnt_sim_cnt(cls, cnt1, cnt2):
        if cnt1 is None or cnt2 is None:
            return
        cypher = 'match (cnt1:Content) where cnt1.id=' + str(
            cnt1.id) + '\n' + 'match (cnt2:Content) where cnt2.id=' + str(
            cnt2.id) + '\n' + 'create (cnt1)-[r1:CNT_REL{relation:"相似"}]->(cnt2)' + '\n' + 'create (cnt2)-[r2:CNT_REL{relation:"相似"}]->(cnt1)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_cnt_opt(cls, cnt, opt):
        if cnt is None or opt is None:
            return
        cypher = 'match (cnt:Content) where cnt.id=' + str(
            cnt.id) + '\n' + 'match (opt:Operation) where opt.id=' + str(
            opt.id) + '\n' + 'create (cnt)-[r:CNT_OPT_REL{relation:"操作"}]->(opt)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_cnt_wdg(cls, cnt, wdg):
        if cnt is None or wdg is None:
            return
        cypher = 'match (cnt:Content) where cnt.id=' + str(
            cnt.id) + '\n' + 'match (wdg:Widget) where wdg.id=' + str(
            wdg.id) + '\n' + 'create (cnt)-[r:CNT_WID_REL{relation:"控件"}]->(wdg)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_cnt_ocr(cls, cnt, ocr):
        if cnt is None or ocr is None:
            return
        cypher = 'match (cnt:Content) where cnt.id=' + str(
            cnt.id) + '\n' + 'match (ocr:OCRText) where ocr.id=' + str(
            ocr.id) + '\n' + 'create (cnt)-[r:CNT_OCR_REL{relation:"文本"}]->(ocr)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def create_cnt_lay(cls, cnt, lay):
        return

    @classmethod
    def create_cnt_next_cnt(cls, cnt1, cnt2):
        if cnt1 is None or cnt2 is None:
            return
        if GraphSearch.exist_cnt_next_cnt(cnt1.id,cnt2.id):
            return
        cypher = 'match (cnt1:Content) where cnt1.id=' + str(
            cnt1.id) + '\n' + 'match (cnt2:Content) where cnt2.id=' + str(
            cnt2.id) + '\n' + 'create (cnt1)-[r1:CNT_REL{relation:"后继"}]->(cnt2)' + '\n' + 'create (cnt2)-[r2:CNT_REL{relation:"前继"}]->(cnt1)'
        GraphAdd.graph.run(cypher)
        print('Graph Add: '+cypher)
        GraphAdd.record_create(cypher)
        return

    @classmethod
    def add_new_content(cls, cnt):
        if cnt is None:
            return
        cypher1 = 'create (c:Content ' + cnt.get_str() + ')'
        GraphAdd.graph.run(cypher1)
        print('Graph Add: ' + cypher1)
        GraphAdd.record_create(cypher1)
        GraphAdd.create_cnt_opt(cnt, cnt.opt)
        GraphAdd.create_cnt_wdg(cnt, cnt.widget)
        GraphAdd.create_cnt_ocr(cnt, cnt.ocr)
        return

    @classmethod
    def tag_cnt_head(cls,cnt):
        if cnt is None:
            return
        cypher1='match (a:Content) where a.id='+str(cnt.id)+' set a.head="True"';
        GraphAdd.graph.run(cypher1)
        print('Graph Add: '+cypher1)
        GraphAdd.record_create(cypher1)
        return

    @classmethod
    def tag_cnt_tail(cls,cnt):
        if cnt is None:
            return
        cypher1='match (a:Content) where a.id='+str(cnt.id)+' set a.tail="True"';
        GraphAdd.graph.run(cypher1)
        print('Graph Add: '+cypher1)
        GraphAdd.record_create(cypher1)
        return
