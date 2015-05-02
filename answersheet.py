from pyPdf import PdfFileReader  # python-pypdf
from PythonMagick import *  # python-pythonmagick
import pygame, tempfile
import yaml
import argparse
import os
from util import *

DENSITY = 200
W = 800
H = 300

def load_answers(filename):
    input1 = PdfFileReader(file(filename))
    info = input1.getDocumentInfo()
    n = input1.getNumPages()
    a = []
    for i in range(n):
        a.append( Answers(filename, i))
    return a
    
class Answers:
    def __init__(self, filename, i):
        self.image = Image()
        self.image.density('%d' % DENSITY)
        self.image.read('%s[%d]' % (filename, i))
        
        temp = tempfile.NamedTemporaryFile(suffix='.png')
        self.image.write(temp.name)
        self.pimage = pygame.image.load(temp.name)
        temp.close()
        
    def draw(self, screen, C):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, W, H), 0)
        
        scaled = self.pimage
        screen.blit(scaled, (0, 0), ( C[0], C[1], C[2]-C[0], C[3]-C[1]))
        pygame.display.flip()
        
        

parser = argparse.ArgumentParser(description='Answer Sheet Reader')
parser.add_argument('folder')
args = parser.parse_args()

files = sort_files(args.folder)

coords = yaml.load(open( files['coords'][0] ))
pygame.init()    
screen = pygame.display.set_mode((W, H))

quit = False
prev = None


for fn in files['pdfs']:
    A = load_answers(fn)

    dfilename = fn + '.yaml'
    if os.path.exists( dfilename ):
        DATA = yaml.load(open(dfilename))
    else:
        DATA = []
        for i in range(len(A)):
            DATA.append({})

    for m in coords:
        key = m['name']
        C = m['coords']
        
        for i, p in enumerate(A):
            if key in DATA[i]:
                continue
            p.draw(screen, C)
            
            x = raw_input(key + '? ')
            if x == 'q' or x=='Q':
                quit = True
                break
            elif x=='l':
                x = prev
            elif x=='?':
                continue
            DATA[i][key] = x
            prev = x
        if quit:
            break

    yaml.dump(DATA, open(dfilename, 'w'))
