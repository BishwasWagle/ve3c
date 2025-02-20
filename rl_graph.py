import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Define RL Mathematical Function
def rl_decision_function(state, action, reward, gamma=0.99):
    """
    RL Mathematical Function:
    Q(s, a) = reward + gamma * max(Q(s', a'))

    :param state: Current state of the environment
    :param action: Action taken
    :param reward: Reward received after action
    :param gamma: Discount factor for future rewards
    :return: Updated Q-value
    """
    # For simplicity, let's assume a mock Q-value update
    next_state = state + action  # Example transition function
    future_rewards = np.max(next_state)  # Example max future reward
    updated_q_value = reward + gamma * future_rewards
    return updated_q_value

# RL Block Diagram Visualization
def plot_rl_environment():
    """
    Visualize the block diagram of RL environments for Performance and Security Models.
    """
    # Create directed graphs for both environments
    G = nx.DiGraph()

    # Common nodes
    G.add_node("Workflow Submission")
    G.add_node("Decision (Cluster)")
    G.add_node("Feedback")

    # Performance environment
    G.add_edge("Workflow Submission", "Performance RL Model")
    G.add_edge("Performance RL Model", "Decision (Cluster)")

    # Security environment
    G.add_edge("Workflow Submission", "Security RL Model")
    G.add_edge("Security RL Model", "Decision (Cluster)")

    # Feedback loops
    G.add_edge("Decision (Cluster)", "Feedback")
    G.add_edge("Feedback", "Performance RL Model")
    G.add_edge("Feedback", "Security RL Model")

    # Visualization
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    plt.title("Reinforcement Learning Environment Block Diagram", fontsize=14)
    plt.show()

# Example usage
if __name__ == "__main__":
    # Test RL Decision Function
    current_state = np.array([1, 0, 0])  # Example state
    action = np.array([0, 1, 0])  # Example action
    reward = 5  # Example reward

    updated_q = rl_decision_function(current_state, action, reward)
    print(f"Updated Q-value: {updated_q}")

    # Visualize RL Block Diagram
    plot_rl_environment()
