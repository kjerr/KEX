import pickle

connections = pickle.load( open( "connections.p", "rb" ) )

def doesindexzeroexist(connections):
    for i in connections:
        for elem in i:
            for j in elem:
                if j == 0 or j>180:
                    return True
    return False

result = doesindexzeroexist(connections)

print(result)

# stringToReturn = str(connections[0][0])
# print(stringToReturn)




