import Tools
import random


class Node:

    max_ID = 0
    nodeCount = 0
    node_list = []
    node_alive_list = []

    def __init__(self, label, id=-1, weight=0, start=1, end=-1):
        if id != -1:
            self.id = id
            if Node.max_ID < id:
                Node.max_ID = id
        else:
            self.id = self.max_ID
        self.label = label
        self.weight = weight
        self.start = start
        self.end = end
        self.in_neighbours = []
        self.out_neighbours = []
        self.logical_nodes = []
        Node.node_list.append(self)
        Node.max_ID += 1

    def __str__(self):
        return "id=%d,label=%s,wight=%d,start=%d,end=%d" % (self.id, self.label, self.weight, self.start, self.end)

    def add_in_neighbour(self, in_neighbour):
        self.in_neighbours.append(in_neighbour)

    def add_out_neighbour(self, out_neighbour):
        self.out_neighbours.append(out_neighbour)

    @staticmethod
    def end_node(node, round):
        node.end = round

    @staticmethod
    def is_res_node(node):

        if node.end > 0:
            return False

        for in_neighbour in node.in_neighbours:
            if in_neighbour.end > 0:
                continue
            if len(in_neighbour.label) < len(node.label):
                return False

        for out_neighbour in node.out_neighbours:
            if out_neighbour.end > 0:
                continue
            if len(out_neighbour.label) < len(node.label):
                return False

        return True

    @staticmethod
    def find_sibling_node(node):
        alive_node_list = list(filter(Tools.end_less_than_0_and_can_merge, Node.node_alive_list))
        for alive_node in alive_node_list:
            if alive_node.label != node.label and alive_node.label[1:] == node.label[1:]:
                return alive_node

        return
        '''
        if node.id == 0:
            return
        elif node.id == len(Node.node_list) - 1: #如果是最后一个点
            while True:
                idx = node.id - 1
                if idx < 0 or node.start != Node.node_list[idx].start:
                    return
                if Node.node_list[idx].end < 0:
                    return Node.node_list[idx]

        else:
            #往前查找
            while True:
                idx = node.id - 1
                if idx < 0 or node.start != Node.node_list[idx].start:
                    break
                if Node.node_list[idx].end < 0:
                    return Node.node_list[idx]
                idx -= 1
            #往后查找
            while True:
                idx = node.id + 1
                if idx == len(Node.node_list) or node.start != Node.node_list[idx].start:
                    break
                if Node.node_list[idx].end < 0:
                    return Node.node_list[idx]
                idx += 1
        '''

    @staticmethod
    def find_node_by_label(label):
        for node in Node.node_list:
            if node.end < 0 and node.label == label:
                return node

        return

    @staticmethod
    def find_node_by_id(id):
        for node in Node.node_list:
            if node.id == id:
                return node

        return




