from pyjanssen import MCM, FORWARD, BACKWARD

if __name__ == "__main__":
    m = MCM(server=True,verbose=True)
    m.get_position(2)
    m.move(2,BACKWARD,steps=1)
