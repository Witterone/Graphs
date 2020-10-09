from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# queue function for ease of access
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
    
# stack for ease    
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
    
directions = ["n","s","e","w"]

visited = set()

def get_adj(room_id):
    adj = []

    for dr in mapper[room_id]:
        y = mapper[room_id][dr]
        adj.append((y, dr))
    return adj
#unimplimented
def walk_back2(cur_room, path):
    cur = cur_room.id
    path_back=[]
    new_room = None
    for i in range(1, len(path)):
        plus = mapper[cur][look_back(path[-i])]
        path_back.append([look_back(path[-i])])
        for rms in get_adj(plus):
            if rms[0] == "?":
                path_back = path_back + [rms[1]]
                room = world.rooms[plus]
                new_room = room.get_room_in_direction(rms[1])
                break
            cur = plus
       
    if new_room is None:
        new_room = -1
        
    
    return path_back,new_room

def walk_back(cur_room):
    q = Queue()
    searched = set()
    q.enqueue([cur_room.id])
    new_room = None
    path = []
    
    while q.size() > 0:
        cors = q.dequeue()
        v = cors[-1]
        
       
        if v not in searched:
            searched.add(v)
            if len(get_adj(v))<2:
                back = get_adj(v)[0]
                new_cors = cors + [back[0]]
                q.enqueue(new_cors)
                
            else:
                for rms in get_adj(v):
                    
                    if rms[0] not in visited :
                        
                        if mapper[v][rms[1]]=="?":
                            room = world.rooms[v]
                            new_room = room.get_room_in_direction(rms[1])
                            if new_room is not None and new_room.id not in mapper:
                                if mapper[v][rms[1]] != new_room.id:
                                    mapper[v][rms[1]]=new_room.id
                                mapper[new_room.id] = dict()
                                mapper[new_room.id][look_back(rms[1])]=v
                                # print("back",mapper[v][rms[1]],mapper[new_room.id][look_back(rms[1])])                              
                                break
                                
                            else:
                                
                                mapper[v].pop(rms[1])
                                q.enqueue(cors)
                        else:
                            
                            room = world.rooms[v]
                            new_room = room.get_room_in_direction(rms[1])
                            print("unvisited",room.id,new_room.id)
                            break
                        
                    elif rms[0] not in searched:
                        new_cors = cors + [rms[0]]
                        q.enqueue(new_cors)
                    
                        
    if new_room is not None:
        path = cors+[room.id,new_room.id]
    if new_room is None:
        new_room = -1
    
    way = [] 
    print(path)           
    for indx in range(len(path)-1):
        for dr in mapper[path[indx]]:            
            if mapper[path[indx]][dr] == path[indx+1]:
                way.append(dr)
    print("way",way)
    return way,new_room

mapper = {}

traversal_path = []

def look_back(direction):
    opposites = {'n':'s',
                 's':'n',
                 'w':'e',
                 'e':'w'}
    return opposites[direction]

def pathfinder(map_set,room = None,travel = None):
    s = Stack()
    if room is None:
        room =  map_set.starting_room
        
    s.push(room)
    
    if travel is None:
        travel = []
    while s.size() > 0:
        r = s.pop()
        if r.id not in visited:
            visited.add(r.id)
            if r.id not in mapper:
                mapper[r.id] = dict()
            
            for dr in directions:
                if dr not in mapper[r.id]:
                    mapper[r.id][dr] = "?"
            for dr in directions:
                if mapper[r.id][dr]=="?":
                    rm = r.get_room_in_direction(dr)
                
            
                    if rm is not None and rm.id not in visited:
                        travel.append(dr)
                        mapper[r.id][dr]=rm.id
                        mapper[rm.id] = dict()
                        mapper[rm.id][look_back(dr)] = r.id
                        # print("path",mapper[r.id][dr],mapper[rm.id][look_back(dr)])
                        s.push(rm)
                        break
                    if rm is None:
                        
                        mapper[r.id].pop(dr)
                    
    back, x = walk_back(r)
    
    travel = travel + back
    if x == -1:
        continues = travel
        return continues
    continues = pathfinder(map_set,x,travel)
    
    return continues
    
    
    
    
     
traversal_path = pathfinder(world)         
    
print(traversal_path, visited, mapper)



# TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
