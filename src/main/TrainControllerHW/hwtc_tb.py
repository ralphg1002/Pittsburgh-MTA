import hwtc_main as hwtc
import time


def hwtc_tb():
    train = hwtc.HWTrainController("Tester Train", 1)
    train.enable()
    time.sleep(5)
    for i in range(5):
        train.UpdateController(1, 40, (10 * (i + 1) - 10), i % 2, [0, 0, 0])
        EBrake = train.BrakeStates()[0]
        SBrake = train.BrakeStates()[1]
        time.sleep(0.5)
        power = train.sendPower()
        # There will probably need to be a delay here after arduino communication is implemented
        print(power)

        # Do all the train model's physics stuff
    for i in range(4):
        train.UpdateController(1, 40, 40 - (i * 10) + 10, (i+1) % 2, [0, 0, 0])
        EBrake = train.BrakeStates()[0]
        SBrake = train.BrakeStates()[1]
        time.sleep(0.5)
        power = train.sendPower()
        print(power)

        # Do all the train model's physics stuff
    train.SetBeaconData("Yard", "Dormont", "randomNext", '01')
    train.UpdateController(0, 0, 0, 1, [0, 0, 0])

hwtc_tb()
