kohteet={}

def lue(filename):
    f = open(filename, 'r', encoding="utf-8")
    kohteet.clear()
    for line in f.read().splitlines():
        if len(line.split(" ",1)) > 1:
            nimi=line.split(" ",1)[0].upper()
            arvo=line.split(" ",1)[1].upper()
            print("nimi:",nimi,"arvo:",arvo)
            kohteet.update({nimi:arvo})
    print("kohteet:",kohteet)
def hae(nimi):
    return kohteet.get(nimi.upper())


if __name__=="__main__":

    lue("omat.dat")
    print("j",hae("j"))    
    print("J",hae("j"))    
    print("harju", hae("harju"))    
    print("HARJU", hae("harju"))    
    print("harjus", hae("harjus"))    
    