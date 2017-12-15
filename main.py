import csv


from Edge import Edge
from Node import Node
from Graph import Graph
import Tools
import random
from gexf import Gexf

graph = Graph()

while True:
    is_random_mode = str.upper(input("Whether to use random mode or not?([Y]/[N]):"))
    if is_random_mode != 'Y' and is_random_mode != 'N':
        print("Input Error!")
    else:
        break

while True:
    is_csv = input("input [0] import csv file, or input [1] use complete graph: ")
    if is_csv != '0' and is_csv != '1':
        print("Input Error!")
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
        with open(node_file_name, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node_id = int(row['id'])
                node_label = row['label']

                timeset = Tools.timeset_split(row['timeset'], graph)
                node_start = timeset[0]
                node_end = timeset[1]

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
        with open(edge_file_name, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                #if 'Infinity' not in row['timeset']:
                #    continue
                edge_id = int(row['id'])
                edge_source = int(row['Source'])
                edge_target = int(row['Target'])

                timeset = Tools.timeset_split(row['timeset'], graph)
                edge_start = timeset[0]
                edge_end = timeset[1]

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

    k = int(input("Input the number of nodes:"))

    graph.create_complete_graph(k)

join_times = int(input("join times:"))
leave_times = int(input("leave times:"))

graph.round_plus()

#graph.merge(graph.nodeList[3], graph.nodeList[4])
print("---")
if is_random_mode == "Y":
    for i in range(join_times):

        print("Now join times：" + str(i+1))

        while True:
            random_node = random.choice(Node.node_alive_list)
            print(random_node)

            if Node.is_res_node(random_node):
                break

        graph.round_plus()
        graph.split(random_node)
        #graph.clear()

    print("---")
    graph.round_plus()
    for i in range(leave_times):

        print("Now leave times：" + str(i+1))

        node_alive_list = list(filter(Tools.node_alive_and_can_be_merged, Node.node_alive_list))

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

elif is_random_mode == "N":
    for i in range(join_times):

        print("Now join times：" + str(i + 1))

        node_alive_list = [x for x in Node.node_list if x.end < 0]

        while True:
            node_id = int(input("Please input node's id:"))
            split_node = Node.find_node_by_id(node_id)
            if split_node:
                if split_node.end < 0:
                    if Node.is_res_node(split_node):
                        graph.round_plus()
                        graph.split(split_node)
                        break
                    else:
                        print("Not Res-Node")
                else:
                    print("Not Alive")
            else:
                print("No such node")

        # graph.clear()

    print("---")
    graph.round_plus()

    for i in range(leave_times):

        print("Now leave times：" + str(i+1))

        node_alive_list = list(filter(Tools.node_alive_and_can_be_merged, Node.node_list))

        while True:
            node_one_id = int(input("Please input first node's id:"))
            node_one = Node.find_node_by_id(node_one_id)
            if (not node_one) or node_one not in node_alive_list:
                print("No Such Node or Not Alive Node")
                continue
            node_two_id = int(input("Please input second node's id:"))
            node_two = Node.find_node_by_id(node_two_id)

            if (not node_two) or node_two not in node_alive_list:
                print("No Such Node or Not Alive Node")
                continue
            if node_one.label[1:] != node_two.label[1:]:
                print("Not Sibling Nodes")
                continue

            new_node = graph.merge(node_one, node_two)

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
        tmp.addAttribute(atr1, str(node.weight))

        if node.logical_nodes:
            logical = "%d %d" % (node.logical_nodes[0].id, node.logical_nodes[1].id)
            tmp.addAttribute(atr2, logical)

    else:
        tmp = gephi_graph.addNode(id=str(node.id),
                            label=node.label,
                            start=str(node.start))

        tmp.addAttribute(atr1, str(node.weight))

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

output_file_name = input("Please input file name:") + '.gexf'
output_file = open(output_file_name, "wb")
gexf.write(output_file)


#Tools.end_program()