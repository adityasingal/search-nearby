class BinarySearchTreeNode():
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
        self.is_leaf = False
        self.yroot = None          # y subtree rooted at that node
        self.left_list = []        # list of all points in left subtree
        self.right_list =[]        # list of all points in right subtree

# sorts list accoring to required dimension eg - x or y
def sorter(coords,dim):
    l=[]
    if dim==1:
        for i in coords:
            l.append(i[::-1])
        l.sort()
        c=[]
        for i in l:
            c.append(i[::-1])
        return c
    else:
        coords.sort()
    return coords

# makes range tree of one dimension 
def Make1DRangeTree(coords,dim):
    coords = sorter(coords,dim)
    if len(coords) == 0:
        return None
    elif len(coords) == 1:
        n = BinarySearchTreeNode(coords[0])
        n.left_list = [coords[0]]
        n.right_list = [coords[0]]
        n.is_leaf = True
    else:
        if len(coords)%2 != 0:
            median = len(coords)//2
        else:
            median = len(coords)//2-1
        n = BinarySearchTreeNode(coords[median])
        n.left_list = coords[:median+1]
        n.left = Make1DRangeTree(n.left_list,dim)
        n.right_list = coords[median+1:]
        n.right = Make1DRangeTree(n.right_list,dim)
    return n

# makes range tree of two dimensions which is basically a one dimensional range tree 
# with a secondary y subtree rooted at each node
def Make2DRangeTree(coords):
    coords =  sorter(coords,0)
    if len(coords) == 0:
        return None
    elif len(coords) == 1:
        n = BinarySearchTreeNode(coords[0])
        n.yroot = BinarySearchTreeNode(coords[0])
        n.is_leaf = True
        n.yroot.is_leaf = True
    else:
        if len(coords)%2 != 0:
            median = len(coords)//2
        else:
            median = len(coords)//2-1
        n = BinarySearchTreeNode(coords[median])
        n.yroot = Make1DRangeTree(coords,1)
        n.left_list = coords[:median+1]
        n.left = Make2DRangeTree(n.left_list)
        n.right_list = coords[median+1:]
        n.right = Make2DRangeTree(n.right_list)
    return n

# finds the node at which the search for the minimum and maximum splits into two, dim = 0 for x and dim = 1 for y
def split_node(root,min_r,max_r,dim):
    n = root
    while n is not None:
        if n.data[dim] < min_r[dim]:
            n = n.right
        elif n.data[dim] > max_r[dim]:
            n = n.left
        elif min_r[dim] <= n.data[dim] and n.data[dim]<= max_r[dim]:
            return n
    return n

# finds the points in a given range for given dimension, dim = 0 for x and dim = 1 for y
def Query_Search1D(root,min_r,max_r,dim):
    final=[]
    Split = split_node(root,min_r,max_r,dim)
    if Split is None:
        return final
    LeftNode = Split.left
    RightNode = Split.right

    if Split.is_leaf:
        final += [Split.data]

    while LeftNode is not None:
        if LeftNode.data[dim]>=min_r[dim]:
            final += LeftNode.right_list
            LeftNode = LeftNode.left
        else:
            LeftNode = LeftNode.right

    while RightNode is not None:
        if RightNode.data[dim] <= max_r[dim]:
            final += RightNode.left_list
            RightNode = RightNode.right
        else:
            RightNode = RightNode.left

    return final

# finds the points in a given rnage for two dimensions
def Query_Search2D(root,min_r,max_r):
    Split = split_node(root,min_r,max_r,0)
    if Split is None:
        return []
    LeftNode = Split.left
    RightNode = Split.right
    final=[]

    if Split.is_leaf:
        if min_r[1]<= Split.yroot.data[1]<=max_r[1]:
            final+=[Split.data]

    while LeftNode is not None:
        if not LeftNode.is_leaf:
            if LeftNode.data[0]>min_r[0]:
                final += Query_Search1D(LeftNode.right.yroot,min_r,max_r,1)
                LeftNode = LeftNode.left
            else:
                LeftNode = LeftNode.right
        else:
            if min_r[0]<LeftNode.data[0]<max_r[0] and  min_r[1]<LeftNode.data[1]<max_r[1]:
                final += [LeftNode.data]
            LeftNode = None

    while RightNode is not None:
        if not RightNode.is_leaf:
            if RightNode.data[0] < max_r[0]:
                final += Query_Search1D(RightNode.left.yroot,min_r,max_r,1)
                RightNode = RightNode.right
            else:
                RightNode = RightNode.left
        else:
            if min_r[0]<RightNode.data[0]<max_r[0] and  min_r[1]<RightNode.data[1]<max_r[1]:
                final += [RightNode.data]
            RightNode = None
    return final

class PointDatabase():
    def __init__(self,pointlist):
        self.node = Make2DRangeTree(pointlist)

    def searchNearby(self,q,d):
        x_min = q[0] - d
        x_max = q[0] + d
        y_min = q[1] - d
        y_max = q[1] + d
        min_r = (x_min,y_min)
        max_r = (x_max,y_max)
        final = Query_Search2D(self.node,min_r,max_r)
        return final
