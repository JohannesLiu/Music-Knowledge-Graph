from py2neo import Graph
graph = Graph(
    "http://192.168.2.130:7476",
    # database="academic-knowledge-graph",
    username="neo4j",
    password="Kddir@123456&"
)
CA_LIST = {"Track":0,"Genre":1,"Album":2, "Album Type": 3, "Artist":4}
similar_words = {
    "作者":"Authorof",
    "子流派":"sub_genre",
    "包含":"Contain",
    "类型":"Typeof"
}
