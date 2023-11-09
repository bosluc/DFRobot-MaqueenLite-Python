import microbit
import machine
import lib_robot_maqueen as mqn
import time

mq = mqn.MaqueenPlus()

#### Example #####

while True:
  mq.move("F", 70)
  time.sleep(1)
  mq.move("R", 70)
  time.sleep(1)

##################
