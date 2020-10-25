from piazza_api import Piazza

# PiazzaScraper is a custom class built from the unofficial Piazza API available online. Think of it as a doorway that
# allows the user to gain access to the Piazza classroom after authenticating his or her identity with username
# and password
class PiazzaScraper:

    # class_code refers to the k12qbt838di4xt in https://piazza.com/class/k12qbt838di4xt
    def __init__(self, class_code, username, password):
        self.piazza = Piazza()
        self.piazza.user_login(username, password)
        self.piazza_class = self.piazza.network(class_code)


    def get_all_posts(self):
        # get_all_posts returns a list of dictionaries. The dictionaries contains information of the thread that resides
        # in the Piazza classroom
        feed = self.piazza_class.get_feed(limit=999999, offset=0)
        thread_ids = [post['id'] for post in feed["feed"]]
        posts = []
        for thread_id in thread_ids:
            posts.append(self.piazza_class.get_post(thread_id))
        return posts

    def get_post(self, thread_id):
        # get_post allows the user to get the dictionary that contains information of a single thread
        return self.piazza_class.get_post(thread_id)

    def get_users(self):
        # get_users allows the user to get a list of dictionaries that contains the profile of a Piazza user
        return self.piazza_class.get_all_users()

    def get_user(self, user_id):
        # get_users allows the user to get a dictionary that contains the profile of a Piazza user
        return self.piazza_class.get_users(user_id)

if __name__ == "__main__":
    pass