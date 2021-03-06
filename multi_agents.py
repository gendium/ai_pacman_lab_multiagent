"""
Author: Sean Egger, Alec Rulev
Class: CSI-480-01
Assignment: Multi Agent Pacman Programming Assignment
Date Assigned: Tuesday
Due Date: Monday 11:59
 
Description:
A pacman ai program
 
Certification of Authenticity: 
I certify that this is entirely my own work, except where I have given 
fully-documented references to the work of others. I understand the definition 
and consequences of plagiarism and acknowledge that the assessor of this 
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
multi_agents.py

Champlain College CSI-480, Fall 2017
The following code was adapted by Joshua Auerbach (jauerbach@champlain.edu)
from the UC Berkeley Pacman Projects (see license and attribution below).

----------------------
Licensing Information:  You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""


from util import manhattan_distance
from game import Directions
import random, util, sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_ghost_states = successor_game_state.get_ghost_states()

        "*** YOUR CODE HERE ***"
        distance = []
        food_list = current_game_state.get_food().as_list()
        pacman_position = list(successor_game_state.get_pacman_position())

        if action == 'Stop':
        	return -float("inf")

        for ghost_state in new_ghost_states:
           	if ghost_state.get_position() == tuple(pacman_position) and ghost_state.scared_timer is 0:
           		return -float("inf")

        for food in food_list:
	        x = -1*abs(food[0] - pacman_position[0])
	        y = -1*abs(food[1] - pacman_position[1])
	        distance.append(x+y) 
        return max(distance)

def score_evaluation_function(current_game_state):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return current_game_state.get_score()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, eval_fn = 'score_evaluation_function', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth)

    def is_terminal_state(self, state, depth, agent):
    	return depth == self.depth or state.is_win() or state.is_lose() or state.get_legal_actions(agent) == 0
    def is_pacman(self, state, agent):
    	return agent % state.get_num_agents() == 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def get_action(self, game_state):
        """
          Returns the minimax action from the current game_state using self.depth
          and self.evaluation_function.

          Here are some method calls that might be useful when implementing minimax.

          game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means Pacman, ghosts are >= 1

          game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action

          game_state.get_num_agents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
       
        return max(game_state.get_legal_actions(0), key = lambda x: self.mini_max(game_state.generate_successor(0,x),0,1))


    def mini_max(self,state,depth, agent):
    	if agent == state.get_num_agents():
    		return self.mini_max(state, depth + 1, 0)
    	if self.is_terminal_state(state, depth, agent):
    		return self.evaluation_function(state)
    	successors = (
    		self.mini_max(state.generate_successor(agent, action), depth, agent + 1)
    		for action in state.get_legal_actions(agent)
    		)
    	return (max if self.is_pacman(state, agent)else min)(successors)
    	



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
          Returns the minimax action using self.depth and self.evaluation_function
        """
        alpha = float('-inf')
        beta = float('inf')
        current_depth = 0
        current_agent = 0
        value = self.valuation(game_state, current_agent, current_depth, alpha, beta)
        return value[0]
    def valuation(self, game_state, current_agent, current_depth, alpha, beta):
        if current_agent >= game_state.get_num_agents():
            current_agent = 0
            current_depth = current_depth + 1
        if self.is_terminal_state(game_state, current_depth, current_agent):
            return self.evaluation_function(game_state)
        if self.is_pacman(game_state, current_agent):
            return self.get_max_or_min_value(game_state, current_agent, current_depth, alpha, beta, True)
        else:
            return self.get_max_or_min_value(game_state, current_agent, current_depth, alpha, beta, False)

    def get_max_or_min_value(self, game_state, current_agent, current_depth, alpha, beta, is_max):
        if is_max:
            this_value = ("unknown", float("-inf"))
        else:
            this_value = ("unknown", float("inf"))

        if not game_state.get_legal_actions(current_agent):
            return self.evaluation_function(game_state)
        for action in game_state.get_legal_actions(current_agent):
            if action == "Stop":
                continue
            return_value = self.valuation(game_state.generate_successor(current_agent, action), current_agent + 1, current_depth, alpha, beta )
            if type(return_value) is tuple:
                return_value = return_value[1]
            value_new = None
            if is_max:
                value_new = max(this_value[1], return_value)
            else:
                value_new = min(this_value[1], return_value)

            if value_new is not this_value[1]:
                this_value = (action, value_new)

            if is_max:
                if this_value[1] > beta:
                   return this_value
                alpha = max(alpha, this_value[1])
            else:
                if this_value[1] < alpha:
                    return this_value
                beta = min(beta, this_value[1])
        return this_value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
          Returns the expectimax action using self.depth and self.evaluation_function

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return max(game_state.get_legal_actions(0), 
          key = lambda x: self.expectimax(game_state.generate_successor(0, x), 0, 1) )

    def expectimax(self, state, depth, agent):
      if agent == state.get_num_agents(): # if agent is pacman
        return self.expectimax(state, depth + 1, 0) #increase depth
      
      if depth == self.depth or state.is_win() or state.is_lose() or state.get_legal_actions(agent) == 0: # if leaf node
        return self.evaluation_function(state) #evaluate

      successors = [
        self.expectimax(state.generate_successor(agent, action), depth, agent + 1)
        for action in state.get_legal_actions(agent)
        ]
      # find the best move for pacman
      if agent % state.get_num_agents() == 0:
        return max(successors)
      # average ghost moves
      else:
        return sum(successors)/len(successors)


def better_evaluation_function(current_game_state):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The evaluation function considers the current score of a state
        and factors in the distance to a ghost, an edible ghost, and the closest food
        dot. If and edible ghost is nearby and is scared for long enough to get to, then
        going for that ghost is greatly incentivized as it adds alot of points.  If 
        there is any ghost nearby it deincentivizes that state, tempered by the distance
        of the ghost. The function also checks the closest food pellet. The closer the 
        closest food pellet the more incentivization. These incentivizers of ghosts,
        edible ghosts and closest food dot are all summed with the score. That value
        is then returned. 
    """
    "*** YOUR CODE HERE ***"
    pos = current_game_state.get_pacman_position()
    food = current_game_state.get_food()
    ghost_states = current_game_state.get_ghost_states()

    food_weight = 1.0
    ghost_weight = 1.0
    edible_ghost_weight = 7.0

    # because the score at each state matters
    value = current_game_state.get_score()

    # distance to ghosts
    ghost_value = 0
    for ghost in ghost_states:
      distance_to_ghost = manhattan_distance(pos, ghost.get_position())
      if distance_to_ghost > 0:
        if ghost.scared_timer > distance_to_ghost: # if ghost scared and close enough to get
          ghost_value += edible_ghost_weight / distance_to_ghost # eat it
        else: # else avoid ghost
          ghost_value -= ghost_weight / distance_to_ghost
    value += ghost_value

    # distance to closest food
    distances_to_food = [manhattan_distance(pos, x) for x in food.as_list()]
    if len(distances_to_food): #if food is found
      value += food_weight / min(distances_to_food)

    return value


# Abbreviation
better = better_evaluation_function

