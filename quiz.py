from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb4IjmgCyaG7hWuKIQ2cVEUyX2j3eE2nn_OvKPZllq21xU1BngIXwccM4JExq3qjzno6Mzm5vq-PyjayTZ-iuXyEGC0Fkw0MsDjmjimRfoAUZgawgZ96KQpJSPCBo1bujrBXezD0ZL2_574lyBA__ZXIRYUuQEOCW2CCfTBfU1AsJ52VI='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
