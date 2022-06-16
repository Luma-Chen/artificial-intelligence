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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newFoodList = newFood.asList()
        ghostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minDistanceGhost = float("+inf")
        for ghostPos in ghostPositions:
            minDistanceGhost = min(minDistanceGhost, util.manhattanDistance(newPos, ghostPos))

        if minDistanceGhost == 0:
            return float("-inf")
        if successorGameState.isWin():
            return float("+inf")
        
        score = successorGameState.getScore()
        # incentiva ação que conduz o agente para mais longe do fantasma mais próximo
        score += 2 * minDistanceGhost

        minDistanceFood = float("+inf")
        for foodPos in newFoodList:
            minDistanceFood = min(minDistanceFood, util.manhattanDistance(foodPos, newPos))

        # incentiva acao que conduz o agente para mais perto da comida mais próxima
        score -= 2 * minDistanceFood

        # incentiva acao que leva a uma comida
        if(successorGameState.getNumFood() < currentGameState.getNumFood()):
            score += 5

        # penaliza as acoes de parada
        if action == Directions.STOP:
            score -= 10
        return score

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
        minimax = self.minimax(gameState, agentIndex=0, depth=self.depth)

        return minimax['action']

    def minimax(self, gameState, agentIndex=0, depth='2', action=Directions.STOP):
        agentIndex = agentIndex % gameState.getNumAgents()

        if agentIndex == 0: 
            depth = depth-1

        if gameState.isWin() or gameState.isLose() or depth == -1:
            return {'value':self.evaluationFunction(gameState), 'action':action}

        else:
            if agentIndex==0: 
                return self.maxValue(gameState,agentIndex,depth)
            else: 
                return self.minValue(gameState,agentIndex,depth)

    def maxValue(self, gameState, agentIndex, depth):
        value = {'value': float('-inf'), 'action': Directions.STOP}
        legalMoves = gameState.getLegalActions(agentIndex)        

        for action in legalMoves:

            if action == Directions.STOP: 
                continue

            successorGameState = gameState.generateSuccessor(agentIndex, action) 
            successorMinMax = self.minimax(successorGameState, agentIndex+1, depth, action)

            if value['value'] <= successorMinMax['value']:
                value['value'] = successorMinMax['value']
                value['action'] = action

        return value

    def minValue(self, gameState, agentIndex, depth):
        value = {'value': float('inf'), 'action': Directions.STOP}
        legalMoves = gameState.getLegalActions(agentIndex)

        for action in legalMoves:

            if action == Directions.STOP: 
                continue

            successorGameState = gameState.generateSuccessor(agentIndex, action)
            successorMinMax = self.minimax(successorGameState, agentIndex+1, depth, action)

            if value['value'] >= successorMinMax['value']:
                value['value'] = successorMinMax['value']
                value['action'] = action

        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float('-inf')
        beta = float('inf')
        minimax = self.minimax(gameState, agentIndex=0, depth=self.depth, alpha=alpha, beta=beta)
        
        return minimax['action']

    def minimax(self, gameState, agentIndex=0, depth='0', action=Directions.STOP, alpha=float('-inf'), beta=float('inf')):
        agentIndex = agentIndex % gameState.getNumAgents()

        if agentIndex == 0: 
            depth = depth-1

        if gameState.isWin() or gameState.isLose() or depth == -1:
            return {'value':self.evaluationFunction(gameState), 'action':action}
        
        if agentIndex==0: 
            return self.maxValue(gameState,agentIndex,depth, alpha, beta)
        else: 
            return self.minValue(gameState,agentIndex,depth, alpha, beta)    

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):

        value = {'value':float('-inf'), 'action':Directions.STOP}

        legalMoves = gameState.getLegalActions(agentIndex)

        for action in legalMoves:

            if action == Directions.STOP: continue

            successorGameState = gameState.generateSuccessor(agentIndex, action)
            successorMinMax = self.minimax(successorGameState, agentIndex+1, depth, action, alpha, beta)

            if value['value'] <= successorMinMax['value']:
                value['value'] = successorMinMax['value']
                value['action'] = action

            if value['value'] > beta: 
                return value
            alpha = max(alpha, value['value'])

        return value

    def minValue(self, gameState, agentIndex, depth, alpha, beta):

        value = {'value':float('inf'), 'action':Directions.STOP}
        legalMoves = gameState.getLegalActions(agentIndex)

        for action in legalMoves:

            if action == Directions.STOP: continue

            successorGameState = gameState.generateSuccessor(agentIndex, action)

            successorMinMax = self.minimax(successorGameState, agentIndex+1, depth, action, alpha, beta)

            if value['value'] >= successorMinMax['value']:
                value['value'] = successorMinMax['value']
                value['action'] = action

            if value['value'] < alpha: 
                return value
            beta = min(beta, value['value'])

        return value

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
        depth = self.depth
        minimax = self.expectimax(gameState, 0, depth, Directions.STOP)
        return minimax['action']

    def expectimax(self, gameState, agentIndex, depth, action):
        agentIndex = agentIndex % gameState.getNumAgents()

        if agentIndex == 0: 
            depth = depth-1

        if gameState.isWin() or gameState.isLose() or depth == -1:
            return {'value':self.evaluationFunction(gameState), 'action':action}
        
        if agentIndex==0: 
            return self.maxValue(gameState,agentIndex,depth)
        else: 
            return self.minValue(gameState,agentIndex,depth)  

    def maxValue(self, gameState, agentIndex, depth):

        value = {'value': float('-inf'), 'action': Directions.STOP}
        legalMoves = gameState.getLegalActions(agentIndex)        

        for action in legalMoves:
            if action == Directions.STOP: 
                continue

            successorGameState = gameState.generateSuccessor(agentIndex, action) 
            successorExpectiMax = self.expectimax(successorGameState, agentIndex+1, depth, action)

            if value['value'] <= successorExpectiMax['value']:
                value['value'] = successorExpectiMax['value']
                value['action'] = action

        return value

    def minValue(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        successorCosts = []

        for action in actions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)

            value = self.expectimax(successorGameState, agentIndex+1, depth, action)
            successorCosts.append(value['value'])

        return {'value': sum(successorCosts) / float(len(successorCosts)), 'action': Directions.STOP}

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    """
    if currentGameState.isWin():
        return float("+inf")

    if currentGameState.isLose():
        return float("-inf")

    score = scoreEvaluationFunction(currentGameState)
    newFoodList = currentGameState.getFood().asList()
    newPos = currentGameState.getPacmanPosition()
    minDistanceFood = float("+inf")

    for foodPos in newFoodList:
        minDistanceFood = min(minDistanceFood, util.manhattanDistance(foodPos, newPos))

    score -= 2 * minDistanceFood
    score -= 4 * len(newFoodList)
    capsulelocations = currentGameState.getCapsules()
    score -= 4 * len(capsulelocations)
    return score
    
# Abbreviation
better = betterEvaluationFunction