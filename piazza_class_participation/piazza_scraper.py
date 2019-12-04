from piazza_api import Piazza

class PiazzaScraper:

    def __init__(self, class_code):
        self.piazza = Piazza()
        self.piazza.user_login()
        Email: "stan1@haverford.edu"
        Password: "ABCabc123,./S9718941B"
        self.piazza_class = self.piazza.network(class_code)


    def get_all_posts(self):
        feed = self.piazza_class.get_feed(limit=999999, offset=0)
        thread_ids = [post['id'] for post in feed["feed"]]
        posts = []
        for thread_id in thread_ids:
            posts.append(self.piazza_class.get_post(thread_id))
        return posts

    def get_post(self, thread_id):
        return self.piazza_class.get_post(thread_id)

    def get_users(self):
        return self.piazza_class.get_all_users()

    def get_user(self, user_id):
        return self.piazza_class.get_users(user_id)

    def get_statistics(self):
        return self.piazza_class.get_statistics()

if __name__ == "__main__":
    pass