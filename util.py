import os
import collections

def sort_files(folder):
    X = collections.defaultdict(list)
    for f in sorted(os.listdir(folder)):
        full = folder + '/' + f
        parts = os.path.splitext(f)
        if parts[-1]=='.pdf':
            X['pdfs'].append(full)
        elif parts[-1]=='.yaml':
            if 'coords' in f:
                X['coords'].append(full)
            else:
                X['yaml'].append(full)
        elif f[0]=='.':
            continue        
        else:
            print "UNKNOWN", f                
    return X
