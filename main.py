import csv


from Edge import Edge
from Node import Node
from Graph import Graph
import Tools
import random
from gexf import Gexf

graph = Graph()
while True:
    is_csv = input("input [0] import csv file, or input [1] use default graph(K4): ")
    if is_csv != '0' and is_csv != '1':
        print("Please input [0] or [1]")
    else:
        break

if is_csv == '0':
    node_file_name = input("Please input Node filename(No Suffix):") + '.csv'
    '''
    id: row[0]
    label: row[1]
    timeset: row[2]
    weight: row[3]
    '''
    try:
        with open(node_file_name, 'r') as f:  # 采用b的方式处理可以省去很多问题
            reader = csv.DictReader(f)
            for row in reader:
                node_id = int(row['id'])
                node_label = row['label']
                timeset = row['timeset'][2:-2].split(',')
                node_start = int(float(timeset[0]))
                if graph.round < node_start:
                    graph.round = node_start
                if timeset[1] == ' Infinity':
                    node_end = -1
                else:
                    node_end = int(float(timeset[1]))
                    now_round = node_end
                node_weight = int(row['weight'])
                node = Node(id=node_id,
                            label=node_label,
                            start=node_start,
                            end=node_end,
                            weight=node_weight)
                if 'logical_nodes' in row:
                    logical_nodes = row['logical_nodes'].split(' ')
                    node.logical_nodes.append(Node.find_node_by_id(int(logical_nodes[0])))
                    node.logical_nodes.append(Node.find_node_by_id(int(logical_nodes[1])))
    except FileNotFoundError:
        print("No such file:" + node_file_name)
        Tools.end_program()
    except ValueError:
        print("File Mismatch")
        Tools.end_program()



    edge_file_name = input("Please input Edge filename(No Suffix):") + '.csv'
    '''
    Source: row[0]
    Target: row[1]
    timeset: row[5]
    weight: row[6]
    '''
    try:
        with open(edge_file_name, 'r') as f:  # 采用b的方式处理可以省去很多问题
            reader = csv.DictReader(f)
            for row in reader:
                #if 'Infinity' not in row['timeset']:
                #    continue
                edge_id = int(row['id'])
                edge_source = int(row['Source'])
                edge_target = int(row['Target'])
                timeset = row['timeset'][2:-2].split(',')
                edge_start = int(float(timeset[0]))
                if timeset[1] == ' Infinity':
                    edge_end = -1
                else:
                    edge_end = int(float(timeset[1]))
                #edge_weight = float(row['weight'])
                edge = Edge(id=edge_id,
                            source_id=edge_source,
                            target_id=edge_target,
                            start=edge_start,
                            end=edge_end)
    except FileNotFoundError:
        print("No such file:" + edge_file_name)
        Tools.end_program()
    except ValueError:
        print("File Mismatch")
        Tools.end_program()

    for edge in Edge.edge_list:
        if edge.end == -1:
            source = Node.find_node_by_id(edge.source_id)
            target = Node.find_node_by_id(edge.target_id)
            if source.end == -1 and target.end == -1:
                source.out_neighbours.append(target)
                target.in_neighbours.append(source)

else:
    node0 = Node(label='0')
    node1 = Node(label='1')
    node2 = Node(label='2')
    node3 = Node(label='3')

    graph.connect(node0, node1)
    graph.connect(node0, node2)
    graph.connect(node0, node3)
    graph.connect(node1, node0)
    graph.connect(node1, node2)
    graph.connect(node1, node3)
    graph.connect(node2, node0)
    graph.connect(node2, node1)
    graph.connect(node2, node3)
    graph.connect(node3, node0)
    graph.connect(node3, node1)
    graph.connect(node3, node2)

join_times = int(input("join times:"))
leave_times = int(input("leave times:"))

graph.round_plus()

#graph.merge(graph.nodeList[3], graph.nodeList[4])
print("---")
for i in range(join_times):

    print("Now join times：" + str(i))

    node_alive_list = list(filter(Tools.end_less_than_0, Node.node_list))

    while True:
        random_node = random.choice(node_alive_list)
        print(random_node)

        if Node.is_res_node(random_node):
            break

    graph.round_plus()
    graph.split(random_node)
    #graph.clear()

print("---")
graph.round_plus()
for i in range(leave_times):

    print("Now leave times：" + str(i))

    node_alive_list = list(filter(Tools.end_less_than_0_and_not_initializtion, Node.node_list))

    while True:
        random_node = random.choice(node_alive_list)
        print(random_node)
        sibling_node = Node.find_sibling_node(random_node)
        if sibling_node:
            new_node = graph.merge(random_node, sibling_node)
            break

    print("%s's sibling node is ：%s" % (random_node.label, sibling_node.label))
    print("new node is %s,logical nodes is：%s, %s" % (new_node.label, new_node.logical_nodes[0].label, new_node.logical_nodes[1].label))
    graph.round_plus()
    #graph.clear()

print("---")
#for node in Node.node_list:
#    print(node)

#for edge in Edge.edge_list:
#   print(edge)

gexf = Gexf("myc", "DLG")

gephi_graph = gexf.addGraph("directed", "dynamic", "DLG")

atr1 = gephi_graph.addNodeAttribute('weight')
atr2 = gephi_graph.addNodeAttribute('logical', type="string")

for node in Node.node_list:
    if node.end > 0:
        tmp = gephi_graph.addNode(id=str(node.id),
                            label=node.label,
                            start=str(node.start),
                            end=str(node.end))
        tmp.addAttribute(atr1, '1')

        if node.logical_nodes:
            logical = "%d %d" % (node.logical_nodes[0].id, node.logical_nodes[1].id)
            tmp.addAttribute(atr2, logical)

    else:
        tmp = gephi_graph.addNode(id=str(node.id),
                            label=node.label,
                            start=str(node.start))

        tmp.addAttribute(atr1, '1')

        if node.logical_nodes:
            logical = "%d %d" % (node.logical_nodes[0].id, node.logical_nodes[1].id)
            tmp.addAttribute(atr2, logical)

for edge in Edge.edge_list:
    if edge.end > 0:
        gephi_graph.addEdge(id=str(edge.id),
                            source=str(edge.source_id),
                            target=str(edge.target_id),
                            start=str(edge.start),
                            end=str(edge.end))
    else:
        gephi_graph.addEdge(id=str(edge.id),
                            source=str(edge.source_id),
                            target=str(edge.target_id),
                            start=str(edge.start))
print(Edge.max_ID)

output_file_name = input("Please input file name:") + '.gexf'
output_file = open(output_file_name, "wb")
gexf.write(output_file)


Tools.end_program()