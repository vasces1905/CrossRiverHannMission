### Your code here! Created by Tom Siggers - University of Bath - thanks to him..
import numpy as np

class Node:
    def __init__(self, parent, action, m_wrong_side, c_wrong_side, boat_wrong_side):
        self.state = np.array([m_wrong_side, c_wrong_side, boat_wrong_side])
        self.parent = parent
    
    
    def __str__(self):
        #Print state of a node for testing.
        return f'This node has state, missionaries: {self.state[0]}, cannibals: {self.state[1]}, and boats: {self.state[2]} on the wrong side.'
    
    def is_goal_state(self):
        #No missionaries, cannibals or boats are on the starting bank.
        if np.array_equal(self.state,np.array([0,0,0])):
            return True
        return False
    
    def is_valid_state(self):
         #if there are more cannibals than missionaries then the state is invalid.
        if (0 <= self.state[0] <= 3) and (0 <= self.state[1] <= 3) and ((self.state[0] == 0 | self.state[0] >= self.state[1]) and (self.state[0] == 3 | self.state[0] >= self.state[1])):
            return True
        else: 
            return False

    def get_child_node(self, action):
        #Copy the array for a new copy
        child_vector = np.array([self.state[0],self.state[1]])
        
        if self.state[2] == 1:
            #subtract the vector
            #change the boat
            child_vector -= action
            child_vector = np.append(child_vector, 0)
            child_node = Node(self, action, child_vector[0], child_vector[1], child_vector[2])
        else:
            #the boat is going away from the right side so add the vector
            child_vector += action
            child_vector = np.append(child_vector, 1)
            child_node = Node(self, action, child_vector[0], child_vector[1], child_vector[2])
        return child_node

            

    

class Game:
    def __init__(self):
        self.initial_node = Node(None, None, m_wrong_side=3, c_wrong_side=3, boat_wrong_side=1)
        #Create vectors of all possible moves
        self.actions = np.array([(1,0),(0,1),(1,1),(2,0),(0,2)])  
     
    def in_list(self, new_state, existing):
        for explored_state in existing:
            if np.array_equal(new_state.state, explored_state.state):
                return True
            return False
    
        
    def bfs(self):
        explored = []
        frontier = [self.initial_node]
        generated = 0
        
        #standard BFS loop similar to TOH
        current_state = frontier.pop(0)
        while not current_state.is_goal_state():
            explored.append(current_state)
            
            for action in self.actions:
                generated += 1
                new_state = current_state.get_child_node(action)
                print(new_state)
                if (not self.in_list(new_state, explored)) & (not self.in_list(new_state, frontier)) & new_state.is_valid_state():
                    frontier.append(new_state)
                    print(new_state)
                
            if (len(frontier) == 0):
                print('No solution found.')
                return 
            
            current_state = frontier.pop(0)
            
        print("Solution found!")
        print(f"Explored {len(explored)} states")
        print(f"Generated {generated} states")
        print(current_state)
        print()

        #Create the sequence by following parent tags.
        final_path = []
        while current_state.parent != None:
            final_path.append(current_state)
            current_state = current_state.parent
        final_path.append(current_state)
        
        #Iterate backwards to put sequence in the correct order.
        for state in reversed(final_path):
            print(state)
            
        
        
g = Game()
g.bfs()
