from app.models.course import Course

# 1A
math109 = Course("MATH 109", "Math")
math100 = Course("MATH 100", "Math")
math110 = Course("MATH 110", "Math")
engr130 = Course("ENGR 130", "Engineering")
engr110 = Course("ENGR 110", "Engineering")
phys110 = Course("PHYS 110", "Physics", coreqs=[[math100, math109]])
csc111 = Course("CSC 111", "Computer Science")

# 1B
math101 = Course("MATH 101", "Math", prereqs=[[math100, math109]])
engr120 = Course("ENGR 120", "Engineering", prereqs=[[engr110]], coreqs=[[csc111]])
engr141 = Course("ENGR 141", "Engineering", prereqs=[[math100, math109]], coreqs=[[math110]])
phys111 = Course("PHYS 111", "Physics", prereqs=[[phys110]], coreqs=[[math100, math109]])
csc115 = Course("CSC 115", "Computer Science", prereqs=[[csc111]])

# Co-op
engr001 = Course("ENGR 001", "Engineering", prereqs=[[engr130], [engr110], [math100, math109]])

# 2A
chem101 = Course("CHEM 101", "Chemistry")
math122 = Course("MATH 122", "Math", prereqs=[[math100, math109]])
stat260 = Course("STAT 260", "Statistics", coreqs=[[math101]])
seng265 = Course("SENG 265", "Software Engineering", prereqs=[[csc115]])
ece255 = Course("ECE 255", "Electrical and Computer Engineering", prereqs=[[csc111]])
ece260 = Course("ECE 260", "Electrical and Computer Engineering", prereqs=[[math101], [math110]])
csc230 = Course("CSC 230", "Computer Science", prereqs=[[csc115]])

# 2B
econ180 = Course("ECON 180", "Economics", prereqs=[[math101]])
seng275 = Course("SENG 275", "Software Engineering", prereqs=[[seng265]])
seng310 = Course("SENG 310", "Software Engineering", prereqs=[[seng265]])
csc225 = Course("CSC 225", "Computer Science", prereqs=[[math122], [csc115]])
ece310 = Course("ECE 310", "Electrical and Computer Engineering", prereqs=[[ece260]])

# Co-op
engr002 = Course("ENGR 002", "Engineering", prereqs=[[engr001], [math122], [engr120]])
engr003 = Course("ENGR 003", "Engineering", prereqs=[[engr002]])
engr004 = Course("ENGR 004", "Engineering", prereqs=[[engr003]])

# 3A
seng321 = Course("SENG 321", "Software Engineering", prereqs=[[seng265]])
seng371 = Course("SENG 371", "Software Engineering", prereqs=[[seng275, seng321]])
csc226 = Course("CSC 226", "Computer Science", prereqs=[[csc225]])
csc361 = Course("CSC 361", "Computer Science", prereqs=[[csc230, ece255], [seng265]], coreqs=[[csc226]])
ece360 = Course("ECE 360", "Electrical and Computer Engineering", prereqs=[[ece260]])
ece458 = Course("ECE 458", "Electrical and Computer Engineering", prereqs=[[csc230, ece255]])

# 3B
seng350 = Course("SENG 350", "Software Engineering", prereqs=[[seng275]], required_year=2)
seng360 = Course("SENG 360", "Software Engineering", prereqs=[[seng265]], required_year=3)
csc320 = Course("CSC 320", "Computer Science", prereqs=[[csc226]])
csc355 = Course("CSC 355", "Computer Science", prereqs=[[math122], [csc230, ece255]])
csc360 = Course("CSC 360", "Computer Science", prereqs=[[csc230, ece255], [seng265]], coreqs=[[csc226]])
csc370 = Course("CSC 370", "Computer Science", prereqs=[[seng265], [csc226]])
ece355 = Course("ECE 355", "Electrical and Computer Engineering", prereqs=[[math122], [csc230, ece255]])

# 4A
seng426 = Course("SENG 426", "Software Engineering", prereqs=[[seng275], [seng321, seng371]])
seng440 = Course("SENG 440", "Software Engineering", prereqs=[[csc355, ece355]])
seng499 = Course("SENG 499", "Software Engineering", prereqs=[[engr002], [csc361, ece458], [csc370], [seng321], [seng350]])

# 4B
seng401 = Course("SENG 401", "Software Engineering", required_year=4)
csc460 = Course("CSC 460", "Computer Science", prereqs=[[csc355, ece355], [csc360]])
ece455 = Course("ECE 455", "Electrical and Computer Engineering", prereqs=[[csc355, ece355]])

course_list = [
    math109,
    math100,
    math110,
    engr130,
    engr110,
    phys110,
    csc111,
    math101,
    engr120,
    engr141,
    phys111,
    csc115,
    engr001,
    chem101,
    math122,
    stat260,
    seng265,
    ece255,
    ece260,
    csc230,
    econ180,
    seng275,
    seng310,
    csc225,
    ece310,
    engr002,
    engr003,
    engr004,
    seng321,
    seng371,
    csc226,
    csc361,
    ece360,
    ece458,
    seng350,
    seng360,
    csc320,
    csc355,
    csc360,
    csc370,
    ece355,
    seng426,
    seng440,
    seng499,
    seng401,
    csc460,
    ece455,
]
