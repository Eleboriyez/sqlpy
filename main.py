import psycopg2
from random import randint
from datetime import date


class Employee:
    def __init__(self, name, age, speciality, list_of_jobs, code):
        self.name = name
        self.age = age
        self.speciality = speciality
        self.list_of_jobs = list_of_jobs
        self.code = code


class Registry:
    def __init__(self, employees, companies):
        connection = psycopg2.connect(database="postgres",
                                      user="postgres",
                                      password="password",
                                      host="localhost",
                                      port="5432"
                                      )
        cur = connection.cursor()
        cur.execute("DROP TABLE IF EXISTS COMPANIES")
        cur.execute('''CREATE TABLE IF NOT EXISTS COMPANIES  
             (ID SERIAL PRIMARY KEY,
             NAME_COMPANY TEXT NOT NULL,
             INFO CHAR(50));''')
        for i in range(companies):
            name = "MacroSoftware: branch " + str(i + 1)
            info = str(randint(40, 100) * 1000) + ' ' + str(randint(40, 100) * 1000) + ' ' + str(
                randint(40, 100) * 1000) + ' ' + str(randint(40, 100) * 1000) + ' ' + str(
                randint(40, 100) * 1000) + ' ' + str(randint(40, 100) * 1000)
            cur.execute('''INSERT INTO COMPANIES (NAME_COMPANY, INFO) VALUES 
                (%s, %s)''', (name, info))
        connection.commit()
        cur.execute("DROP TABLE IF EXISTS JOURNAL")
        cur.execute('''CREATE TABLE IF NOT EXISTS JOURNAL  
             (ID SERIAL PRIMARY KEY,
             EMPLOYEE_NAME TEXT NOT NULL,
             ID_COMPANY TEXT NOT NULL,
             START_DATE TEXT NOT NULL,
             SPECIALITY TEXT NOT NULL,
             SALARY TEXT NOT NULL,
             END_DATE TEXT NOT NULL)''')
        for employee in employees:
            for k in employee.list_of_jobs:
                cur.execute('''SELECT INFO FROM COMPANIES
                            WHERE ID = {}'''.format(str(k)))
                info = cur.fetchall()
                salary = info[0][0].split(' ')[employee.code]
                start = date.fromordinal(randint(730120, 733772)).isoformat()
                end = date.fromordinal(randint(734503, 738520)).isoformat()
                cur.execute('''INSERT INTO JOURNAL (EMPLOYEE_NAME, ID_COMPANY, START_DATE, SPECIALITY, SALARY, END_DATE) VALUES
                    (%s, %s, %s, %s, %s, %s)''', (employee.name, str(k), start, employee.speciality, salary, end))
        connection.commit()
        cur.execute("SELECT * FROM JOURNAL")
        for row in cur.fetchall():
            print(*row)
        connection.close()


def main():
    names = ['John', 'Sam', 'Nicole', 'Mike', 'Kate', 'Iris']
    specs = ['Data Analyst', 'FE Dev', 'BE Dev', 'DevOps', 'Lead Designer', 'CyberSec']
    companies = 15
    employees = []
    for _ in range(20):
        code = randint(0, 5)
        cur_list = [randint(1, companies) for _ in range(randint(1, 3))]
        employees.append(Employee(names[randint(0, 5)], randint(20, 45), specs[code], cur_list, code))
    Registry(employees, companies)


if __name__ == "__main__":
    main()
