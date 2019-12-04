from piazza_scraper import PiazzaScraper
from piazza_tree import PiazzaTree
from participation_functions import ParticipationFunctions
import queue
import objgraph

class_id = input("Enter a class ID: ")
piazza_interpreter = PiazzaScraper(class_id)

piazza_posts = piazza_interpreter.get_all_posts()
piazza_tree = PiazzaTree(piazza_posts)
participation_functions = ParticipationFunctions(piazza_tree, piazza_interpreter)
piazza_profiles = participation_functions.build_piazza_profiles()
piazza_reportcard = dict()
for key, value in piazza_profiles.items():
    profile_name = piazza_interpreter.get_user([key])[0].get("name")
    piazza_reportcard[profile_name] = value.calculate_score()
    print(profile_name, piazza_reportcard[profile_name])

objgraph.show_refs([piazza_tree])
