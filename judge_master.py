import math
import random

from models import Hacker, Submission, Grade, Team


class JudgeMaster:

    # Will return the optimal number of grades per submission to be used with shuffle given the number of grades we
    # want each hacker to complete
    def getOptimalGradesPerSubmission(self, given_grades_per_hacker):
        # make sure given grades per hacker is > 0
        if given_grades_per_hacker <= 0:
            return None

        # get number of hackers and submissions
        number_of_hackers = Hacker.query.count()
        number_of_submissions = Submission.query.count()

        return math.ceil((number_of_hackers * given_grades_per_hacker) / number_of_submissions)

    # Will set x number of hackers to judge a project
    # Requires: grades_per_project int > 0
    def shuffle(self, grades_per_submission):
        # make sure grades_per_projects is positive
        if grades_per_submission <= 0:
            return None

        # get number of hackers
        number_of_hackers = Hacker.query.count()
        hackers = Hacker.query.all()

        # make sure there are more hackers than grades_per_project
        if not number_of_hackers > grades_per_submission:
            return None

        # get number of submissions
        number_of_submissions = Submission.query.count()
        submissions = Submission.query.all()

        # total number of grades
        total_grades = number_of_submissions * grades_per_submission
        # approximate amount of grades per hacker
        grades_per_hacker = math.ceil(total_grades / number_of_hackers)

        # The following vars are only for testing purposes:
        set_up = {}
        for hacker in hackers:
            set_up[hacker.name] = [0, hacker]

        # loop over each project
        for submission in submissions:
            # loop over grades_per_project
            for index in range(grades_per_submission):
                # set list of possible hackers to choose from, only those with less grades than grades_per_hacker
                hackers_to_choose = {key: value for (key, value) in set_up.items() if value[0] < grades_per_hacker}

                # Times over the while loop
                while_times = 0

                # times try again
                try_again_times = 0

                # grab a hacker that is not part of this submission
                while True:
                    while_times += 1
                    # get random hacker from list
                    hacker_key = random.choice(list(hackers_to_choose.keys()))
                    hacker_dict = hackers_to_choose[hacker_key]

                    # check that hacker is not of current project
                    if hacker_dict[1].team_id != submission.team.id:
                        hacker_dict[0] += 1
                        break

                    # if we have gone over the entire list once, then re do the list with more hackers
                    if while_times > len(hackers_to_choose):
                        try_again_times += 1
                        hackers_to_choose = {key: value for (key, value) in set_up.items() if
                                             value[0] < grades_per_hacker + try_again_times}
                        while_times = 0
        # grab the hackers with the most and least grades and try to balance them out by moving grades between the two
        sets = {}
        for key, value in set_up.items():
            if sets.get(value[0]):
                sets[value[0]].append(value)
            else:
                sets[value[0]] = [value, ]

        # we want to sort the dict by the int keys, we receive a tuple
        sets = sorted(sets.items())

        numbers = {}
        for key, value in sets:
            numbers[key] = len(value)
        print(numbers)

        # here key is number of grade, value is list of hackers with that number of grades
        for key, value in sets:
            list_to_fix = value

            # we want to bring these hackers one less than the optimal grades per hacker
            times_to_fix = grades_per_hacker - key - 1

            # only proceed if we need to fix hackers in this range of grades
            if times_to_fix > 0:
                for index in range(len(list_to_fix)):
                    item = list_to_fix[0]

                    ttf = times_to_fix

                    # remove item we are fixing from its list
                    value.remove(item)

                    # loop over the number of times we need to fix this hacker
                    while ttf > 0:
                        # highest set
                        highest_set = sets[-1]

                        # second highest set
                        second_highest_set = sets[-2]

                        # choose a random hacker that will help us
                        random_hacker = random.choice(highest_set[1])

                        # remove one from the random hacker and move one to the hacker we are fixing
                        item[0] += 1

                        highest_set[1].remove(random_hacker)
                        second_highest_set[1].append(random_hacker)
                        random_hacker[0] -= 1

                        ttf -= 1


                # create the grade object
                # grade = Grade()
                #
                # # add the new grade to the hacker and the submission
                # hacker.grades.append(grade)
                # submission.grades.append(grade)

        numbers = {}
        for key, value in sets:
            numbers[key] = len(value)
        print(numbers)
