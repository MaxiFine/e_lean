# #  consuming the restful api
# import requests


# username = 'test'
# password = 'maxwell22'
# base_url = 'http://127.0.0.1:8001/api/'

# # retrieve all courses
# r = requests.get(f'{base_url}courses/')

# courses = r.json()

# available_courses = ', '.join([course['title'] for course in courses])
# print(f'Available courses: {available_courses}')


# for course in courses:
#     course_id = course['id']
#     course_title = course['title']
#     r = requests.post(f'{base_url}courses/{course_id}/enroll/', auth=(username, password))
#     if r.status_code == 200:
#         # successful request
#         print(f'Successfully enrolled in {course_title}')




import requests
import json

username = 'test'
password = 'maxwell22'
base_url = 'http://127.0.0.1:8001/api/'

# Retrieve all courses
r = requests.get(f'{base_url}courses/')

try:
    # Check if the response is valid JSON
    json.loads(r.content.decode('utf-8'))
    courses = r.json()
except json.JSONDecodeError:
    # Handle invalid JSON response
    print("Invalid JSON response received from server")
    exit(1)

available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses: {available_courses}')

for course in courses:
    course_id = course['id']
    course_title = course['title']

    # Enroll in the course
    r = requests.post(f'{base_url}courses/{course_id}/enroll/', auth=(username, password))

    if r.status_code == 200:
        # Successful enrollment
        print(f'Successfully enrolled in {course_title}')
    else:
        # Failed enrollment
        print(f'Failed to enroll in {course_title}: {r.status_code}')
