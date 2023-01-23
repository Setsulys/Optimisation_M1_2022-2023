def decRec(current, i, goal, res, longueurs):
    if i == 0:
        if goal < min(longueurs) :
            res.append(current)
        return 
    max = 0
    while max * longueurs[i] <= goal :
        current[i] = max
        decRec(current, i - 1, goal - longueurs[i] * max,res, longueurs)
        max +=1

def decoupe(entree, longueurs):
    res = []
    decRec([0]*len(longueurs),len(longueurs), entree, res, longueurs)
    print(res)

decoupe(300,[120,100,50])