import sys
import os
import subprocess
from ResultParser import ResultParser
from pprint import pprint as pp

TESTCASESPATH = "../testcases/step4/input"

GOLDCOMPILERPATH = "../goldCompilers/step5/"
TINYPATH = "../tiny"

BASEOUTPUTDIR = "output/"
BASELOGDIR = "logs/"

COMPILEROUTPUT = BASEOUTPUTDIR + "compiledOutput/"
GOLDCOMPILEROUTPUT = COMPILEROUTPUT + "gold/"
ACTUALCOMPILEROUTPUT = COMPILEROUTPUT + "actual/"

TINYOUTPUT = BASEOUTPUTDIR + "tinyOutput/"
GOLDTINYOUTPUT = TINYOUTPUT + "gold/"
ACTUALTINYOUTPUT = TINYOUTPUT + "actual/"


def setupDirectoryStructure():
    directoryNames = [BASELOGDIR, BASEOUTPUTDIR, COMPILEROUTPUT, GOLDCOMPILEROUTPUT, ACTUALCOMPILEROUTPUT, TINYOUTPUT, GOLDTINYOUTPUT, ACTUALTINYOUTPUT]
    for directoryName in directoryNames:
        if not os.path.isdir(directoryName):
            os.mkdir(directoryName)


def runCompiler(input_file, gold=False):
    if gold:
        args = ['java', '-cp', GOLDCOMPILERPATH + 'antlr/:' + GOLDCOMPILERPATH, 'Micro', os.path.join(TESTCASESPATH, input_file)]
        compiler_output = GOLDCOMPILEROUTPUT
    else:
        args = ['../Micro',  os.path.join(TESTCASESPATH, input_file)]
        compiler_output = ACTUALCOMPILEROUTPUT

    runProc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = runProc.communicate()
    compiled_output = os.path.join(compiler_output, input_file.replace(".micro", ".tiny"))
    open(compiled_output, 'w').write(str(output))
    return compiled_output

def runTiny(input_file, gold=False):
    pass


# Runs the compiler against the input_files
def runGoldCompilerAndTiny(input_files):
    for fileName in input_files:
        # Run goldCompiler
        # runProc = subprocess.Popen(['java', '-cp', GOLDCOMPILERPATH + 'antlr/:' + GOLDCOMPILERPATH, 'Micro', os.path.join(TESTCASESPATH, fileName)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output, error = runProc.communicate()
        # goldCompiledOutput = os.path.join(GOLDCOMPILEROUTPUT, fileName.replace(".micro", ".tiny"))
        # outFile = open(goldCompiledOutput, "w")
        # outFile.write(output)
        # outFile.close()

        goldCompiledOutput = runCompiler(fileName, gold=True)

        # Run tiny on the gold compiled output
        runProc = subprocess.Popen([TINYPATH, goldCompiledOutput], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=open(os.path.join(TESTCASESPATH, fileName.replace(".micro", ".input"))) if os.path.exists(os.path.join(TESTCASESPATH, fileName.replace(".micro", ".input"))) else None )
        output, error = runProc.communicate()
        goldTinyOutput = os.path.join(GOLDTINYOUTPUT, fileName.replace(".micro", ".out"))
        outFile = open(goldTinyOutput, "w")
        outFile.write(output)
        outFile.close()
    return


# Run gold compiler and tiny
def runActualCompilerAndTiny(input_files):
    for fileName in input_files:
        # Run Actual Compiler
        # runProc = subprocess.Popen(['../Micro',  os.path.join(TESTCASESPATH, fileName)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output, error = runProc.communicate()
        # compiledOutput = os.path.join(ACTUALCOMPILEROUTPUT, fileName.replace(".micro", ".tiny"))
        # outFile = open(compiledOutput, "w")
        # outFile.write(output)
        # outFile.close()

        compiledOutput = runCompiler(fileName)

        # Run tiny on our compiled output
        runProc = subprocess.Popen([TINYPATH, compiledOutput], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=open(os.path.join(TESTCASESPATH, fileName.replace(".micro", ".input"))) if os.path.exists(os.path.join(TESTCASESPATH, fileName.replace(".micro", ".input"))) else None )
        output, error = runProc.communicate()
        tinyOutput = os.path.join(ACTUALTINYOUTPUT, fileName.replace(".micro", ".out"))
        outFile = open(tinyOutput, "w")
        outFile.write(output)
        outFile.close()


def getTinyOutput(input_file, path=ACTUALTINYOUTPUT):
    return open(os.path.join(path, input_file.replace(".micro", ".out"))).readlines()


def compareTinyOutput(input_files):
    for fileName in input_files:
        actualOutput = getTinyOutput(fileName)[0]
        goldOutput = getTinyOutput(fileName, path=GOLDTINYOUTPUT)[0]
        if actualOutput == goldOutput:
            print(fileName + " PASSED")
        else:
            print(fileName + " FAILED")
            # print("ACTUALOUTPUT: " + actualOutput)
            # print("GOLDOUTPUT: " + goldOutput)


# Gets all the files that are going to be tested
def getFileNames():
    input_files = []
    inputArg = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "all" else None
    if inputArg is None:
        input_files = [f for f in os.listdir(TESTCASESPATH) if os.path.isfile(os.path.join(TESTCASESPATH, f)) and ".micro" in f]
    else:
        input_files.append(inputArg)

    return input_files


def main():
    # parse args
    input_files = getFileNames()

    # setup directory structure
    setupDirectoryStructure()

    # scripting
    # run .micro and tiny on your file
    runActualCompilerAndTiny(input_files)

    # run gold compiler
    runGoldCompilerAndTiny(input_files)

    # compare output
    compareTinyOutput(input_files)
    # inputs to nico / outputs of Manish
    # input_files -- [List of ~~~~~ALL THE FILE NAMES~~~~~~ lol file names or just the one specified]

    # parsing
    # output dictionary {input_file_name : TestLogEntry()}
    result_parser = ResultParser()
    result_parser.parse_results(input_files)

    pp(result_parser.logs)
    # logging
    loggers = []

    for f in input_files:
        logger = TestLogger(file_name=f)
        logger.add_entry_to_log(result_parser.logs[f])
        loggers.append()

if __name__ == '__main__':
    main()
