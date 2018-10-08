import sys
import yaml

TEST = 'a'
DATA = []
for x in sys.argv[1:]:
    DATA += yaml.load(open(x))
CORRECT = yaml.load(open('%s_answers.yaml' % TEST))
POINTS = yaml.load(open('points.yaml'))

results = yaml.load(open('results.yaml'))

for answers in DATA:
    name = answers['NAME']
    M = results.get(name, {})

    pts = 0.0
    total = 0.0

    for key, value in sorted(CORRECT.items()):
        if key not in answers:
            continue
        if key in M:
            pts += M[key] * POINTS[key]
            total += POINTS[key]
            continue
        a = answers[key]
        numerical = type(value) == float or type(value) == int
        if numerical and len(a) > 0:
            a = eval(a)

        if type(a) == str and len(a) == 0:
            M[key] = 0.0
        elif a == value:
            M[key] = 1.0
        elif numerical:
            if '1' in key and round(value, 1) == round(a, 1):
                M[key] = 1.0
            elif '5' in key and round(value, 2) == round(a, 2):
                M[key] = 1.0
            elif key == '4f' and round(value, 2) == round(a, 2):
                M[key] = 1.0
            else:
                print key, a, value
                x = raw_input()
                if len(x) > 0:
                    M[key] = float(x)
                else:
                    continue

        elif key == '3e':
            X = {'A': 0.5, 'D': 0.5, 'ACD': 0.5, 'AC': 0.5}
            if a in X:
                M[key] = X[a]
            else:
                print '3e: ~~~ ', a
                continue
        else:
            print key, a, value
            x = raw_input()
            if len(x) > 0:
                M[key] = float(x)
            else:
                continue
        pts += M[key] * POINTS[key]
        total += POINTS[key]

    print "%30s %.1f %.0f %.0f" % (name, pts * 100 / total, pts, total)
    results[name] = M

yaml.dump(results, open('results.yaml', 'w'))

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
