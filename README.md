
# Tic Tac Toe Game With AI

This is a simple Tic Tac Tor game played on a 3*3 board, The game is implemented using a Board class that represents the game board and state of the game. The class has a 9x1 numpy array representing the game board, which is initially set to all zeros. It also has lists to store the positions marked by player 1 (X) and player 2 (O) on the game board and a list of valid moves that can be made on the game board.
You can try this game by clicking this link http://pongsiri.pythonanywhere.com/

![image](https://user-images.githubusercontent.com/116048487/211845195-09437e8a-095f-44fc-b48a-f7ff8ccd8e90.png)




# The AI
In addition, this program contains two types of AI opponents made by two different algorithms, 1st using an objective function called the V function 2nd using the minimax algorithm.


## 1st AgentMaxV:

AgentMaxV using an objective function it chooses the action that gives the highest score from the function called the V function
The formula to calculate V functions is 
### V(b) = X(b) - O(b) + 1 
- X(b) is the summation of X symbols in the board that hasn't any O symbol in each line
- O(b) is the summation of the O symbols in the board that hasn't any X symbol in each line  
This method was adapted from Parinya Sanguansat. Artificial Intelligence with Machine Learning
![image](https://user-images.githubusercontent.com/116048487/211844743-5c742290-9e69-4818-9689-980b749ea93f.png)
![image](https://user-images.githubusercontent.com/116048487/211844770-9902cb99-ca0c-401f-b3ac-d63233c86dc1.png)



## 2nd AgentMinimax
AgentMinimax using the Minimax algorithm which is a Backtracking Algorithm that is used in decision-making to find the optimal move for a player in a two-player game.
It works by using a recursive function called minimax to explore all the possible moves and game states in the game tree,
starting from the root node (which represents the current state of the game)
and going all the way down to the leaf nodes (which represent the final stages of the game) to consider the scores of all possible moves at each step.
![null (13)](https://user-images.githubusercontent.com/116048487/211844283-c6e19488-3da8-4ae4-b9e7-a63c88269b31.png)
![Uploading image.png…]()





## How to Run

The program requires Python, NumPy, and flask to be installed on your computer
(Python 3.6+) 

```bash
  pip install python
  pip install numpy
  pip install flask
```

( This program can run both web and console )

## The Result of Testing the Efficacy of AI.
I have tested AI by letting it play against random and another AI, In addition, I've recorded hash from the final state for further study and development, You can access these by opening the folder named testing.
![1 Random(X) vs AgentmaxV(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843657-23cc52ef-b40c-4287-bf7c-b5d986df8538.png)
![2 AgentmaxV(X) vs Random(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843707-0829c0db-a41a-46f6-a645-182afb4be3ad.png)
![3 Random(X) vs AgentMinimax(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843735-22fd4f3a-28d6-4a66-8117-f200850b2caf.png)
![4 AgentMinimax(X) vs Random(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843754-9da52c62-a895-4fa7-b8ec-0660e7447f03.png)
![5 AgentmaxV(X) vs AgentMinimax(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843772-fdbd518e-14f9-417d-a868-c7f99d9e1ba1.png)
![6 AgentMinimax(X) vs AgentmaxV(O) (1,000 times)](https://user-images.githubusercontent.com/116048487/211843791-27ebfc54-9a4b-469b-bd4b-c88466e81d9f.png)

