# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import sys

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        heuristic = list()
        foodList = newFood.asList()
        for food in foodList:
            heuristic.append(-1 * manhattanDistance(food, newPos))
        if action == Directions.STOP:
            return -sys.maxint
        for ghostState in newGhostStates:
            if ghostState.getPosition() == newPos:
                if ghostState.scaredTimer == 0:
                    return -sys.maxint
        return max(heuristic)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        depth = 0
        agentIndex = 0
        value = self.value(gameState, agentIndex, depth)
        return value[0]

    def value(self, gameState, agentIndex, depth): 
        numAgents = gameState.getNumAgents()
        if agentIndex >= numAgents:
            depth += 1
            agentIndex = 0
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex != 0:
            return self.minValue(gameState, depth, agentIndex)
        else:
            return self.maxValue(gameState, depth, agentIndex)
        
    def maxValue(self, gameState, depth, agentIndex):
        v = (None, -sys.maxint)
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)
            val = self.value(successor, agentIndex + 1, depth)
            if type(val) is tuple:
                val = val[1] 
            maximize = max(v[1], val)
            if maximize is not v[1]:
                v = (action, maximize) 
        return v

    def minValue(self, gameState, depth, agentIndex):
        v = (None, sys.maxint)
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)           
            val = self.value(successor, agentIndex + 1, depth)
            if type(val) is tuple:
                val = val[1]
            minimize = min(v[1], val)
            if minimize is not v[1]:
                v = (action, minimize) 
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        agentIndex = 0
        a = -sys.maxint
        b = sys.maxint
        val = self.value(gameState, agentIndex, depth, a, b)
        return val[0]

    def value(self, gameState, agentIndex, depth, a, b): 
        numAgents = gameState.getNumAgents()
        if agentIndex >= numAgents:
            depth += 1
            agentIndex = 0
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex != 0:
            return self.minValue(gameState, depth, agentIndex, a, b)
        else:
            return self.maxValue(gameState, depth, agentIndex, a, b)
        
    def maxValue(self, gameState, depth, agentIndex, a, b):
        v = (None, -sys.maxint)
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)
            val = self.value(successor, agentIndex + 1, depth, a, b)
            if type(val) is tuple:
                val = val[1] 
            maximize = max(v[1], val)
            if maximize is not v[1]:
                v = (action, maximize)
            if v[1] > b:
                return v
            a = max(a, v[1]) 
        return v

    def minValue(self, gameState, depth, agentIndex, a, b):
        v = (None, sys.maxint)
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)           
            val = self.value(successor, agentIndex + 1, depth, a, b)
            if type(val) is tuple:
                val = val[1]
            minimize = min(v[1], val)
            if minimize is not v[1]:
                v = (action, minimize)
            if v[1] < a:
                return v
            b = min(b, v[1]) 
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        agentIndex = 0
        value = self.value(gameState, agentIndex, depth)
        return value[0]

    def value(self, gameState, agentIndex, depth): 
        numAgents = gameState.getNumAgents()
        if agentIndex >= numAgents:
            depth += 1
            agentIndex = 0
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex != 0:
            return self.expected(gameState, depth, agentIndex)
        else:
            return self.maxValue(gameState, depth, agentIndex)
        
    def maxValue(self, gameState, depth, agentIndex):
        v = (None, -sys.maxint)
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)
            val = self.value(successor, agentIndex + 1, depth)
            if type(val) is tuple:
                val = val[1] 
            maximize = max(v[1], val)
            if maximize is not v[1]:
                v = (action, maximize) 
        return v

    def expected(self, gameState, depth, agentIndex):
        v = [None, 0]
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        for action in legalActions:
            if action == Directions.STOP:
                continue
            successor = gameState.generateSuccessor(agentIndex, action)
            val = self.value(successor, agentIndex + 1, depth)
            if type(val) is tuple:
                val = val[1] 
            v[1] += val/len(legalActions)
            v[0] = action
        return tuple(v)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Copied most of the code from the reflex agent, using the manhattanDistance
    to determine heuristics for food and ghosts. Added capsules to account for score loss
    due to timesteps.
    """
    "*** YOUR CODE HERE ***"
    #functions I need
    thisPos = currentGameState.getPacmanPosition()
    thisFood = currentGameState.getFood()
    thisGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    foodHeuristic = list()
    ghostHeuristic = list()
    
    foodList = thisFood.asList()
    scaredGhosts = 0
    for food in foodList:
        foodHeuristic.append(-1 * manhattanDistance(food, thisPos))    
    if not foodHeuristic:
        foodHeuristic.append(0)
    for ghostState in thisGhostStates:
        if ghostState.scaredTimer == 0:
            scaredGhosts += 1
            ghostHeuristic.append(0)
            continue
        ghostPos = ghostState.getPosition()
        ghostHeuristic.append(-1 * manhattanDistance(ghostPos, thisPos))
    return max(foodHeuristic) + min(ghostHeuristic) + score - 100*len(capsules) - 20*(len(thisGhostStates) - scaredGhosts)
 
    
# Abbreviation
better = betterEvaluationFunction

