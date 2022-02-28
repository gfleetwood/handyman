from sys import argv

def add(a,b):
  return(a+b)
  
def main():

  args = [int(x) for x in argv[1:]]
  print(add(*args))
  
if __name__=="__main__":
  main()
