import queue as queue
from graph import graph
from models import TradeItem, IndividualTrades, TradeItemForm, TradeSequence


class bfs:

    # Graph: V(), adj(v) (list of adjacents)
    # 
    def __init__(self, pid):
        # G is a graph and s is an integer for nodes.
        # calculate the number of nodes
        num_nodes = TradeItem.objects.count()
        self.marked = [False] * num_nodes
        self.edgeTo = [0] * num_nodes
        self.s = s
        self.bfsearch(s)

    def bfsearch(self, s):
        q = queue.Queue()
        self.marked[s] = True
        q.put(s)
        while not q.empty():
            print('another round')
            v = q.get()
            t_item = TradeItem.objects.get(id=v)
            t = IndividualTrades.objects.filter(askerItem=t_item)
            for node_item in t:
                w = node_item.id
                print(w)
                if not self.marked[w]:
                    self.edgeTo[w] = v
                    self.marked[w] = True
                    q.put(w)

    def hasPathTo(self, v):
        return self.marked[v]

b = bfs(15)
print(b.hasPathTo(2))
c = bfs(g,1)
print(c.hasPathTo(2))
