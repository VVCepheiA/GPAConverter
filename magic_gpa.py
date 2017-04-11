import os

tmp_file = "tmp"

# A quick and ugly script to calculate GPA cause I am too lazy
# Don't judge

# Source: https://www.ouac.on.ca/guide/omsas-conversion-table/
def to_gpa(grade):
    if grade >= 90:
        return 4.0
    elif grade >= 85:
        return 3.9
    elif grade >= 80:
        return 3.7
    elif grade >= 77:
        return 3.3
    elif grade >= 73:
        return 3.0
    elif grade >= 70:
        return 2.7
    elif grade >= 67:
        return 2.3
    else:
        raise Exception("Too lazy to type on... Just try not to get here :)")

def remove_tmp_file(tmp_file):
    try:
        os.remove(tmp_file)
    except OSError:
        pass

remove_tmp_file(tmp_file)

# output
os.system("pdf2txt.py -o tmp transcripts/Quest.pdf")

# if major is None, calculate the overall GPA
# if major is a set of major code (ex. CS, SE...), calculate major GPA only
def print_stats(major = None):
    global tmp_file
    count = 0
    total_GPA = 0
    with open(tmp_file) as f:
        content = f.read().splitlines()
        for line in content:
            line = line.split()
            try:
                mark = int(line[-3])
                # ignore the header or work term report or PD
                if mark > 100 or line[0] == "WKRPT" or line[0] == "PD":
                    continue
                # ignore the non major if calculating major GPA
                ignore = "IGNORED" if (major is not None and line[0] not in major) else "COUNTED"
                print line[0], line[1], mark, ignore
                if major is not None and line[0] not in major:
                    continue
                if line[-4] == '0.50/0.50':
                    total_GPA += to_gpa(mark)
                    count += 1
                elif line[-4] == '0.25/0.25':
                    total_GPA += to_gpa(mark) * 0.5
                    count += 0.5
                else:
                    print "Error in reading", line
                    raise Exception("Unexpected credit, check the code bro")
            except (ValueError, IndexError) as e:
                # naturally drop the DRNA
                pass

        print "************************************************************"
        if major is None:
            print "Overall Courses Stats:"
        else:
            print "Major Courses Stats:"
            print "Your selected majors are:", list(major)
        print "#course:", count
        print "GPA:", total_GPA/ count
        print "************************************************************"

# overall
print_stats()
# major
print_stats(set(['SE', 'CS', 'MATH']))

remove_tmp_file(tmp_file)