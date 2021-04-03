from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



from datetime import datetime, timedelta

def start(session):

    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

        res = int(input())
        today = datetime.today()
        days = { 0: "Monday", 1: "Tuesday", 2 :"Wednesday", 3: "Thursday", 4: "Friday", 5 : "Saturday", 6: "Sunday"}
        if res == 1:
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if len(rows) == 0:
                print()
                print(f"Today {today.day} {today.strftime('%b')}:")
                print("Nothing to do!")
                print()

            else:
                print(f"Today {today.day} {today.strftime('%b')}: ")
                for i in rows:
                    print(f"\n{i.id}. {i.task}")
        if res == 2:
            for i in range(8):
                tt = today + timedelta(days=i)
                rows = session.query(Table).filter(Table.deadline == tt.date()).all()
                if len(rows) == 0:
                    print(f"""\n{days[tt.weekday()]} {tt.day} {tt.strftime('%b')}: \nNothing to do!
                    """)
                else:
                    for i in rows:
                        dd = datetime.strptime(str(i.deadline), '%Y-%m-%d')
                        print()
                        print(f"{days[dd.weekday()]} {dd.day} {dd.strftime('%b')}: ")
                        print(f"{i.id}. {i.task}")
        if res == 3:
            print()
            print("All tasks:")
            rows = session.query(Table).order_by(Table.deadline).all()
            for i in rows:
                dd = datetime.strptime(str(i.deadline), '%Y-%m-%d')
                print(f"{i.id}. {i.task}. {dd.day} {dd.strftime('%b')}")
            print()
        if res == 4:
            print()
            print("Missed tasks:")
            rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
            if len(rows) == 0:
                print("Nothing is missed!")
            else:
                for i in rows:
                    dd = datetime.strptime(str(i.deadline), '%Y-%m-%d')
                    print(f"{i.id}. {i.task}. {dd.day} {dd.strftime('%b')}")
            print()
        if res == 5:
            print()
            print("Enter task")
            tt = input()
            print("Enter deadline")
            dead = input()
            new_row = Table(task=tt, deadline=datetime.strptime(dead, '%Y-%m-%d'))
            session.add(new_row)
            session.commit()
            print("The task has been added!")
            print()
        if res == 6:
            print()
            rows = session.query(Table).order_by(Table.deadline).all()
            print("Choose the number of the task you want to delete:")
            if len(rows) == 0:
                print("Nothing to delete")
            else:
                for i in rows:
                    dd = datetime.strptime(str(i.deadline), '%Y-%m-%d')
                    print(f"{i.id}. {i.task}. {dd.day} {dd.strftime('%b')}")
                num = int(input())
                specific_row = rows[num-1]
                session.delete(specific_row)
                print("The task has been deleted!")
                session.commit()

            print()
        if res == 0:
            print()
            print("Bye!")
            break

start(session)
