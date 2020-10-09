# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:50:20 2020

@author: Ronin
"""

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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# Barely passing solution! 1995 moves
tg = {player.current_room.id: player.current_room.get_exits()}
reverse = []
opp_d = {"n": "s", "e": "w", "s": "n", "w": "e"}
while len(tg) < len(world.rooms):
    if player.current_room.id not in tg:
        
        tg[player.current_room.id] = player.current_room.get_exits()
        
        direction = tg[player.current_room.id].pop()
       
        player.travel(direction)
        player.current_room.get_exits().remove(opp_d[direction])
        
        traversal_path.append(direction)
        reverse.append(opp_d[direction])
    else:
        if player.current_room.id in tg and len(tg[player.current_room.id]) > 0:
            direction = tg[player.current_room.id].pop()
            player.travel(direction)
            player.current_room.get_exits().remove(opp_d[direction])
            traversal_path.append(direction)
            reverse.append(opp_d[direction])
        else:
            move_back = reverse.pop()
            
            player.travel(move_back)
            traversal_path.append(move_back)
            if len(tg[player.current_room.id]) > 0:
                direction = tg[player.current_room.id].pop()
                player.travel(direction)
                player.current_room.get_exits().remove(opp_d[direction])
                traversal_path.append(direction)
                reverse.append(opp_d[direction])
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
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