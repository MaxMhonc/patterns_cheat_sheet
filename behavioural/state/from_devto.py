# https://dev.to/jemaloqiu/design-pattern-in-python-3-state-pattern-1ekh

from abc import ABCMeta, abstractmethod
import threading, time


# Singleton Decorator method
def singleton(cls):
    __instance = {}

    def __singleton(*args, **kwargs):

        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
        else:
            pass

        return __instance[cls]

    return __singleton


class Context():
    """Context base class"""

    def __init__(self, ContextName):
        self.__states = {}
        self.__currentState = None  # state name
        self.__name = ContextName

    def addState(self, state):
        self.__states[state.getName()] = state
        print("States: ", self.__states.keys())

    def setState(self, stateName):
        if stateName in self.__states:
            self.__currentState = self.__states[stateName]
        else:
            print("Error: unknown state: {}".format(stateName))

    def getState(self):
        return self.__currentState

    def getContextName(self):
        return self.__name

        # message driven transition

    def doTransition(self, msg):
        current = self.__currentState.getName()
        if msg["from"] == current:
            print("Transition from {} to {}".format(msg["from"], msg["to"]))
            self.exitBehavior(self.__states[msg["from"]])
            self.setState(msg["to"])
            self.entryBehavior(self.__states[msg["to"]])
        else:
            print(
                "Error: Current State is {}, received transition from {} to {}".format(
                    current, msg["from"], msg["to"]))

    # Behavior upon entry of a new state
    def entryBehavior(self, toState):
        if isinstance(toState, State):
            toState.onEntryBehavior(self)

    # Behavior upon exit of present state
    def exitBehavior(self, fromState):
        if isinstance(fromState, State):
            fromState.onExitBehavior(self)


class State(metaclass=ABCMeta):
    """State base class"""

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    @abstractmethod
    def onEntryBehavior(self, CANOpen_Node):
        pass

    @abstractmethod
    def onExitBehavior(self, CANOpen_Node):
        pass


@singleton
class InitializationState(State):

    def __init__(self, name):
        super().__init__(name)

    def onEntryBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Start dispatching heartbeat msg of state - {}".format(nn,
                                                                          sn))

    def onExitBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Stop dispatching  heartbeat msg of state - {}".format(nn,
                                                                          sn))


@singleton
class PreOperationalState(State):

    def __init__(self, name):
        super().__init__(name)

    def onEntryBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Start dispatching heartbeat msg of state - {}".format(nn,
                                                                          sn))

    def onExitBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Stop dispatching  heartbeat msg of state - {}".format(nn,
                                                                          sn))


@singleton
class OperationalState(State):

    def __init__(self, name):
        super().__init__(name)

    def onEntryBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Start dispatching heartbeat msg of state - {}".format(nn,
                                                                          sn))

    def onExitBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Stop dispatching  heartbeat msg of state - {}".format(nn,
                                                                          sn))


@singleton
class StoppedState(State):

    def __init__(self, name):
        super().__init__(name)

    def onEntryBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Start dispatching heartbeat msg of state - {}".format(nn,
                                                                          sn))

    def onExitBehavior(self, context):
        nn = context.getContextName()
        sn = self.getName()
        print("[{}] Stop dispatching  heartbeat msg of state - {}".format(nn,
                                                                          sn))


class CANOpen_Node(Context):
    """
    Simulated CANOpen 301 Node class
    """

    def __init__(self, ContextName):
        super().__init__(ContextName)

        self.addState(InitializationState("State_Initialization"))
        self.addState(PreOperationalState("State_PreOperational"))
        self.addState(OperationalState("State_Operational"))
        self.addState(StoppedState("State_Stopped"))
        self.__active = False
        self.__thread = threading.Thread(target=self.communication)
        self.__timer = 0

    def PowerOn(self):

        if self.__thread.isAlive():
            pass
        else:
            self.__active = True
            print("Power is ON!")
            self.setState("State_Initialization")
            print("Automatically entering State_Initialization!")
            self.__thread.start()

    def PowerOff(self):
        self.__active = False
        print("Calling Power Off!")

    def communication(self):
        while self.__active:
            print("[HeartBeat] Node {} is in {}".format(self.getContextName(),
                                                        self.getState().getName()))
            time.sleep(1)
            self.__timer += 1
        print("Power is Off!")


## State transition msgs
msg12 = {"from": "State_Initialization", "to": "State_PreOperational"}
msg21 = {"from": "State_PreOperational", "to": "State_Initialization"}
msg23 = {"from": "State_PreOperational", "to": "State_Operational"}
msg32 = {"from": "State_Operational", "to": "State_PreOperational"}
msg34 = {"from": "State_Operational", "to": "State_Stopped"}
msg43 = {"from": "State_Stopped", "to": "State_Operational"}
msg42 = {"from": "State_Stopped", "to": "State_PreOperational"}
msg24 = {"from": "State_PreOperational", "to": "State_Stopped"}

## simulate a ring buffer for msgs
msgQ = [(msg12, 6), (msg23, 7), (msg32, 22), (msg34, 25), (msg24, 28)]

if __name__ == "__main__":

    Simulated_Node = CANOpen_Node("Node_Lidar_2020")
    step = 0
    buffer_head = 0
    while (True):

        if step == 3:
            Simulated_Node.PowerOn()
        if step == 30:
            Simulated_Node.PowerOff()
            break

        if step == msgQ[buffer_head][1]:
            Simulated_Node.doTransition(msgQ[buffer_head][0])
            buffer_head += 1
            if buffer_head == len(msgQ):
                buffer_head = 0

        time.sleep(1)
        step += 1
        print("========= step {} =========".format(step))
