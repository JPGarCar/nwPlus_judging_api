import random

from models import Hacker, Submission, Grade, Team


class JudgeMaster:

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
        grades_per_hacker = total_grades // number_of_hackers

        # The following vars are only for testing purposes:
        total_loops = 0
        set_up = {}
        for hacker in hackers:
            set_up[hacker.name] = 0

        # loop over each project
        for submission in submissions:
            # loop over grades_per_project
            for index in range(grades_per_submission):
                # grab a hacker that is not part of this submission
                while True:
                    total_loops += 1
                    # get random hacker from list
                    hacker = random.choice(hackers)
                    # check that hacker is not of current project
                    if hacker.team_id != submission.team.id:
                        set_up[hacker.name] += 1
                        break
                # create the grade object
                # grade = Grade()
                #
                # # add the new grade to the hacker and the submission
                # hacker.grades.append(grade)
                # submission.grades.append(grade)

        print(set_up)
        print(total_loops) # TODO remove