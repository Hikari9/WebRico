# see http://www.mpi-sb.mpg.de/~sanders/programs/suffix/

def radixSort(a, b, r, n, K):
    # counter array
    c = [0] * (K + 1)
    #count occurences
    for i in xrange(n):
        c[r[a[i]]] += 1
    # exclusive sum prefix
    S = 0
    for i in xrange(K + 1):
        t = c[i]
        c[i] = S
        S += t
    # K'arrka'ainnen and P. Sanders
    for i in xrange(n):
        b[c[r[a[i]]]] = a[i] # sort
        c[r[a[i]]] += 1

# find the suffix array sa of s[0...n-1] in {1...K}^n
def DC3algorithm(s, sa, n, K):
    # sizes
    nL = (n + 2) // 3
    nM = (n + 1) // 3
    nR = n // 3
    nLR = nL + nR

    # dummy subarrays
    sL = [0] * nL
    saL = [0] * nL
    sMR = [0] * (nLR + 3)
    saMR = [0] * (nLR + 3)

    # radix sort those not divisible by 3
    j = 0
    for i in xrange(n + nL - nM):
        if i % 3 != 0:
            sMR[j] = i
            j += 1

    # swap indices
    radixSort(sMR, saMR, s[2:], nLR, K)
    radixSort(saMR, sMR, s[1:], nLR, K)
    radixSort(sMR, saMR, s, nLR, K)

    # assign bucket names
    name = 0
    c = [-1] * 3
    for i in xrange(nLR):
        equal = True
        for j in xrange(3):
            equal &= (c[j] == s[saMR[i] + j])
            c[j] = s[saMR[i] + j]
        if not equal: name += 1
        if saMR[i] % 3 == 1:
            sMR[saMR[i] // 3] = name
        else:
            sMR[saMR[i] // 3 + nL] = name


    # ternary partition
    if name < nLR:
        DC3algorithm(sMR, saMR, nLR, name)
        for i in xrange(nLR):
            sMR[saMR[i]] = i + 1
    else:
        for i in xrange(nLR):
            saMR[sMR[i] - 1] = i
    j = 0
    for i in xrange(nLR):
        if saMR[i] < nL:
            sL[j] = 3 * saMR[i]
            j += 1
    radixSort(sL, saL, s, nL, K)
    p, k, t = 0, 0, nL - nM
    while k < n:
        i = 3 * saMR[t] + 1 if saMR[t] < nL else 3 * (saMR[t] - nL) + 2
        j = saL[p]
        comp = ((s[i], sMR[saMR[t] + nL]) <= (s[j], sMR[j // 3])) if saMR[t] < nL else ((s[i], s[i + 1], sMR[saMR[t] - nL + 1]) <= (s[j], s[j + 1], sMR[j // 3 + nL]))
        if comp:
            sa[k] = i
            t += 1
            if t == nLR:
                k += 1
                while p < nL:
                    sa[k] = saL[p]
                    k += 1
                    p += 1
        else:
            sa[k] = j
            p += 1
            if p == nL:
                k += 1
                while t < nLR:
                    sa[k] = 3 * saMR[t] + 1 if saMR[t] < nL else 3 * (saMR[t] - nL) + 2
                    k += 1
                    t += 1
        k += 1


def DC3(text):
    if isinstance(text, (str, unicode)):
        text = map(ord, text)
    n = len(text)
    mn, mx = min(text), max(text)
    sn = [s - mn + 1 for s in text] + [0, 0, 0]
    sa = [0] * n
    DC3algorithm(sn, sa, n, mx - mn + 1)
    return sa
