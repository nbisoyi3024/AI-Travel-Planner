from graph.graph import build_graph

def test_supervisor_routing():
    graph = build_graph()

    result = graph.invoke({
                "input": "Find restaurants near CN Tower"
    })

    assert result is not None