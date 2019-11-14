class Activity:
    def __init__(
        self, id, defid, executionid, procdefid,
        child_procinstid, taskid
    ):
        self.id = id
        self.defid = defid
        self.executionid = executionid
        self.procdefid = procdefid
        self.child_procinstid = child_procinstid
        self.taskid = taskid
