from game import *
"""_summary_
TD Learning - afterstate solution

Completes TD learning on afterstates - the state after player makes a move, before a new tile
is generated

Uses row -tuples to reduce the state space from 16^ 12 to 4* 4^12
    Returns:
        _type_: _description_
    """


moves = [0, 1, 2, 3]


def arr_to_tuple(arr):
    '''
    Convert array to tuple
    '''
    return tuple(e for e in arr)



class score_tracker:
    '''
    Class for hadnling weight tracking by row instead of 2d array
    each row is handled as a seperate state space.
    
    Get score function results in the score for each row added together
    
    Set score function results in the score being divided by 4 and setting 
    divided score to each row state
    
    To do: research better get and set functions
    '''
    def __init__(self, **args):
        self.row1 = {}
        self.row2 = {}
        self.row3 = {}
        self.row4 = {}
        
        self.rows = [self.row1, self.row2, self.row3, self.row4]
        
    def get_score(self, board):
        b_row1 = board[0]
        b_row2 = board[1]
        b_row3 = board[2]
        b_row4 = board[3]
        
        score_row1 = self.safe_get(b_row1, self.row1)
        score_row2 = self.safe_get(b_row2, self.row2)
        score_row3 = self.safe_get(b_row3, self.row3)
        score_row4 = self.safe_get(b_row4, self.row4)
        
        return score_row1 + score_row2 + score_row3 + score_row4
        
        
        
    def safe_get(self, arr, dict):
        s = arr_to_tuple(arr)
        if s in dict:
            return dict[s]
        return 0.0
    
    
    
    def safe_set(self, arr, score, dict):
        s = arr_to_tuple(arr)
        dict[s] = score
    
    
    
    def set_score(self,  afterstate, alpha, reward_next, afterstate_next,score):
        b_rows = [afterstate[0], afterstate[1], afterstate[2], afterstate[3]]
        
        score_b_rows = [self.safe_get(b_rows[0], self.row1), self.safe_get(b_rows[1], self.row2),
                        self.safe_get(b_rows[2], self.row3), self.safe_get(b_rows[3], self.row4)]
        
        as_rows = [ afterstate_next[0],  afterstate_next[1],  afterstate_next[2],  afterstate_next[3]]
        
       
        '''
        how do we split up scores? rn it is score/4
        update to V function for each row
        '''
        #score = self.scoreDictionary.get_score(afterstate) + self.alpha* (reward_next + self.scoreDictionary.get_score(afterstate_next)- self.scoreDictionary.get_score(afterstate))
        
        
        for i in range(4):
           # score = score_b_rows[i] + alpha*(reward_next + self.safe_get(as_rows[i], self.rows[i]) - score_b_rows[i] )
            self.safe_set(b_rows[i], score/4, self.rows[i])
      
      
      
      
class TDAfterStateLearningAgent:
    """
     TD after state agent
     
     score tracker is initiated as well as learning rate (alpha)
     
     get_move_from_score takes a board and returns the best productive
     move. If there are no productive moves then None is returned
    """
    def __init__(self, **args):
        self.scoreDictionary = score_tracker()
        self.alpha = 0.1
        
    
    def get_move_from_score(self, board):
        """
        Runs eval function on each action for a given state and returns
        the action with the max score
        """
        bestAction = None
        score = -float('inf')
        for move in moves:
            new_board = perform_move(board, move)[0]
            if np.array_equal(board, new_board):  # don't consider a move that does nothing
                continue
            new_score = self.evaluate(board, move)
            if new_score > score:
                bestAction = move
                score = new_score
            if new_score == score:
                choice = random.choice([move, bestAction]) 
                bestAction = choice
        
        return bestAction
    
        
    def evaluate(self,board,action):
        '''
        V is lookup table
        s',r = Compute afterstate(s,a)
        return r + V(s')
        '''
        afterstate, reward_next = perform_move(board, action)
       
        return self.scoreDictionary.get_score(afterstate) +reward_next
    
    '''def safe_get(self, board):
        s = arr_to_tuple(board)
        if s in self.scoreDictionary:
            return self.scoreDictionary[s]
        return 0.0
        '''
         
    
    def update(self, startState, reward, afterstate, nextState):
         '''
         learning function - get current state weight and update it with the 
         experienced reward
         
         
         nextaction = evaluate for each action (nextstate, possibleaction)
         afterstatenext, rewardnext = compute_afterstate(nextstate, actionnext)
         V(afterstate) = V(sfterstate)+ alpha(rewardnext + V(afterstatenext)- V(afterstate))'''
         nextaction = self.get_move_from_score(nextState)
         afterstate_next = nextState
         reward_next = 0
         if nextaction != None:
            
            afterstate_next, reward_next = perform_move(nextState, nextaction)
         #asState = arr_to_tuple(afterstate)
        #self, score, afterstate, alpha, reward_next, afterstate_next):
         score = self.scoreDictionary.get_score(afterstate) + self.alpha* (reward_next + self.scoreDictionary.get_score(afterstate_next)- self.scoreDictionary.get_score(afterstate))
         self.scoreDictionary.set_score(afterstate, self.alpha, reward_next, afterstate_next, score)
    


def play_game(iterations, learning_enabled, agent):
    '''
    score = 0
    s = initialize game state
    while not in terminal state (s)
        bestAction = argmax(actions)-Evaluate(s,a')
        r,s',s'' = make_move(s,bestAction)
        if learning enabled
            learn eval(s,bestAction, s',s''
        score += r
    return score
    '''
    scores = np.zeros(iterations)
    for i in range(iterations):
        board = new_game(4)
        board = add_two(board)
        board = add_two(board)
        lost = False
        #print(board)
        #print()
        while not lost:
          
                
            bestAction = agent.get_move_from_score(board)
            # r = new_score, s' = board = afterstate
            afterboard, new_score = perform_move(board, bestAction)
            scores[i] += new_score
            #s'' = board = nextstate
            nextboard = add_two(afterboard)
           
            if learning_enabled:
                agent.update(board, new_score, afterboard, nextboard)
            #print(np.array(board))
            #print()
            board = nextboard
            #print(np.array(board))
            if game_state(board) == 'lose':
                    #print(np.array(board))
                #print()
                print(f"Game {i} score: {scores[i]}")
                #print()
                
                print(np.array(board))
                lost = True
                continue
            
    print(f'Average score: {scores.mean()}')
    
def main():
    agent  = TDAfterStateLearningAgent() 
    learning_games = 1000
    play_game(learning_games, True, agent)
    print()
    print()
    real_games = 30
    play_game(real_games, False, agent)
   


if __name__ == "__main__":
    main()
