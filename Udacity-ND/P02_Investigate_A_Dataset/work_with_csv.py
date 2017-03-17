# -*- coding: utf-8 -*-
import unicodecsv
from datetime import datetime as dt


def process_csv(file_location, mode):
	with open(file_location, mode) as f:
		reader = unicodecsv.DictReader(f)
		return list(reader)


# -- Load the data files -------------------------------------------------------
enrollments = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/enrollments.csv','rb')
daily_engagement = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/daily_engagement.csv','rb')
project_submissions = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/project_submissions.csv','rb')


# -- SET OF FUNCTIONS TO CLEAN UP THE DATA, AND FIX DATA TYPE ISSUES -----------------
'''
Take date as string, then retune datetime python object 
if no date is given, returns None
'''
def parse_date(date):
	if date == '':
		return None
	else:
		return dt.strptime(date, '%Y-%m-%d')

'''
takes a string which either is empty or represent int
return int or None
'''
def parse_maybe_int(i):
	if i == '':
		return None
	else:
		return int(i)

	# -- END OF THE FUNCTIONS SET


# clean up the datasets ---------------------------------------------------------------------
for enrollment in enrollments:
	enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
	enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
	enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
	enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
	enrollment['join_date'] = parse_date(enrollment['join_date'])

for engagement_record in daily_engagement:
	engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
	engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
	engagement_record['total_minutes_visited'] = float(engagement_record['projects_completed'])
	engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
	engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))


for project_submission in project_submissions:
	project_submission['completion_date'] = parse_date(project_submission['completion_date'])
	project_submission['creation_date'] = parse_date(project_submission['creation_date'])



# get the total, uniqe students in each dataset ----------------------------
"enrollments"
enrollment_num_rows = len(enrollments)
enrollment_num_unique_students = 0

# enrollment_unique_students = set()
# for enrollment in enrollments:
# 	enrollment_unique_students.add(enrollment['account_key'])

# enrollment_num_unique_students = len(enrollment_unique_students)

"daily_engagement"
engagement_num_rows = len(daily_engagement)            # Replace this with your code
engagement_num_unique_students = 0  # Replace this with your code

# engagement_unique_students = set()
# for engagement_record in daily_engagement:
# 	engagement_unique_students.add(engagement_record['acct'])

# engagement_num_unique_students = len(engagement_unique_students)


"project_submissions"
submission_num_rows = len(project_submissions)             # Replace this with your code
submission_num_unique_students = 0  # Replace this with your code

# submission_unique_students = set()
# for project_submission in project_submissions:
# 	submission_unique_students.add(project_submission['account_key'])

# submission_num_unique_students = len(submission_unique_students)



#-- fix 'acct' name issues by creating a new key in the dict, then delete the old key
for engagement_record in daily_engagement:
	engagement_record['account_key'] = engagement_record['acct']
	del(engagement_record['acct'])



#-- create more generic function to get the unique students number
def get_unique_students(data):
	unique_students = set()
	for student in data:
		unique_students.add(student['account_key'])
	return unique_students

enrollment_num_unique_students = len(get_unique_students(enrollments))
engagement_num_unique_students = len(get_unique_students(daily_engagement))
submission_num_unique_students = len(get_unique_students(project_submissions))


# issues ----------------------------------------------------------------------------
	# -- issue : why we have more student in [daily_engagement] table than [enrollments]
	#-- investigate
unique_students = get_unique_students(daily_engagement)


for enrollment in enrollments:
	student = enrollment['account_key']
	if student not in unique_students:
		print(enrollment)
		break
	"{'join_date': datetime.datetime(2014, 11, 12, 0, 0), 'account_key': '1219', 'status': 'canceled', 'is_canceled': True, 'days_to_cancel': 0, 'is_udacity': False, 'cancel_date': datetime.datetime(2014, 11, 12, 0, 0)}"
	# we can see 	join date, and cancel data are the same .. days to cancel is 0

	# -- issue : we need to investigate more for other issues
num_problem_students = 0
for enrollment in enrollments:
	student = enrollment['account_key']
	if student not in unique_students and enrollment['join_date'] != enrollment['cancel_date'] :
		print(enrollment)
		num_problem_students += 1

