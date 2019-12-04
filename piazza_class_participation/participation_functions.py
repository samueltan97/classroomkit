from piazza_student import PiazzaStudent
from listqueue import ListQueue

class ParticipationFunctions:

    def __init__(self, tree, interpreter):
        self.tree = tree
        self.interpreter = interpreter

    def build_piazza_profiles(self):
        piazza_profiles = dict()
        piazza_node_queue = ListQueue()
        for root_node in self.tree.root:
            piazza_node_queue.enqueue(root_node)
        self.traverse_piazza_tree(piazza_node_queue, piazza_profiles)
        while piazza_node_queue.is_empty() is False:
            print("size", len(piazza_node_queue))
            self.piazza_node_handler(piazza_node_queue.dequeue(), piazza_profiles)
        return piazza_profiles


    def traverse_piazza_tree(self, queue, piazza_profiles):
        current_node = queue.dequeue()
        for child in current_node.children:
            queue.enqueue(child)
        self.piazza_node_handler(current_node, piazza_profiles)
        if queue.is_empty() is False:
            self.traverse_piazza_tree(queue, piazza_profiles)

    def piazza_node_handler(self, current_node, piazza_profiles):
        print(current_node.thread_number)
        if piazza_profiles.get(current_node.author) is not None:
            piazza_profiles.get(current_node.author).add_post(current_node)
        else:
            if current_node.author is not None:
                profile_name = self.interpreter.get_user([current_node.author])[0].get("name")
                piazza_profiles[current_node.author] = PiazzaStudent(profile_name, current_node.author)
                piazza_profiles[current_node.author].add_post(current_node)
