import traci

# Define the SUMO command with a valid configuration file
sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "intersection.sumocfg"]

# Start SUMO in a separate process
try:
    traci.start(sumoCmd)
except traci.exceptions.FatalTraCIError as e:
    print("Failed to start SUMO:", e)
    exit(1)

# Get all edges and traffic lights in the network
try:
    edges = traci.edge.getIDList()
    traffic_lights = traci.trafficlight.getIDList()

    print("Edges:", edges)
    print("Traffic Lights:", traffic_lights)
except traci.exceptions.TraCIException as e:
    print("Error accessing SUMO data:", e)
    traci.close()
    exit(1)

# Simulation loop to check basic operations
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()  # Step through the simulation

# Close the SUMO process
traci.close()
