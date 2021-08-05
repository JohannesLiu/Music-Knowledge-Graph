from neo_db.config import graph, CA_LIST, similar_words
from spider.show_profile import get_profile
import codecs
import os
import json
import base64


def query(name):
    data = graph.run(
        "match(p )-[r]->(n:Person) where n.name=~'(?i)%s'  return  p.name,r.relation,n.name, labels(p), labels(n) \
            Union all\
        match(p:Person) -[r]->(n) where p.name=~'(?i)%s' return p.name, r.relation, n.name, labels(p), labels(n) " % (name, name)
    )
    data = list(data)
    return get_json_data(data)

def query_random():
    data = graph.run(
        "match(p:Track )-[r]->(n:Genre)  return  p.name,r.relation,n.name, labels(p), labels(n) limit 25 \
            Union all\
        match(p:Genre )-[r]->(n:Genre)  return  p.name,r.relation,n.name, labels(p), labels(n) limit 25 \
                Union all\
        match(p:Artist) -[r]->(n:Track) return p.name, r.relation, n.name, labels(p), labels(n) limit 25\
            Union all\
        match(p:Album) -[r]->(n:Track) return p.name, r.relation, n.name, labels(p), labels(n) limit 25"
    )
    data = list(data)
    return get_json_data(data)

def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "_" + i['labels(p)'])
        d.append(i['n.Name'] + "_" + i['labels(n)'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)


# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
def get_KGQA_answer(array):
    data_array = []
    for i in range(len(array) - 2):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.name']

        data = graph.run(
            "match(p)-[r:%s{relation: '%s'}]->(n:Person{name:'%s'}) return  p.name,n.name,r.relation,p.cate,n.cate" % (
                similar_words[array[i + 1]], similar_words[array[i + 1]], name)
        )

        data = list(data)
        print(data)
        data_array.extend(data)

        print("===" * 36)
    with open("./spider/images/" + "%s.jpg" % (str(data_array[-1]['p.name'])), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)

    return [get_json_data(data_array), get_profile(str(data_array[-1]['p.name'])), b.split("'")[1]]


def get_answer_profile(name):
    with open("./spider/images/" + "%s.jpg" % (str(name)), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]




