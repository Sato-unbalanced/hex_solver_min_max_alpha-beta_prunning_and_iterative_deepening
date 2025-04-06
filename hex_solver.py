
from termcolor import colored
class Node:
    def __init__(self ,x_cord = 0 , y_cord = 0, node_value = 0,level = 0):
        self._node_value = node_value
        self._x_cord = x_cord
        self._y_cord = y_cord
        self._level = level

    def get_value(self):
        return self._node_value
    def get_nodes(self):
        return [self._T1,self._T2, self._S1,self._B1,self._B2,self._S2,]
    def get_cords(self):
        return self._x_cord , self._y_cord
    def set_value(self, value):
        self._node_value = value 
    def set_child(self):
        self._T1 = Node(self._x_cord  ,self._y_cord -1, self._node_value + 1,self._level +1)
        self._T2 = Node(self._x_cord + 1,self._y_cord -1,self._node_value + 1,self._level +1)
        self._S1 = Node(self._x_cord + 1,self._y_cord,self._node_value,self._level +1)
        self._B1 = Node(self._x_cord ,self._y_cord +1 ,self._node_value + 1,self._level +1)
        self._B2 = Node(self._x_cord - 1,self._y_cord + 1,self._node_value + 1,self._level +1)
        self._S2 = Node(self._x_cord -1,self._y_cord,self._node_value,self._level +1)
    def cords_in_bound(self):
        return (self._x_cord >=0 and self._x_cord <= 4) and (self._y_cord >=0 and self._y_cord <= 4)
    def get_child_node(self, hex_state):
        if self._T1.get_value() == self.get_value() and self._T1.cords_in_bound() and valid_move(self._T1 , hex_state):
            return self._T1.get_cords()
        if self._T2.get_value() == self.get_value() and self._T2.cords_in_bound() and valid_move(self._T2, hex_state):
            return self._T2.get_cords()
        if self._S1.get_value() == self.get_value() and self._S1.cords_in_bound() and valid_move(self._S1 , hex_state):
            return self._S1.get_cords()
        if self._B1.get_value() == self.get_value() and self._B1.cords_in_bound() and valid_move(self._B1 , hex_state):
            return self._B1.get_cords()
        if self._B2.get_value() == self.get_value() and self._B2.cords_in_bound() and valid_move(self._B2 , hex_state):
            return self._B2.get_cords()
        if self._S2.get_value() == self.get_value() and self._S2.cords_in_bound() and valid_move(self._S2 , hex_state):
            return self._S2.get_cords()
    def get_child_values(self):
        print("value for t1: ",self._T1.get_value())
        print("value for t2: ",self._T2.get_value())
        print("value for s1: ",self._S1.get_value())
        print("value for b1: ",self._B1.get_value())
        print("value for b2: ",self._B2.get_value())
        print("value for s2: ",self._S2.get_value())
    def get_level(self):
        return self._level
X_INDEX = ['A','B','C','D','E']
Y_INDEX = ['1','2','3','4','5']
current_hex_states = {}
def valid_move(node:Node, hex_states):
    x, y = node.get_cords()
    hexagon = hex_states[Y_INDEX[y]][X_INDEX[x]]
    return (hexagon != colored("⬢", "blue")) and  (hexagon != colored("⬢", "red"))

def ai_move(p1_move, hex_states):
    x = p1_move[0]
    y = p1_move[1]
    ai_x = 4 if (x == 'A') else 0
    ai_y = 4 if (y == '5') else 0
    yield X_INDEX[ai_x] , Y_INDEX[ai_y]
    while True:
        current = Node(ai_x, ai_y)
        print(current.get_level())
        current_hex_states.update(hex_states)
        return_value = value(current) 
        current.set_value(return_value)
        move = current.get_child_node(current_hex_states)
        current.get_child_values()
        ai_x = move[0]
        ai_y = move[1]
        print("x and y", ai_x, ai_y)
        yield X_INDEX[move[0]] , Y_INDEX[move[1]]
        
def value(state:Node, alpha = -100000, beta = 100000):
    x , y = state.get_cords()
    level = state.get_level()
    if (y > 4 or y < 0 or x > 4 or x < 0 or level == 4):
        return state.get_value() 
    hexagon = current_hex_states[Y_INDEX[y]][X_INDEX[x]]
    if ((hexagon == colored("⬢", "blue")) or ( hexagon == colored("⬢", "red") ))and (level != 0):
        return state.get_value()
    state.set_child()
    if (level % 2 == 0):
        return max_value(state, alpha, beta)
    else:
        return min_value(state, alpha, beta)
    
def max_value(state:Node, alpha, beta):
    v = -1000
    for sucessor in state.get_nodes():
        v = max(v, value(sucessor, alpha, beta))
        if (v >= beta): 
            return v
        alpha = max(alpha , v)
    state.set_value(v)
    return v

def min_value(state:Node, alpha, beta):
    v = 1000
    for sucessor in state.get_nodes():
        v = min(v, value(sucessor, alpha, beta))
        if (v <= alpha): 
            return v
        beta = min(beta , v)
    state.set_value(v)
    return v
