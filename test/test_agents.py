from core.agents import planner_agent

def test_planner_agent_returns_response():

    response = planner_agent({
       "input": "Create a 3 day Toronto itinerary"
    })

    assert response is not None
   