from domain.graph import Graph


def test():
    connections = [('car', 'machine'), ('car', 'limo'), ('machine', 'car'), ('machine', 'auto'),
                        ('limo', 'car'), ('limo', 'wheels')]
    graph = Graph(connections, directed=False)
    print(graph.__str__())
    print("==========")
    print(graph.find("car"))
    graph.add("algorithm", "technique")
    graph.add("algorithm", "mathematic")
    print(graph.__str__())
    print(graph.find("algorithm"))
    graph.remove("algorithm")
    print("==========")
    print(graph.__str__())
    print(graph.find("mathematic"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()
