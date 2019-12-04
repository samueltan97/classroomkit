from piazza_node import PiazzaNode

class PiazzaTree:

    def __init__(self, post):
        self.root = []
        self.post = post
        self.setup_tree()

    def setup_tree(self):
        for thread in self.post:
            print(thread)
            tag = thread.get("tag_endorse")
            author = (thread.get("change_log"))[0].get("uid")
            thread_data = thread.get("history")[0]
            if tag:
                self.root.append(PiazzaNode(thread.get("nr"), author, thread.get("children"), thread.get("tag_endorse"), thread_data.get("subject"), thread.get("type"), thread_data.get("content"), thread.get("no_upvote")))
            else:
                self.root.append(PiazzaNode(thread.get("nr"), author, thread.get("children"), thread.get("tag_good"), thread_data.get("subject"), thread.get("type"), thread_data.get("content"), thread.get("no_upvote")))
