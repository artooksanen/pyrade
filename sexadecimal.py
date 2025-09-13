import string

def splitrade(s):
    if len(s.split('+')) == 2:
        return s.split('+')[0],"+"+s.split('+')[1]
    if len(s.split('-')) == 2:
        return s.split('-')[0],"-"+s.split('-')[1]
    return None,None
    
def parse(s):
#    print("\ninput:",s)
    sr,sd=splitrade(s)
#    print("sr=",sr)
    if sr!=None and sd!=None:
        r=subparse(sr)
#    print("r:",r)
#    print("sd=",sd)
        d=subparse(sd)
#    print("d:",d)
        return r,d
    else:
       return None,None

def subparse(s):
    ptr=0
    h1=h2=h3=h4=h5=h6=0
    rd1=rd2=rd3=rd4=0
    d1=d2=d3=d4=d5=d6=0
    dd1=dd2=dd3=dd4=0
    sign=1

    if s[ptr]=='-':
      sign=-1
      ptr=ptr+1
    if s[ptr]=='+':
      sign=1
      ptr=ptr+1      

    if s[ptr].isnumeric():
        h2=int(s[ptr])
        #print("1. numero on ",h2)
        ptr=ptr+1
    
    if len(s)>ptr:
      if s[ptr].isnumeric():
        h1=h2
        h2=int(s[ptr])
        #print("2. numero on ",h2)
        ptr=ptr+1
        
    if len(s)>ptr:
        while len(s)>ptr and (s[ptr]==' ' or s[ptr]==':'):
            ptr=ptr+1
    
    if len(s)>ptr:
      if s[ptr].isnumeric():
        h3=int(s[ptr])
        #print("3. numero on ",h3)
        ptr=ptr+1
    if len(s)>ptr:
      if s[ptr].isnumeric():
        h4=int(s[ptr])
        #print("4. numero on ",h4)
        ptr=ptr+1

    if len(s)>ptr:
      while len(s)>ptr and (s[ptr]==' ' or s[ptr]==':'):
        ptr=ptr+1
    
    if len(s)>ptr:
      if s[ptr].isnumeric():
        h5=int(s[ptr])
        #print("5. numero on ",h5)
        ptr=ptr+1

    if len(s)>ptr:
      if s[ptr].isnumeric():
        h6=int(s[ptr])
        #print("6. numero on ",h6)
        ptr=ptr+1

    if len(s)>ptr:
     if ptr<len(s):
      if s[ptr]=='.':
        ptr=ptr+1
        if len(s)>ptr and s[ptr].isnumeric():
            rd1=int(s[ptr])
            ptr=ptr+1
        if len(s)>ptr and s[ptr].isnumeric():
            rd2=int(s[ptr])
            ptr=ptr+1
        if len(s)>ptr and s[ptr].isnumeric():
            rd3=int(s[ptr])
            ptr=ptr+1
        if len(s)>ptr and s[ptr].isnumeric():
            rd4=int(s[ptr])
            ptr=ptr+1
            
    ra=(h1*10+h2+(h3*10+h4)/60.0+(h5*10+h6)/3600.0+rd1/10.0+rd2/100.0+rd3/1000.0+rd4/10000.0)*sign

    return ra




if __name__ == '__main__':

        print(parse("123456 +123456"))    
        print(parse("123456+123456"))    
        print(parse("123456-123456"))
        print(parse("123456 123456"))        
        print(parse("123456+1234"))    
        print(parse("12 34 56 -12 34 56"))    
        print(parse("12:34:56 -12:34:56"))    
        print(parse("12:34 +12:34"))    
        print(parse("12.56 -12.34"))    
        print(parse("12+10"))
        print(parse("1-0"))    