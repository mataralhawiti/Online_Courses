# -*- coding: utf-8 -*-
import unicodecsv
from datetime import datetime as dt


def process_csv(file_location, mode):
	with open(file_location, mode) as f:
		reader = unicodecsv.DictReader(f)
		return list(reader)


# -- SET OF FUNCTIONS TO CLEAN UP THE DATA, AND FIX DATA TYPE ISSUES
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



#-- Let's test our function
enrollments = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/enrollments.csv','rb')
daily_engagement = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/daily_engagement.csv','rb')
project_submissions = process_csv('/home/matar/GitHub/Online_Courses/Udacity-ND/P02_Investigate_A_Dataset/Lessons/project_submissions.csv','rb')



# clean up enrollments
for enrollment in enrollments:
	enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
	enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
	enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
	enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
	enrollment['join_date'] = parse_date(enrollment['join_date'])

	
# clean up 	daily engagement
for engagement_record in daily_engagement:
	engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
	engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
	engagement_record['total_minutes_visited'] = float(engagement_record['projects_completed'])
	engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
	engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))


for project_submission in project_submissions:
	project_submission['completion_date'] = parse_date(project_submission['completion_date'])
	project_submission['creation_date'] = parse_date(project_submission['creation_date'])

