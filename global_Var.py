class GlobalVar:  # 全局变量类
    def __init__(self):
        self.stop_0_flag = 0  # 正常退出信号，即一轮结束,为0表示正常
        self.stop_1_flag = 0  # 非正常退出信号，即出现bug,为0表示正常

    def init_0(self):
        self.stop_0_flag = 0

    def set_0(self):
        self.stop_0_flag = 1

    def set_1(self):
        self.stop_1_flag = 1

    def if_out(self):
        if self.stop_0_flag or self.stop_1_flag:
            return 1  # 有一个为1，返回1，表示当前两个线程都应该结束
        else:
            return 0  # 全为0，返回0，表示当前两个线程正常

    def if_error(self):
        if self.stop_1_flag:
            return 1
        else:
            return 0


def create():  # 创建一个全局变量类的对象
    global g  # 该对象是一个全局变量，这样通过global_var.g就可以调用，而不必执行create函数g=GlobalVar()
    g = GlobalVar()
