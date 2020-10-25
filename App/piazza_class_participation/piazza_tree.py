from piazza_class_participation.piazza_node import PiazzaNode

class PiazzaTree:

    def __init__(self, post):
        # self.root is a list of the first post/node in the different threads
        self.root = []
        # self.post contains a list of the different threads and their posts in an unordered manner without the custom
        # data structure designed by the scraper
        self.post = post
        # the setup_tree function kickstarts the conversion of all messy post/comments in threads into nodes that are linked
        # to this tree
        self.setup_tree()

    def setup_tree(self):
        # iterates through the first post in every thread and convert them into PIazzaNodes that are appended to self.root
        for thread in self.post:
            print(thread)
            tag = thread.get("tag_endorse")
            author = (thread.get("change_log"))[0].get("uid")
            thread_data = thread.get("history")[0]
            # vary data structure depending on the type of post (instructor/student). After the head nodes are created, an internal function
            # within the PiazzaNode will be called after they are instantiated to check for possible children nodes before instantiating
            # those children nodes in a recursive manner while ensuring they are connected to their parent nodes
            if tag:
                self.root.append(PiazzaNode(thread.get("nr"), author, thread.get("children"), thread.get("tag_endorse"), thread_data.get("subject"), thread.get("type"), thread_data.get("content"), thread.get("no_upvote")))
            else:
                self.root.append(PiazzaNode(thread.get("nr"), author, thread.get("children"), thread.get("tag_good"), thread_data.get("subject"), thread.get("type"), thread_data.get("content"), thread.get("no_upvote")))
