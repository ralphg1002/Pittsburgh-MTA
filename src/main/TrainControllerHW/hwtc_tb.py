import hwtc_main as hwtc


def hwtc_tb():
    train = hwtc.HWTrainController("Tester Train")
    for i in range(5):
        train.UpdateController(1, (10 * (i + 1)), (10 * (i + 1) - 10), i % 2, [0, 0, 0])
        EBrake = train.BrakeStates()[0]
        SBrake = train.BrakeStates()[1]
        power = train.sendPower()
        # There will probably need to be a delay here after arduino communication is implemented
        print(power)

        # Do all the train model's physics stuff
    for i in range(4):
        train.UpdateController(1, 50 - (i * 10), 50 - (i * 10) + 10, (i+1) % 2, [0, 0, 0])
        EBrake = train.BrakeStates()[0]
        SBrake = train.BrakeStates()[1]
        power = train.sendPower()
        print(power)

        # Do all the train model's physics stuff
    train.SetBeaconData("Yard", "Dormont", "randomNext", '01')
    train.UpdateController(0, 0, 0, 1, [0, 0, 0])
    print(train.getAnnouncement())

hwtc_tb()
