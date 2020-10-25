class PiazzaNode:
    def __init__(self, thread_number, author=None, children=None, tag_endorse=None, subject=None, type=None, content=None, no_upvote=None):
        self.thread_number = thread_number
        # note: author is the piazza_id of the student and not the name of the student
        self.author = author
        # children is a list of children PiazzaNodes
        self.children = children
        # tag_endorse is a list of users who have either liked or endorsed the post
        self.tag_endorse = tag_endorse
        self.subject = subject
        self.type = type
        self.content = content
        self.no_upvote = no_upvote
        # implements the create_children_piazza_node() function which uses the information in self.children to create children nodes
        self.create_children_piazza_node()

    def create_children_piazza_node(self):
        # final_children will be appended with the PiazzaNode of its children
        final_children = []
        # if this PiazzaNode has children, create PiazzaNodes from them and append them into final_children
        if self.children is not None:
            for child in self.children:
                # some nodes have tag_endorse instead of tag_good depending on the type of post
                tag = child.get("tag_endorse")
                author = child.get("uid")
                # some nodes have history depending on the type of post
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