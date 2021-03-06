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
        if node.weight == 1:
            return self.weight_is_1_split(node)
        else:
            return self.weight_not_1_split(node)

    def weight_is_1_split(self, node):
        #n : length of node
        new_node_list = []
        n = len(node.label)
        alive_in_neighbours = [x for x in node.in_neighbours if x.end < 0]
        for in_neighbour in alive_in_neighbours:
            #m : length of inneighbour
            m = len(in_neighbour.label)
            #create new name
            new_name = "%s%s" % (in_neighbour.label[m-n:m-n+1], node.label)
            #create new node
            #Is new node repeat
            new_node = Node.find_node_by_label(new_name)
            if new_node is not None:
                print("Node is existed:")
                print(new_node)
            else:
                new_node = Node(new_name, start=self.round)
                print("New node is :")
                print(new_node)
            #connect innei and new node
            new_edge = Edge.find_by_source_and_target(in_neighbour.id, new_node)
            if new_edge is None:
                new_edge = Edge(in_neighbour.id, new_node.id, start=self.round)
                #print("new edge is :")
                #print(new_edge)
            if in_neighbour not in new_node.in_neighbours:
                new_node.add_in_neighbour(in_neighbour)
            if new_node not in in_neighbour.in_neighbours:
                in_neighbour.add_out_neighbour(new_node)
            #connect outnei and new node
            alive_out_neighbours = [x for x in node.out_neighbours if x.end < 0]
            for out_neighbour in alive_out_neighbours:
                new_edge2 = Edge.find_by_source_and_target(new_node.id, out_neighbour.id)
                if new_edge2 is None:
                    Edge(new_node.id, out_neighbour.id, start=self.round)
                if out_neighbour not in new_node.out_neighbours:
                    new_node.add_out_neighbour(out_neighbour)
                if new_node not in out_neighbour.in_neighbours:
                    out_neighbour.add_in_neighbour(new_node)
            new_node_list.append(new_node)
        #set the value of original node's end to now round
        Node.end_node(node, self.round)
        return new_node_list

    def weight_not_1_split(self, node):
        new_node_list = []
        node_alive_out_neighbours = [x for x in node.out_neighbours if x.end < 0]
        node_alive_in_neighbours = [x for x in node.in_neighbours if x.end < 0]
        for logical_node in node.logical_nodes:
            new_node = Node(label=logical_node.label,
                            weight=logical_node.weight,
                            start=self.round)
            new_node.out_neighbours.extend(node_alive_out_neighbours)
            new_node.logical_nodes.extend(logical_node.logical_nodes)
            sub_logical_nodes = []
            def preorder(n):
                sub_logical_nodes.append(n.label[:-1])
                if n.weight > 1:
                    preorder(n.logical_nodes[0])
                    preorder(n.logical_nodes[1])
            preorder(new_node)
            if sub_logical_nodes:
                label_length = len(sub_logical_nodes[0])
            for in_neighbour in node_alive_in_neighbours:
                if in_neighbour.label[-label_length:] in sub_logical_nodes:
                    new_edge = Edge.find_by_source_and_target(in_neighbour.id, new_node.id)
                    if not new_edge:
                        Edge(in_neighbour.id, new_node.id, start=self.round)
                    if in_neighbour not in new_node.in_neighbour:
                        new_node.add_in_neighbour(in_neighbour)
                    if new_node not in in_neighbour.out_neighbours:
                        in_neighbour.add_out_neighbour(new_node)
            for out_neighbour in new_node.out_neighbours:
                new_edge = Edge.find_by_source_and_target(new_node.id, out_neighbour.id)
                if not new_edge:
                    Edge(new_node.id, out_neighbour.id, start=self.round)
                if out_neighbour not in new_node.out_neighbours:
                    new_node.add_out_neighbour(out_neighbour)
                if new_node not in out_neighbour.in_neighbours:
                    out_neighbour.add_in_neighbour(new_node)
            new_node_list.append(new_node)
        Node.end_node(node, self.round)
        return new_node_list

    def merge(self, node1, node2):

        new_node_weight = node1.weight + node2.weight
        new_node = Node(node1.label, start=self.round, weight=new_node_weight)
        new_node.logical_nodes.append(node1)
        new_node.logical_nodes.append(node2)
        #求入点并集
        new_node.in_neighbours = list(set(node1.in_neighbours).union(set(node2.in_neighbours)))
        #求出点并集
        new_node.out_neighbours = list(set(node1.out_neighbours).union(set(node2.out_neighbours)))

        Node.end_node(node1, self.round)
        Node.end_node(node2, self.round)
        if not Node.find_sibling_node(new_node):
            new_node.label = new_node.label[1:]
            new_node.weight = 1
        return new_node

    def round_plus(self):
        Node.node_alive_list = [x for x in Node.node_list if x.end < 0]
        self.round += 1

    @staticmethod
    def clear():
        alive_node_list = [x for x in Node.node_list if x.end < 0]
        for alive_node in alive_node_list:
            alive_node.in_neighbours = [x for x in alive_node.in_neighbours if x.end < 0]
            alive_node.out_neighbours = [x for x in alive_node.out_neighbours if x.end < 0]

    def create_complete_graph(self, k):
        for i in range(1, k+1):
            Node(label=str(i))

        for node in Node.node_list:
            test_list = list(set(Node.node_list) - set([node]))
            for another_node in test_list:
                self.connect(node, another_node)





