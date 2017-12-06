import Tools
from Node import Node
from Edge import Edge


class Graph:

    round = 0

    def __init__(self):
        self.nodeList = Node.node_list
        self.edgeList = Edge.edge_list

    @staticmethod
    def connect(source, target):
        new_edge = Edge.find_by_source_and_target(source.id, target.id)
        if not new_edge:
            Edge(source.id, target.id)
        else:
            return
        source.add_out_neighbour(target)
        target.add_in_neighbour(source)

    def split(self, node):
        #n = 原点的label长度
        n = len(node.label)
        #迭代
        alive_in_neighbours = list(filter(Tools.end_less_than_0, node.in_neighbours))
        for in_neighbour in alive_in_neighbours:
            #m = 入点的label长度
            m = len(in_neighbour.label)
            #生成新名字
            new_name = "%s%s" % (in_neighbour.label[m-n:m-n+1], node.label)
            #生成新点
            #查看新点是否重复
            if Node.find_node_by_label(new_name):
                new_node = Node.find_node_by_label(new_name)
            else:
                new_node = Node(new_name, start=self.round)
            print("new node is :")
            print(new_node)
            #连接入点和新点
            new_edge = Edge.find_by_source_and_target(in_neighbour.id, new_node)
            if not new_edge:
                new_edge = Edge(in_neighbour.id, new_node.id, start=self.round)
                print("new edge is :")
                print(new_edge)
            if in_neighbour not in new_node.in_neighbours:
                new_node.add_in_neighbour(in_neighbour)
            if new_node not in in_neighbour.in_neighbours:
                in_neighbour.add_out_neighbour(new_node)
            #连接原点的出点和新点
            alive_out_neighbours = list(filter(Tools.end_less_than_0, node.out_neighbours))
            for out_neighbour in alive_out_neighbours:
                new_edge2 = Edge.find_by_source_and_target(new_node.id, out_neighbour.id)
                if not new_edge2:
                    Edge(new_node.id, out_neighbour.id, start=self.round)
                if out_neighbour not in new_node.out_neighbours:
                    new_node.add_out_neighbour(out_neighbour)
                if new_node not in out_neighbour.in_neighbours:
                    out_neighbour.add_in_neighbour(new_node)
        #end原点
        Node.end_node(node, self.round)

    def merge(self, node1, node2):
        new_node = Node(node1.label, start=self.round)
        new_node.logical_nodes.append(node1)
        new_node.logical_nodes.append(node2)
        #求入点并集
        new_node.in_neighbours = list(set(node1.in_neighbours).union(set(node2.in_neighbours)))
        #求出点并集
        new_node.out_neighbours = list(set(node1.out_neighbours).union(set(node2.out_neighbours)))

        Node.end_node(node1, self.round)
        Node.end_node(node2, self.round)
        return new_node

    def round_plus(self):
        self.round += 1

    @staticmethod
    def clear():
        alive_node_list = list(filter(Tools.end_less_than_0, Node.node_list))
        for alive_node in alive_node_list:
            alive_node.in_neighbours = list(filter(Tools.end_less_than_0, alive_node.in_neighbours))
            alive_node.out_neighbours = list(filter(Tools.end_less_than_0, alive_node.out_neighbours))





