class PiazzaStudent:

    def __init__(self, name, id, score=None):
        self.name = name
        self.id = id
        self.score = score
        self.posts = dict()
        self.number_of_posts = 0
        self.number_of_instructor_likes = 0
        self.number_of_student_likes = 0
        self.immediate_children_from_own_post = 0
        self.grandchildren_from_own_post = 0


    def calculate_score(self):
        total_score = 0
        total_score += (1.5 * self.number_of_posts)
        total_score += (10 * self.number_of_instructor_likes)
        total_score += (3.5 * self.number_of_student_likes)
        total_score += (2 * self.immediate_children_from_own_post)
        total_score += (0.5 * self.grandchildren_from_own_post)
        self.score = total_score
        return self.score

    def add_post(self, piazza_node):
        if self.posts.get(piazza_node.thread_number) is None:
            self.posts[piazza_node.thread_number] = [piazza_node]
        else:
            self.posts[piazza_node.thread_number].append(piazza_node)
        self.number_of_posts += 1
        instructor_student_likes = self.split_likes_to_instructor_and_students(piazza_node)
        self.number_of_instructor_likes += instructor_student_likes[0]
        self.number_of_student_likes += instructor_student_likes[1]
        immediate_children_grandchildren_count = self.split_immediate_children_and_grandchildren(piazza_node)
        self.immediate_children_from_own_post += immediate_children_grandchildren_count[0]
        self.grandchildren_from_own_post += immediate_children_grandchildren_count[1]

    def split_likes_to_instructor_and_students(self, piazza_node):
        instructor_likes = 0
        student_likes = 0
        if piazza_node.tag_endorse is not None:
            for endorse in piazza_node.tag_endorse:
                if endorse.get("role") == 'professor' or endorse.get("role") == "instructor":
                    instructor_likes += 1
                else:
                    student_likes += 1
        return (instructor_likes, student_likes)

    def split_immediate_children_and_grandchildren(self, piazza_node):
        immediate_children = 0
        grandchildren = 0
        immediate_children += len(piazza_node.children)
        for child in piazza_node.children:
            grandchildren += self.check_for_number_of_grandchilren(child, grandchildren)
        return (immediate_children, grandchildren)

    def check_for_number_of_grandchilren(self, piazza_node, count):
        new_count = count
        for child in piazza_node.children:
            new_count += self.check_for_number_of_grandchilren(child, new_count)
        return new_count


