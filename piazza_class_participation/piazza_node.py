class PiazzaNode:
    def __init__(self, thread_number, author=None, children=None, tag_endorse=None, subject=None, type=None, content=None, no_upvote=None):
        self.thread_number = thread_number
        self.author = author
        self.children = children
        self.tag_endorse = tag_endorse
        self.subject = subject
        self.type = type
        self.content = content
        self.no_upvote = no_upvote
        self.create_children_piazza_node()

    def create_children_piazza_node(self):
        final_children = []
        if self.children is not None:
            for child in self.children:
                tag = child.get("tag_endorse")
                author = child.get("uid")
                if child.get("history") is None:
                # child_data = child.get("history")[0]
                    if tag:
                        final_children.append(PiazzaNode(self.thread_number, author, child.get("children"), child.get("tag_endorse"), child.get("subject"), child.get("type"), child.get("content"), child.get("no_upvote")))
                    else:
                        final_children.append(PiazzaNode(self.thread_number, author, child.get("children"), child.get("tag_good"), child.get("subject"), child.get("type"), child.get("content"), child.get("no_upvote")))
                else:
                    history = child.get("history")[0]
                    if tag:
                        final_children.append(
                            PiazzaNode(self.thread_number, history.get("uid"), child.get("children"), child.get("tag_endorse"), history.get("subject"),
                                       child.get("type"), history.get("content"), child.get("no_upvote")))
                    else:
                        final_children.append(
                            PiazzaNode(self.thread_number, history.get("uid"), child.get("children"), child.get("tag_good"), history.get("subject"),
                                       child.get("type"), history.get("content"), child.get("no_upvote")))

        self.children = final_children