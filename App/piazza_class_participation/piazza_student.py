class PiazzaStudent:

    def __init__(self, name, id, score=None):
        self.name = name
        self.id = id
        self.score = score
        # self.posts gives a dictionary that has the thread id has the key and a list of PiazzaNode(posts/comments) made by the user
        # in that thread
        self.posts = dict()
        self.number_of_posts = 0
        self.number_of_instructor_likes = 0
        self.number_of_student_likes = 0
        self.immediate_children_from_own_post = 0
        # grandchildren refers to all nodes that are below its children nodes
        self.grandchildren_from_own_post = 0


    def calculate_score(self):
        # calculate score is the method that combines the different factors that constitutes what makes a great post
        # and return a score
        total_score = 0
        total_score += (1.5 * self.number_of_posts)
        total_score += (10 * self.number_of_instructor_likes)
        total_score += (3.5 * self.number_of_student_likes)
        total_score += (2 * self.immediate_children_from_own_post)
        total_score += (0.5 * self.grandchildren_from_own_post)
        self.score = total_score
        return self.score

    def add_post(self, piazza_node):
        # add_post adds a piazza_node to the list of posts/comments in self.posts made in a certain thread by the user

        # if no post has been made by the user in this thread prior to the function call, create a new list with the
        # post appended as a node
        if self.posts.get(piazza_node.thread_number) is None:
            self.posts[piazza_node.thread_number] = [piazza_node]
        # if there are already posts made by the user in this thread, simply append the post/comment as a node in the list
        else:
            self.posts[piazza_node.thread_number].append(piazza_node)
        #increase the count of self.number_of_posts to faciliate subsequent counting of score
        self.number_of_posts += 1
        # separate the number of instructor likes and student likes from the post. a tuple with the two different values
        # will be returned.
        instructor_student_likes = self.split_likes_to_instructor_and_students(piazza_node)
        #increase the count of the different likes to faciliate subsequent counting of score
        self.number_of_instructor_likes += instructor_student_likes[0]
        self.number_of_student_likes += instructor_student_likes[1]
        # separate the number of children posts/comments and posts/comments below the children nodes. a tuple with the two different values
        # will be returned.
        immediate_children_grandchildren_count = self.split_immediate_children_and_grandchildren(piazza_node)
        #increase the count of the different posts to faciliate subsequent counting of score
        self.immediate_children_from_own_post += immediate_children_grandchildren_count[0]
        self.grandchildren_from_own_post += immediate_children_grandchildren_count[1]

    def split_likes_to_instructor_and_students(self, piazza_node):
        # this function figures out how many likes came from instructor and how many came from students before returning
        # a tuple that contains both values
        instructor_likes = 0
        student_likes = 0
        if piazza_node.tag_endorse is not None:
            # basically, if the role within the tag_endorse is professor or instructor, the endorse/like would be classified
            # as one from an instructor
            for endorse in piazza_node.tag_endorse:
                if endorse.get("role") == 'professor' or endorse.get("role") == "instructor":
                    instructor_likes += 1
                else:
                    student_likes += 1
        return (instructor_likes, student_likes)

    def split_immediate_children_and_grandchildren(self, piazza_node):
        # this function figures out how many nodes below that post are children and grandchildren (lower than children) returning
        # a tuple that contains both values
        immediate_children = 0
        grandchildren = 0
        immediate_children += len(piazza_node.children)
        for child in piazza_node.children:
            # the recursive function (check_for_number_of_grandchildren) is called recursively to find all grandchildren that lie below
            # the children nodes
            grandchildren += self.check_for_number_of_grandchilren(child, grandchildren)
        return (immediate_children, grandchildren)

    def check_for_number_of_grandchilren(self, piazza_node, count):
        new_count = count
        # since piazza_node.children will never be none (at worst, it is just an empty list), this recursive function will always
        # be able to see if there are any grandchildren
        for child in piazza_node.children:
            new_count += self.check_for_number_of_grandchilren(child, new_count)
        return new_count


