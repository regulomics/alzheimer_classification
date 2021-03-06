import numpy as np
import sys
sys.path.insert(0, '../')
import exceptions

'''
See readme.txt for input, output and possible options.
'''


def vcf_to_matrix(ch, inp, outdir):

    o = open(inp, 'r')

    line = o.readline()
    while line.startswith('##'):
        line = o.readline()

    p = open('%spid_chr%s.txt' % (outdir, ch), 'w')
    line = line.split()
    for pat, el in enumerate(line[9:]):
        p.write(el.strip() + '\n')
    pat += 1
    header = o.tell()
    p.close()

    for snp, _ in enumerate(o):
        pass
    snp += 1
        
    o.seek(header)

    s = open('%ssnps_chr%s.txt' % (outdir, ch), 'w')
    '''
    matrix = np.zeros(shape=(pat, snp, 2), dtype=np.int8)
    for i, line in enumerate(o):
    
        line = line.split()
        s.write('%s\t%s\t%s\n' % (line[1], line[3], line[4]))
        
        for j, e in enumerate(line[9:]):
            e = e.split(':')[0]
            try:
                v1, v2 = map(int, e.split("/"))
            except ValueError:
                try:
                    v1, v2 = map(int, e.split("|"))
                except ValueError:
                    v1, v2 = -1, -1
            matrix[j, i] = [v1, v2]
    np.save('%smatrix_chr%s.npy' % (outdir, ch), matrix)     
    '''

    X = np.zeros(shape=(pat, snp+1), dtype=np.int8)
    for i, line in enumerate(o):
        line = line.split()
        s.write('%s\t%s\t%s\n' % (line[1], line[3], line[4]))
        for j, e in enumerate(line[9:]):
            X[j][0] = j
            try:
                v = int(e.split(':')[0].replace('|', '/').split('/')[1])
            except ValueError:
                v = -1
            X[j, i+1] = v

    np.savetxt('%sX_chr%s.csv' % (outdir, ch), X, fmt='%d', delimiter=',',
               header=','+','.join(list(map(str, range(snp)))), comments='')
    o.close()
    s.close()

    return "%s\t%d\t%d" % (ch, snp, pat)


ch = '1'
outdir = './'
for q in range(len(sys.argv)):
    if sys.argv[q] == '-chr':
        ch = sys.argv[q+1]
    if sys.argv[q] == '-input':
        inp = sys.argv[q+1]
    if sys.argv[q] == '-outdir':
        outdir = sys.argv[q+1]

if 'inp' not in globals():
    raise exceptions.NoParameterError('inp', 'name of input file')

print(vcf_to_matrix(ch, inp, outdir))
