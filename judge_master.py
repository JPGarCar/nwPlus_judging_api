import math
import random

from models import Hacker, Submission, Grade, Team


class JudgeMaster:

    # helper function, makes sure the given hacker is not already grading the given submission
    # will return a boolean, True if not grading, False if grading
    def hackerNotGradingThis(self, hacker, submission):
        for grade in hacker.grades:
            if grade.submission.id == submission.id:
                return False
        return True

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

                    hacker = hacker_dict[1]
                    num_of_grades = hacker_dict[0]

                    # check that hacker is not of current project
                    if hacker.team_id != submission.team.id:
                        # check that this hacker is not already grading this submission
                        if num_of_grades == 0 or self.hackerNotGradingThis(hacker, submission):
                            num_of_grades += 1
                            # create the grade object
                            grade = Grade()

                            # add the new grade to the hacker and the submission
                            hacker.grades.append(grade)
                            submission.grades.append(grade)

                            # need to set list items to the edited items
                            hacker_dict[1] = hacker
                            hacker_dict[0] = num_of_grades

                            break

                    # if we have gone over the entire list once, then re do the list with more hackers
                    if while_times > len(hackers_to_choose):
                        try_again_times += 1
                        hackers_to_choose = {key: value for (key, value) in set_up.items() if
                                             value[0] < grades_per_hacker + try_again_times}
                        while_times = 0

        # grab the hackers with the most and least grades and try to balance them out by moving grades between the two

        # order the hackers by number of grades in them
        sets = {}
        for key, value in set_up.items():
            if sets.get(value[0]):
                sets[value[0]].append(value)
            else:
                sets[value[0]] = [value, ]

        # grab max number of grades in hacker
        max_num = sorted(sets.keys())[-1]

        # add numbers 0 to man_num to sets if it does not exist
        for index in range(max_num):
            if index not in sets.keys():
                sets[index] = []

        # we want to sort the dict by the int keys, we receive a tuple
        sets = sorted(sets.items())

        print(self.getDistribution(sets))

        # here key is number of grade, value is list of hackers with that number of grades
        for key, value in sets:
            list_to_fix = value

            # we want to bring these hackers one less than the optimal grades per hacker
            times_to_fix = grades_per_hacker - key - 1

            # only proceed if we need to fix hackers in this range of grades
            if times_to_fix > 0:
                for index in range(len(list_to_fix)):
                    # the list of number of grades and the hacker we are working with
                    num_grades_hacker_list = list_to_fix[0]

                    ttf = times_to_fix

                    # highest set, set of optimal value
                    highest_set = sets[grades_per_hacker]

                    # second highest set, set of one less than optimal value
                    second_highest_set = sets[grades_per_hacker - 1]

                    # loop over the number of times we need to fix this hacker
                    while ttf > 0:

                        # choose a random hacker that will help us
                        random_num_grades_hacker_list = random.choice(highest_set[1])

                        # iterate of grades of random hacker
                        for grade in random_num_grades_hacker_list[1].grades:

                            # make sure the grade is not of the hacker's team
                            if grade.submission.team_id is not num_grades_hacker_list[1].team_id:

                                # make grade switch
                                grade = random_num_grades_hacker_list[1].grades.pop()
                                num_grades_hacker_list[1].grades.append(grade)

                                # add one grade to hacker
                                num_grades_hacker_list[0] += 1

                                # remove one from random hacker and switch him to next list below
                                highest_set[1].remove(random_num_grades_hacker_list)
                                second_highest_set[1].append(random_num_grades_hacker_list)
                                random_num_grades_hacker_list[0] -= 1

                                # fix was complete so remove a time to fix and break out of for each loop
                                ttf -= 1
                                break
                        # if all the grades from the random hacker can't be added to this hacker than choose a different
                        # random hacker next round
                    # if the num_grade_hacker_list number of grades is different from the key then we remove it
                    # from the current list and add it to a new list depending on the number of grades
                    if num_grades_hacker_list[0] is not key:
                        # remove num_grades_hacker_list we are fixing from its list
                        value.remove(num_grades_hacker_list)

                        # add the num_grade_hacker_list we are fixing to its new list
                        sets[num_grades_hacker_list[0]][1].append(num_grades_hacker_list)
            # this is to fix hackers with too many grades
            if times_to_fix < -1:
                for index in range(len(list_to_fix)):
                    # the list of number of grades and the hacker we are working with
                    num_grades_hacker_list = list_to_fix[0]

                    ttf = times_to_fix

                    # lowest set, the time to fix minus one more
                    lowest_set = sets[(times_to_fix - 1)]

                    # second lowest set
                    second_lowest_set = sets[times_to_fix]

                    # loop over the number of times we need to fix this hacker
                    while ttf < -1:

                        # choose a random hacker that will help us
                        random_num_grades_hacker_list = random.choice(lowest_set[1])

                        # iterate of grades of hacker with too many grades
                        for grade in num_grades_hacker_list[1].grades:

                            # make sure the grade is not of the random hacker's team
                            if grade.submission.team_id is not num_grades_hacker_list[1].team_id:

                                # make grade switch
                                grade = num_grades_hacker_list[1].grades.pop()
                                random_num_grades_hacker_list[1].grades.append(grade)

                                # remove one from the hacker
                                num_grades_hacker_list[0] -= 1

                                # add one to random hacker and bump him one list up
                                lowest_set[1].remove(random_num_grades_hacker_list)
                                second_lowest_set[1].append(random_num_grades_hacker_list)
                                random_num_grades_hacker_list[0] += 1

                                # fix was complete so remove a time to fix and break out of for each loop
                                ttf += 1
                                break
                        # if all the grades from the random hacker can't be added to this hacker than choose a different
                        # random hacker next round
                    # if the num_grade_hacker_list number of grades is different from the key then we remove it
                    # from the current list and add it to a new list depending on the number of grades
                    if num_grades_hacker_list[0] is not key:
                        # remove num_grades_hacker_list we are fixing from its list
                        value.remove(num_grades_hacker_list)
                        sets[num_grades_hacker_list[0]][1].append(num_grades_hacker_list)
        dis = self.getDistribution(sets)
        print(dis)
        return dis

    def getDistribution(self, sets):
        numbers = {}
        for key, value in sets:
            numbers[key] = len(value)
        return numbers
