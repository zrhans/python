import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print('test.py -i <arq_entrada> -o <arq_saida>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <arq_entrada> -o <arq_saida>')
         sys.exit();
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
    print('Arquivo de Entrada: "', inputfile)
    print('Arquivo de Saida  : "', outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])