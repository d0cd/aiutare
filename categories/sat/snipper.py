from glob import glob
import errno

# Define directory to file locations
# Backslashes requires two to have one in a string
path = ".\\Files\\*.cnf"
files = glob(path)

# Loop through all the files
for name in files:
    try:
        with open(name, "r") as f:
            # read all the lines seperately and put it into an array
            arrLines = f.readlines()
        with open(name, "w") as f:
            endIndex=0
            # Find the index of last non-empty line
            for i in range(len(arrLines)):
                if arrLines[i].strip("\n")!="":
                    endIndex=i
            counter =-1
            for line in arrLines:
                counter+=1
                # Add one line at a time until we reach the part that we want to remove or the end
                if line.strip("\n") == "%" or line.strip("\n") == "0" or counter>endIndex:
                    f.write("")
                    break
                f.write(line)
    except IOError as exc:
        # If there's exception, raise exception
        if exc.errno != errno.EISDIR:
            raise