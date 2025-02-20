class PerformanceEnv(gym.Env):
    def __init__(self, vm_data, workflow_data):
        self.vm_data = vm_data
        self.workflow_data = workflow_data
        self.state = self.initialize_state()
        self.action_space = gym.spaces.Discrete(len(vm_data))  # Assign to one of the VMs
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(self.state),), dtype=np.float32)
    
    def step(self, action):
        selected_vm = self.vm_data[action]
        reward, done = self.calculate_reward(selected_vm)
        self.state = self.update_state(selected_vm)
        return self.state, reward, done, {}
    
    def calculate_reward(self, vm):
        reward = 0
        # Add reward based on performance metrics
        if vm["cpu"]["cpu_usage"] < 50: reward += 1
        if vm["memory"]["memory_usage_percent"] < 70: reward += 1
        # Consider workflow-specific requirements
        if self.workflow_data["time_intensive"]: reward += (100 - float(vm["cpu"]["cpu_usage"]))
        done = True  # One task assignment per step
        return reward, done
    
    def reset(self):
        self.state = self.initialize_state()
        return self.state
    
    def initialize_state(self):
        state = []
        # Normalize and combine VM and workflow features
        for vm in self.vm_data:
            state.append(float(vm["cpu"]["cpu_usage"]) / 100)
            state.append(float(vm["memory"]["memory_usage_percent"]) / 100)
        state += [self.workflow_data["time_intensive"], self.workflow_data["resource_intensive"]]
        return np.array(state, dtype=np.float32)
