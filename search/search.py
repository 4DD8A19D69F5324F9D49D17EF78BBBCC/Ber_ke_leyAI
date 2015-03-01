# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  vis = {}
  pre = []
  def dfs(nowState):
      if problem.isGoalState(nowState):
          return pre[:]
      vis[nowState] = 1
      for nextState,action,cost in problem.getSuccessors(nowState):
          if nextState not in vis:
              pre.append(action)
              res = dfs(nextState)
              if res:
                  return res
              pre.pop()
      return []
  ans=dfs(problem.getStartState())
  return ans

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  "*** YOUR CODE HERE ***"
  from collections import deque
  pre = {problem.getStartState():None}
  q = deque([problem.getStartState()])
    
  actions_rev = []
  while q:
      nowState = q.popleft()
      if problem.isGoalState(nowState):          
          while pre[nowState]:
            preState,preAction = pre[nowState]
            nowState = preState
            actions_rev.append(preAction)
          return actions_rev[::-1]
      for nextState,action,cost in problem.getSuccessors(nowState):
          if nextState not in pre:
              pre[nextState]=(nowState,action)
              q.append(nextState)
              
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  return aStarSearch(problem)
    

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  import heapq
  pre = {problem.getStartState():None}
  total_cost = {problem.getStartState():0}
  q = []
  heapq.heappush(q, (0,0,problem.getStartState()))
  
  actions_rev = []
  while q:
      nowh,nowCost,nowState = heapq.heappop(q)
      nowCost = -nowCost
      if problem.isGoalState(nowState):          
          while pre[nowState]:
            preState,preAction = pre[nowState]
            nowState = preState
            actions_rev.append(preAction)
          return actions_rev[::-1]
      for nextState,action,cost in problem.getSuccessors(nowState):
          if nextState not in total_cost or nowCost+cost<total_cost[nextState]:
              pre[nextState]=(nowState,action)
              total_cost[nextState] = nowCost+cost
              heapq.heappush(q, (nowCost+cost+heuristic(nextState,problem=problem),-(nowCost+cost),nextState))
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
