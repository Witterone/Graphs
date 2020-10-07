import random, math
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


class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        self.friend_added = 0

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        for i in range(0, num_users):
            self.add_user(f"User {i}")
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        random.shuffle(possible_friendships)
        
        for i in range(0, math.floor(num_users * avg_friendships / 2)):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])
            self.friend_added += 1
        
    def find_friends(self, user_id):
        return self.friendships[user_id]
        
        
    
    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  
        
        for i in self.users:
            if i == user_id:
                    visited[i]=user_id
            if i not in visited:
                
                path_check = set()
                q = Queue()
                q.enqueue([user_id])
                
                while q.size() >0:
                    path = q.dequeue()
                    v = path[-1]
                    if v == i:
                        visited[i] =  path
                        break
                    if v not in path_check:
                        path_check.add(v)
                        
                        for bro in self.find_friends(v):
                            
                            new_path = list(path)+[bro]
                            if bro == i:
                                visited[i] = new_path
                                break
                            q.enqueue(new_path)
        
        paths = []    
        for x in visited:
            if type(visited[x]) != int:
                paths.append(len(visited[x]))
            else:
                paths.append(1)
        average_path =   sum(paths)/len(paths)      
        percent_connected = (len(visited)/len(self.users))
        return visited,"percent connected "+str(percent_connected),"average distance of separation "+str(average_path)





if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print("friendships",sg.friendships)
    connections = sg.get_all_social_paths(1)
    print("connections",connections)

bg = SocialGraph()
bg.populate_graph(1000,5)
print(bg.friend_added)
connections = bg.get_all_social_paths(1)
print("connections",connections)
"Question 1 : answer 500"
"Question 2 : answer almost 100% and 7.5 "