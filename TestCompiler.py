import sys

# Runs the compiler against the input_files
def runCompiler(input_files):
    pass
    
# Gets all the files that are going to be tested
def getFileNames():
    inputArg =  sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "all" else None
    if inputArg is None:
        pass
    

def main():
    # parse args (this first) actual code??
    input_files = getFileNames()

    # scripting
         
    # run .micro
    runCompiler(input_files) 
    # run tiny
    
    # inputs to nico / outputs of Manish 
    # input_files -- [List of ~~~~~ALL THE FILE NAMES~~~~~~ lol file names or just the one specified]

    # parsing
    
    # output dictionary {input_file_name : TestLogEntry()}
    
    # logging
    
    loggers = [TestLogger(name=f) for f in input_files]
    
    
   
if __name__ == '__main__':
    main() 
    
    



    
   