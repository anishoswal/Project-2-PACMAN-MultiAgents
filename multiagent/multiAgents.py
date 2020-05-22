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
import math

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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFood = newFood.asList()
        nearestF = 999999999

        #calculate the distance to the nearest food position
        for f in newFood:
            dist = manhattanDistance(newPos,f)
            nearestF = min(nearestF, dist)

        #Find the position of the ghost
        ghostPositions = successorGameState.getGhostPositions()
        for g in ghostPositions:
            dist = manhattanDistance(newPos, g)
            if (dist < 2): #if the ghost is too close then abort
                return -nearestF
        return (successorGameState.getScore()*nearestF + math.exp(1))/nearestF #else update the evaluation function

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
        """
        "*** YOUR CODE HERE ***"
        #initialization
        return self.maximum(gameState, 0, 0)[0]
        util.raiseNotDefined()


    def minimaxAgent(self, gameState, aIndex, d):
        won = gameState.isWin() #check if the game is won
        lost = gameState.isLose() #check if the game is lost
        noAgents = self.depth*gameState.getNumAgents()
        if d is noAgents or won or lost:
            return self.evaluationFunction(gameState) #if the game is won or lost call the evaluation function

        #for odd depth iterations minimize else maximize
        var = self.minimum(gameState, aIndex, d)[1] if aIndex != 0 else self.maximum(gameState, aIndex, d)[1]
        return var

    def maximum(self, gameState, aIndex, d):
        legalActions = gameState.getLegalActions(aIndex)
        bestChoice = ("max", -999999999)
        d = d + 1
        #finds the best max reward choice among the given choices to choose from
        for act in legalActions:
            successor = gameState.generateSuccessor(aIndex, act)
            noAgents = d%gameState.getNumAgents()
            minimax = self.minimaxAgent(successor, noAgents, d) #calculates the best move
            successorMove = (act, minimax)
            key = lambda x: x[1]
            bestChoice = max(bestChoice, successorMove, key=key) #compares the new founded move to the older best
        return bestChoice

    def minimum(self, gameState, aIndex, d):
        legalActions = gameState.getLegalActions(aIndex)
        bestChoice = ("min", 999999999)
        d = d+1
        # finds the best min reward choice among the given choices to choose from (opponents turn)
        for act in legalActions:
            successor = gameState.generateSuccessor(aIndex, act)
            noAgents = d%gameState.getNumAgents()
            minimax = self.minimaxAgent(successor, noAgents, d) #calculates the best move
            successorMove = (act, minimax)
            key = lambda x: x[1]
            bestChoice = min(bestChoice, successorMove, key=key) #compares the new founded move to the older best
        return bestChoice

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #initialization
        num = 999999999
        max = self.maximum(gameState,0,0,-num,num)[0]
        return max
        util.raiseNotDefined()

    def abPruning(self, gameState, aIndex, d, a, b):
        won = gameState.isWin()
        lost = gameState.isLose()
        noAgents = self.depth*gameState.getNumAgents()
        if d is noAgents or won or lost:
            return self.evaluationFunction(gameState) #if the game is won or lost call the evaluation function

        # for odd depth iterations minimize else maximize
        var = self.minimum(gameState, aIndex, d, a, b)[1] if aIndex != 0 else self.maximum(gameState, aIndex, d, a, b)[1]
        return var

    def maximum(self, gameState, aIndex, d, a, b):
        legalActions = gameState.getLegalActions(aIndex)
        bestChoice = ("max", -999999999)
        d=d+1
        for act in legalActions:
            successor = gameState.generateSuccessor(aIndex, act)
            noAgents = d%gameState.getNumAgents()
            ab = self.abPruning(successor, noAgents, d, a, b) #calculates the best move
            successorMove = (act, ab)
            key = lambda x: x[1]
            bestChoice = max(bestChoice, successorMove, key=key) #compares the new founded move to the older best
            if bestChoice[1] > b: #pruning with respect to the beta value
                return bestChoice
            else:
                a = max(a, bestChoice[1])
        return bestChoice

    def minimum(self, gameState, aIndex, d, a, b):
        legalActions = gameState.getLegalActions(aIndex)
        bestChoice = ("min", 999999999)
        d = d + 1
        for act in legalActions:
            successor = gameState.generateSuccessor(aIndex, act)
            noAgents = d%gameState.getNumAgents()
            ab = self.abPruning(successor, noAgents, d, a, b) #calculates the best move
            successorMove = (act, ab)
            key = lambda x: x[1]
            bestChoice = min(bestChoice, successorMove, key=key) #compares the new founded move to the older best
            if bestChoice[1] < a: #pruning with respect to the alpha value
                return bestChoice
            else:
                b = min(b, bestChoice[1])
        return bestChoice

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
        d = self.depth* gameState.getNumAgents()
        expecti = self.expectimaxAlgo(gameState,"expect", d, 0)[0]
        return expecti
        util.raiseNotDefined()

    def expectimaxAlgo(self, gameState, act, d, aIndex):
        won = gameState.isWin()
        lost = gameState.isLose()
        if d is 0 or lost or won:
            return act, self.evaluationFunction(gameState) #if the game is won or lost call the evaluation function

        # for odd depth iterations minimize else maximize
        var = self.maximum(gameState, act, d, aIndex) if aIndex == 0 else self.expected(gameState, act, d, aIndex)
        return var

    def maximum(self, gameState, act, d, aIndex):
        legalActions = gameState.getLegalActions(aIndex)
        bestChoice = ("max", -999999999)
        for a in legalActions:
            newAgent = (aIndex+1)%gameState.getNumAgents()
            ndepth = self.depth*gameState.getNumAgents()
            successor = a if d==ndepth else act
            s = gameState.generateSuccessor(aIndex, a)
            successorVal = self.expectimaxAlgo(s,successor, d-1, newAgent) #calculates the best move
            k = lambda x: x[1]
            bestChoice = max(bestChoice, successorVal, key=k) #compares the new founded move to the older best
        return bestChoice

    def expected(self, gameState, act, d, aIndex):
        legalActions = gameState.getLegalActions(aIndex)
        avg = 0
        p = 1.0/len(legalActions) #probability calc
        for a in legalActions:
            newAgent = (aIndex+1)%gameState.getNumAgents()
            s = gameState.generateSuccessor(aIndex, a) #generate a new successor
            bestChoice = self.expectimaxAlgo(s, act, d-1, newAgent) #finds the best move
            avg += bestChoice[1]*p #calculates average
        return act, avg

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    nextPosition = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    newFood = 999999999
    for i in food:
        newFood = min(newFood, manhattanDistance(nextPosition, i)) #find the closest food positon

    ghostPosition = 0 #initialize the ghost position
    ghostRoute = currentGameState.getGhostPositions()
    for i in ghostRoute:
        ghostPosition = manhattanDistance(nextPosition, i) #update ghost position
        if (ghostPosition < 2): #if the ghost is too close abort
            return -999999999
    addFactors = 0
    won = currentGameState.isWin()
    lost = currentGameState.isLose()
    if won:
        addFactors += 10000 #add bias
    elif lost:
        addFactors -= 10000 #subtract bias
    #updated evaluation function taking receprocals of the values at hand like the food position, ghost position and the capsules remaining in game along with the bias
    return 20000 / (currentGameState.getNumFood() + math.exp(1)) + ghostPosition + 200 / (newFood + math.exp(1)) + 2000 / (len(currentGameState.getCapsules()) + math.exp(1)) + addFactors
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

