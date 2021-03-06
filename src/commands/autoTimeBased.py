import wpilib
import wpilib.drive
import networktables

class AutoTimeBased(wpilib.command.Command):
    def __init__(self):
        super().__init__("AutoTimeBased")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.Time_table = networktables.NetworkTables.getTable('/Time/')

    def initialize(self):
        self.time = wpilib.Timer()
        self.time.start()

    def timereset(self):
        self.time.reset()

    def motorset(self, power):
        self.drivetrain.motor_lb.set(power)
        self.drivetrain.motor_rb.set(-power)

    def motorturn(self, power):
        self.drivetrain.motor_rb.set(power)
        self.drivetrain.motor_lb.set(power)

    def execute(self):
        deltaTime = self.time.get()
        self.Time_table.putNumber("Time", deltaTime)
        self.motorset(0.2)
        if 5.0 <= self.time.get() <= 5.5:
            #should drive x feet then kills motor
            self.motorset(0)

        elif 5.5 <= self.time.get() <= 6.0:
            # waits for half a sec then hopefully turns clockwise
            self.motorturn(0.3)

        elif self.time.get() >= 6.0:
            #stops again
            self.drivetrain.off()

    def isFinished(self):
        if self.time.get() <= 15:
            return False
        elif self.time.get() > 15:
            return True

    def end(self):
        self.drivetrain.off()
        self.time.stop()
