class Student:
    def __init__(self,name,chinese,math,englise):
        self.name=name
        self.chinese=chinese
        self.math=math
        self.englise=englise

    def update(self,chinese=None,math=None,englise=None):
        if(chinese is not None):
            self.chinese=chinese
        if(math is not None):
            self.math=math
        if(englise is not None):
            self.englise=englise
    def get(self):
        print(f"姓名：{self.name} | {self.chinese} | {self.math} | {self.englise}")

class Edu:
    def __init__(self):
        self.stu_list=[]

    #增
    def add(self):
        stuname=input("请输入学生姓名")
        for i in self.stu_list:
            if(i.name==stuname):
                print("该学生已存在，添加失败!")
                return

        stuchinese=int(input("请输入语文成绩"))
        stumath=int(input("请输入数学成绩"))
        stuenglise=int(input("请输入英语成绩"))

        if stumath<0 or stumath>150 or stuchinese<0 or stuchinese>150 or stuenglise<0 or stuenglise>150:
            print("输入成绩有误，添加失败!")
            return

        print("学生信息添加成功")
        stu=Student(stuname,stuchinese,stumath,stuenglise)
        self.stu_list.append(stu)

    #删
    def remove(self):
        stuname=input("请输入学生姓名")
        for i in self.stu_list:
            if(i.name==stuname):
                self.stu_list.remove(i)
                print("删除成功!")
                return
        print("该学生不存在，删除失败!")

    #改
    def updata(self):
        stuname = input("请输入学生姓名")
        for i in self.stu_list:
            if(i.name==stuname):
                stuchinese = int(input("请输入语文成绩"))
                stumath = int(input("请输入数学成绩"))
                stuenglise = int(input("请输入英语成绩"))

                if stumath < 0 or stumath > 150 or stuchinese < 0 or stuchinese > 150 or stuenglise < 0 or stuenglise > 150:
                    print("输入成绩有误，添加失败!")
                    return

                print("学生信息修改成功")
                Student(i,stuchinese,stumath,stuenglise)
                return
        print("该学生不存在，修改失败!")

    #查
    def find(self):
        stuname = input("请输入学生姓名")
        for i in self.stu_list:
            if(i.name==stuname):
                Student.get(i)
                return
        print("该学生不存在，查询失败!")

    #输出全部
    def get(self):
        for i in self.stu_list:
            print(i)

edu=Edu()

while(True):
    print("1.添加学生 2.删除学生 3.修改学生 4.查询学生 5.输出全部")
    i=input()
    match i:
        case "1":
            edu.add()
        case "2":
            edu.remove()
        case "3":
            edu.updata()
        case "4":
            edu.find()
        case "5":
            edu.get()