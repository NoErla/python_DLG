class Edge:

    max_ID = 0
    edge_list = []

    def __init__(self, source_id, target_id, id=-1, start=1, end=-1):
        if id != -1:
            self.id = id
            if Edge.max_ID < id:
                Edge.max_ID = id
        else:
            self.id = self.max_ID
        self.source_id = source_id
        self.target_id = target_id
        self.start = start
        self.end = end
        Edge.edge_list.append(self)
        Edge.max_ID += 1

    def __str__(self):
        return "source: %d, target: %d"%(self.source_id, self.target_id)

    @staticmethod
    def find_by_source_and_target(source_id, target_id):
        for edge in Edge.edge_list:
            if edge.source_id == source_id and edge.target_id == target_id:
                return edge
        return

    #def end_edge(self,source):





