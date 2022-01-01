# https://programmerall.com/article/9902138764/

'''
Code example

 It's cold, Xiao Ming got up late today and doesn't want to go to work anymore.
  Prepare to ask the company for a leave. The company's leave process is as
  follows:
 1: 0 <x <3h Group leader can directly approve
 2: 3h <x <48h approved by department leaders
 3:48 <x The department leader needs to report to the boss for approval
'''

import abc


class AbsLeader(abc.ABC):

    def __init__(self):
        self._next = None

    #  Ask for leave
    @abc.abstractmethod
    def leave(self): ...

    #  Next processor
    @property
    def next(self):
        if (not self._next):
            raise Exception("No processing object")
        return self._next

    @next.setter
    def next(self, process):
        self._next = process


class GroupLeader(AbsLeader):
    def leave(self, hour: float):
        if hour < 3:
            print("ok, the leave leader approved")
        else:
            self.next.leave(hour)


class DepartmentLeader(AbsLeader):
    def leave(self, hour):
        if hour < 48:
            print("ok, the head of the leave department approved")
        else:
            self.next.leave(hour)


class BossLeader(AbsLeader):
    def leave(self, hour):
        if hour >= 48:
            print("ok, leave boss approved")


if __name__ == "__main__":
    #  Establish a chain of responsibility
    groupleader = GroupLeader()
    department = DepartmentLeader()
    boos = BossLeader()

    groupleader.next = department
    department.next = boos

    #  Ask for 1 hour leave, the team leader will handle it
    groupleader.leave(1)

    #  Ask for 45 hours off, the department will handle it
    groupleader.leave(45)

    #  Ask for 66 hours of leave, boss processing
    groupleader.leave(66)
