from piazza_class_participation.piazza_student import PiazzaStudent
from piazza_class_participation.listqueue import ListQueue

class ParticipationFunctions:

    def __init__(self, tree, interpreter):
        self.tree = tree
        self.interpreter = interpreter

    def build_piazza_profiles(self):
        # method returns a dictionary that has the student's piazza id as the key and the PiazzaStudent as a value

        piazza_profiles = dict()
        # method uses a Queue to traverse through the tree in a level order traversal
        piazza_node_queue = ListQueue()
        # iterates through the head of each thread in the piazza classroom and enque the head node of each thread
        for root_node in self.tree.root:
            piazza_node_queue.enqueue(root_node)
        # runs the recursive function of traverse_piazza_tree with the queue and piazza_profiles. this also applies
        # the node_handler method on those nodes which extract the PiazzaStudent profile and insert it into piazza_profiles
        self.traverse_piazza_tree(piazza_node_queue, piazza_profiles)
        # apply the node_handler method on remaining nodes which are not cleared from the queue
        while piazza_node_queue.is_empty() is False:
            self.piazza_node_handler(piazza_node_queue.dequeue(), piazza_profiles)
        return piazza_profiles


    def traverse_piazza_tree(self, queue, piazza_profiles):
        # when traversing through the piazza_tree, we dequeue the first node before enqueing its children nodes
        current_node = queue.dequeue()
        for child in current_node.children:
            queue.enqueue(child)
        # following which, apply node_handler function to extract student profile from the node to piazza_profiles
        self.piazza_node_handler(current_node, piazza_profiles)
        # if the queue still has some nodes inside, apply traverse_piazza_tree method recursively
        if queue.is_empty() is False:
            self.traverse_piazza_tree(queue, piazza_profiles)

    def piazza_node_handler(self, current_node, piazza_profiles):
        # if the author of the node is not anonymous and already has been added to piazza_profiles,
        # add a post to the user in piazza_profiles
        if piazza_profiles.get(current_node.author) is not None:
            piazza_profiles.get(current_node.author).add_post(current_node)
        else:
            # else if the author is not anonymous and hasn't been added to piazza_profiles before, create a new PiazzaStudent
            # for the user and then add the post to his or her profile on piazza_profiles
            if current_node.author is not None:
                profile_name = self.interpreter.get_user([current_node.author])[0].get("name")
                piazza_profiles[current_node.author] = PiazzaStudent(profile_name, current_node.author)
                piazza_profiles[current_node.author].add_post(current_node)
