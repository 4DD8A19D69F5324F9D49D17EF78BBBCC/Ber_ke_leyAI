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
import operator

from game import Agent

import math




def evalState(successorGameState):
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    

    walls = successorGameState.getWalls().data
    def getdistFrom(pt):
    	dis = [[10000]*len(walls[0]) for i in range(len(walls))]
    	x,y=pt
    	dis[x][y]=0
    	dxs = [1,-1,0,0]
    	dys = [0,0,1,-1]
    	from collections import deque

    	q = deque()

    	q.append((x,y))

    	while q:
    		x,y = q.popleft()
    		for dx,dy in zip(dxs,dys):
    			nx = x+dx
    			ny = y+dy
    			if not walls[nx][ny] and dis[nx][ny]==10000:
    				dis[nx][ny]=dis[x][y]+1
    				q.append((nx,ny))
    	return dis


    d = getdistFrom(newPos)


    def dist(p2):
        x2,y2 = p2
        x2 = int(x2)
        y2 = int(y2)
        return d[x2][y2]
    
    all_dis = [dist(pFood) for pFood in newFood.asList()]
    all_dis_g = [dist(ghost.getPosition()) for ghost in newGhostStates]
    
    all_dis.sort()
    def myexp(x,d):
        if x>0:
            return x**d
        else:
            return -((-x)**d)
    K = 3
    dis_weight = [0.9**i for i in range(K)]
    
    for i,scaredTime in enumerate(newScaredTimes):
        if scaredTime>all_dis_g[i]+5:
            all_dis_g[i]*=-0.01
    
    dis_score = sum(x*w for x,w in zip(all_dis,dis_weight))
    ghost_penalty = max(1.0/(myexp(x,1)+0.001) for x in all_dis_g)
    
    food_remain = len(newFood.asList())
    return successorGameState.getScore() - 2*dis_score - 50*ghost_penalty - 40 * food_remain


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
        return evalState(successorGameState)
    
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
        n = gameState.getNumAgents()
        
        
        def nextPlayer(agentIndex):
            return (agentIndex + 1) % n
        
        def depthInc(agentIndex):
            if agentIndex == n-1:
                return 1
            else:
                return 0
        
        def dfs(agentIndex,nowState,nowDepth):
            decision_function = max if agentIndex == 0 else min
            judge_function = nowState.isWin if agentIndex == 0 else nowState.isLose
            
            if nowDepth>=self.depth or judge_function():
                return None,self.evaluationFunction(nowState)
            
            vals = []
            for action in nowState.getLegalActions(agentIndex):
                newState = nowState.generateSuccessor(agentIndex,action)
                enemy_action,value = dfs(nextPlayer(agentIndex),newState,nowDepth+depthInc(agentIndex))
                vals.append((action,value))
                
            if vals:
                ret = decision_function(vals,key = lambda x:x[1])
            else:
                ret = (None,self.evaluationFunction(nowState))
            return ret

        action,value = dfs(0,gameState,0)
        return action
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """             
        n = gameState.getNumAgents()
        def nextPlayer(agentIndex):
            return (agentIndex + 1) % n
        
        def depthInc(agentIndex):
            if agentIndex == n-1:
                return 1
            else:
                return 0
        
        def getInf(agentIndex):
            return -10**5 if agentIndex == 0 else 10**5 
        
        def dfs(alpha,beta,agentIndex,nowState,nowDepth):
            judge_function = nowState.isWin if agentIndex == 0 else nowState.isLose
            if nowDepth>=self.depth or judge_function():
                return None,self.evaluationFunction(nowState)
            
            def max_node(nowState,alpha=-10**9,beta=10**9):
                ret = None,-10**9
                for action in nowState.getLegalActions(agentIndex):
                    newState = nowState.generateSuccessor(agentIndex,action)
                    enemy_action,value = dfs(alpha,beta,nextPlayer(agentIndex),newState,nowDepth+depthInc(agentIndex))
                    ret = max(ret,(action,value),key= lambda x:x[1])
                    if ret[1]>beta:
                        return action,ret[1]
                    alpha = max(alpha,value)
                
                if ret[1]==-10**9:
                    ret = None,self.evaluationFunction(nowState)
                return ret
                
            def min_node(nowState,alpha=-10**9,beta=10**9):
                ret = None,10**9
                for action in nowState.getLegalActions(agentIndex):
                    newState = nowState.generateSuccessor(agentIndex,action)
                    enemy_action,value = dfs(alpha,beta,nextPlayer(agentIndex),newState,nowDepth+depthInc(agentIndex))
                    ret = min(ret,(action,value),key= lambda x:x[1])
                    if ret[1]<alpha:
                        return action,ret[1]
                    beta = min(beta,value)
                if ret[1]==10**9:
                    ret = None,self.evaluationFunction(nowState)         
                return ret
            
            if agentIndex==0:
                return max_node(nowState,alpha,beta)
            else:
                return min_node(nowState,alpha,beta)
                
            
        
        action,value = dfs(-10**9,10**9,0,gameState,0)
        return action

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
        n = gameState.getNumAgents()
        
        
        def nextPlayer(agentIndex):
            return (agentIndex + 1) % n
        
        def depthInc(agentIndex):
            if agentIndex == n-1:
                return 1
            else:
                return 0
        
        def avg(Iterable,key = lambda x:x):
            
            ks = [key(x) for x in Iterable]
            return None,1.0*sum(ks)/ len(ks)
        
        def dfs(agentIndex,nowState,nowDepth):
            decision_function = max if agentIndex == 0 else avg
            judge_function = nowState.isWin if agentIndex == 0 else nowState.isLose
            
            if nowDepth>=self.depth or judge_function():
                return None,self.evaluationFunction(nowState)
            
            vals = []
            for action in nowState.getLegalActions(agentIndex):
                newState = nowState.generateSuccessor(agentIndex,action)
                enemy_action,value = dfs(nextPlayer(agentIndex),newState,nowDepth+depthInc(agentIndex))
                vals.append((action,value))
                
            if vals:
                ret = decision_function(vals,key = lambda x:x[1])
            else:
                ret = (None,self.evaluationFunction(nowState))
            return ret

        action,value = dfs(0,gameState,0)
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


    return evalState(currentGameState)

# Abbreviation
better = betterEvaluationFunction

