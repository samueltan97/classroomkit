from piazza_class_participation.piazza_scraper import PiazzaScraper
from piazza_class_participation.piazza_tree import PiazzaTree
from piazza_class_participation.participation_functions import ParticipationFunctions

class ScrapeApp:

    def run(self, class_id, username, password):
        # the run function returns a tuple that contains the class participation report card for the class and the individual
        # piazza profiles of the different students (contains student info + the posts they have made)

        # piazza_interpreter is an instance of PiazzaScraper (think of it as a doorway to the Piazza classroom that
        # has been authenticated with the user's username and password)
        piazza_interpreter = PiazzaScraper(class_id, username, password)

        # piazza_posts is a list that contains dictionaries which contains information about each single thread that
        # exists on the piazza classroom.
        piazza_posts = piazza_interpreter.get_all_posts()

        # piazza_tree is an instance of PiazzaTree that consists of the different threads and the relevant posts that
        # are situated within the thread
        piazza_tree = PiazzaTree(piazza_posts)

        # participation_functions is an instance of ParticipationFunctions that is a set of functions that traverse through
        # the tree to colelct different information. It is a layer that sits on top of our piazza_tree and the piazza_interpreter
        participation_functions = ParticipationFunctions(piazza_tree, piazza_interpreter)

        # piazza_profiles is a dictionary that has the student ID as key and PiazzaStudent as the value. PiazzaStudent
        # contains important information like past posts, number of likes, and participation score
        piazza_profiles = participation_functions.build_piazza_profiles()

        #piazza_reportcard is a dictionary with the name of the student as key and a numerical score as the class participation
        # score
        piazza_reportcard = dict()
        for key, value in piazza_profiles.items():
            profile_name = piazza_interpreter.get_user([key])[0].get("name")
            # value is a PiazzaStudent and calculate_score simply computes the class participation score
            piazza_reportcard[profile_name] = value.calculate_score()

        return piazza_reportcard, piazza_profiles

if __name__ == "__main__":
    ScrapeApp().run("k12qbt838di4xt", "stan1@haverford.edu", "1ihorbiobwcb")