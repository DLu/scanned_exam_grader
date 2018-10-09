import os
import yaml
import argparse
import collections
from util import sort_files

def print_unique_answers(data):
    answers = collections.defaultdict(lambda: collections.defaultdict(int))
    for a in data:
        for k, v in a.iteritems():
            if k == 'NAME':
                continue
            answers[k][v] += 1

    for key in sorted(answers):
        print key
        for ans, n in sorted(answers[key].items(), key=lambda d: d[1], reverse=True):
            print '%03d %s' % (n, ans)
        print

def interpret_value(value, correct_a):
    numerical = type(correct_a) == float or type(correct_a) == int
    if numerical and len(value) > 0:
        try:
            value = eval(value)
        except:
            pass
    return value

def grade_answers(student_answers, correct, results, points):
    for student in student_answers:
        name = student['NAME']
        if name not in results:
            results[name] = {}

    for key, correct_a in sorted(correct.items()):
        incorrect_points = {}
        question_points = points[key]
        for student in student_answers:
            M = results[student['NAME']]
            if key not in student:
                continue

            answer = interpret_value(student[key], correct_a)
            if key in M:
                incorrect_points[answer] = M[key]
                continue

            if type(answer) == str and len(answer) == 0:
                M[key] = 0.0
            elif answer == correct_a:
                M[key] = 1.0
            elif answer in incorrect_points:
                M[key] = incorrect_points[answer]
            else:
                # TODO: Reimplement rounding logic
                print 'Question ' + str(key), '(%d points)' % question_points
                print 'Answer:  ' + str(answer)
                print 'Correct: ' + str(correct_a)
                x = raw_input()
                if len(x) == 0:
                    continue
                if '%' in x:
                    M[key] = float(x.replace('%', '')) / 100.0
                else:
                    M[key] = float(x) / question_points
                incorrect_points[answer] = M[key]

def print_grades(results, points):
    totals = {}
    for name, student in results.iteritems():
        pts = 0.0
        total = 0.0
        for key in points:
            pts += student.get(key, 0.0) * points[key]
            total += points[key]
        totals[name] = pts
    for name, total in sorted(totals.items(), key=lambda d: d[1], reverse=True):
        print "%30s %.1f" % (name, total)


parser = argparse.ArgumentParser(description='Grader')
parser.add_argument('folder')
args = parser.parse_args()

files = sort_files(args.folder)

DATA = []
for x in files['yaml']:
    if 'answers' in x or 'points' in x or 'results' in x:
        continue
    DATA += yaml.load(open(x))

CORRECT = yaml.load(open(os.path.join(args.folder, 'answers.yaml')))
POINTS = yaml.load(open(os.path.join(args.folder, 'points.yaml')))
r_fn = os.path.join(args.folder, 'results.yaml')
if os.path.exists(r_fn):
    results = yaml.load(open(r_fn))
else:
    results = {}
rules_fn = os.path.join(args.folder, 'rules.yaml')
if os.path.exists(rules_fn):
    rules = yaml.load(open(rules_fn))
else:
    rules = {}

print_unique_answers(DATA)
try:
    grade_answers(DATA, CORRECT, results, POINTS)
finally:
    yaml.dump(results, open(r_fn, 'w'))
print_grades(results, POINTS)

N = 40
for key in sorted(POINTS):
    t = 0.0
    p = 0.0
    u = 0.0
    for name in results:
        t += 1.0
        if key in results[name]:
            p += results[name][key]
        else:
            u += 1.0
    if t != 0.0:
        n = int(N * p / t)
        r = int(N * u / t)
    else:
        n = 0
        r = N
    x = N - n - r

    print "%4s" % key, "*" * n + ' ' * x + '?' * r, '%.2F' % (p / t)
