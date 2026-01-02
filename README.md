# Binary String Game with AI Opponents

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A competitive two-player game implementing advanced game theory algorithms (Minimax and Alpha-Beta pruning) with comprehensive performance analysis and GUI interface.

## Project Overview

This project implements a strategic binary string manipulation game where players compete by selecting adjacent bit pairs to transform the string and accumulate points. The AI opponent uses adversarial search algorithms with custom heuristic evaluation functions to make optimal moves.

**Team 14** - Riga Technical University  
**Course**: Fundamentals of Artificial Intelligence  
**Academic Year**: 2024/2025  
**Instructor**: Alla Anohina-Naumeca

**Repository**: [github.com/Borinskii/Practical_Assignment_Team14](https://github.com/Borinskii/Practical_Assignment_Team14)

## Game Rules

Players take turns selecting adjacent binary pairs according to these transformation rules:

| Input Pair | Output | Effect |
|------------|--------|--------|
| `00` | `1` | Current player +1 point |
| `01` | `0` | Opponent +1 point |
| `10` | `1` | Opponent -1 point |
| `11` | `0` | Current player +1 point |

- **Starting Configuration**: Random binary string (length 15-25)
- **Win Condition**: Highest score when string reduces to single bit
- **Tie Condition**: Equal scores at game end

## Key Features

### AI Implementation
- **Minimax Algorithm**: Full game tree exploration with depth-limited search
- **Alpha-Beta Pruning**: Optimized search with branch cutoffs (up to 91% reduction in node exploration)
- **Custom Heuristic Function**: Evaluates board positions using score differential, positional value of remaining pairs, and look-ahead strategic assessment

### Performance Results

Based on 20 experimental runs with rigorous methodology:

| Algorithm | Win Rate | Avg Nodes Visited | Avg Time/Move | Best Use Case |
|-----------|----------|-------------------|---------------|---------------|
| **Minimax** | 90% | 48,272 - 750,776 | 0.026s - 0.222s | Educational, shorter strings |
| **Alpha-Beta** | 90% | 8,567 - 70,419 | 0.006s - 0.030s | Production, all lengths |

**Key Finding**: Alpha-Beta pruning reduces node exploration by up to 91% while maintaining identical strategic quality, making it vastly superior for strings longer than 20 bits.

## Installation and Setup

### Prerequisites
```bash
python --version  # Requires Python 3.7 or higher
```

Python's tkinter library is typically included with standard Python installations. If not installed:
- **Windows**: Reinstall Python with "tcl/tk" option checked
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: Should be included by default

### Running the Game

1. Clone the repository:
```bash
git clone https://github.com/Borinskii/Practical_Assignment_Team14.git
cd Practical_Assignment_Team14
```

2. Run the game:
```bash
python Main2.py
```

No additional dependencies or pip installations are required.

## Usage

### Game Configuration

When you start the game, you'll configure:

1. **String Length** (15-25): Longer strings provide more strategic depth
2. **First Player**: Choose whether you or the AI plays first
3. **AI Algorithm**: 
   - **Minimax**: Traditional algorithm, explores more nodes
   - **Alpha-Beta**: Optimized algorithm, same quality with better performance (recommended)

### Playing the Game

During gameplay:
- The binary string and current scores are displayed
- On your turn, select an index position (0 to string_length-2)
- The pair at that position will be transformed according to the game rules
- The AI will make its move automatically
- Game continues until only one bit remains

### Winning Strategies

- Look for `00` and `11` pairs: These give you points
- Avoid `01` pairs when possible: These benefit your opponent
- Use `10` strategically: Can reduce opponent's score
- Think ahead about which pairs will be available after your move

## Technical Implementation

### Project Structure

```
Practical_Assignment_Team14/
├── Main2.py                 # Game controller and main loop
├── GameTree2new.py          # AI algorithms (Minimax, Alpha-Beta)
├── GameStates.py            # Game state management
├── Gui2.py                  # Tkinter GUI interface
├── README.md                # This file
└── docs/
    └── Report.pdf          # Full experimental analysis
```

### Data Structures

**Node Class**: Represents a game state with:
- Unique node ID
- Current binary string
- Player 1 and Player 2 scores
- Tree level
- Heuristic evaluation value

**GameStates Class**: Tracks game progression by storing:
- List of states that have occurred
- Current game state
- Methods to add nodes and retrieve current state

**Game_Tree Class**: Full tree representation (used for analysis):
- Set of all possible nodes
- Set of arcs connecting nodes
- Methods for adding nodes and connections

### Heuristic Evaluation Function

The evaluation function considers four factors:

1. **Node String Score (eval_score)**: Calculated by evaluating potential of each pair in the string
   - `00` → +1 (favorable for current player)
   - `01` → -1 (favorable for opponent)
   - `10` → +1 (reduces opponent score)
   - `11` → +1 (favorable for current player)

2. **Player Role**: Determines whether to maximize or minimize
   - Maximizer (first player): Wants to increase p1 - p2
   - Minimizer (second player): Wants to increase p2 - p1

3. **Score Differential**: Current point advantage or disadvantage

4. **Turn Indicator**: Whose turn it is affects how string score is applied
   - Turn = 1 for maximizer's turn
   - Turn = -1 for minimizer's turn

**Final Formula**:
```python
if player_is_maximizer:
    return (node.p2 - node.p1) + turn * eval_score
else:
    return (node.p1 - node.p2) + turn * eval_score
```

### Algorithm Implementations

#### Minimax Algorithm

**Concept**: Recursively explores the game tree, alternating between maximizing and minimizing players. Assumes both players play optimally.

**Properties**:
- Time Complexity: O(b^d) where b = branching factor, d = depth
- Space Complexity: O(d) due to recursion stack
- Guarantees optimal play within search depth limit

**Implementation Details**:
```python
def minimax(node, depth, is_maximizing, max_depth, player_is_maximizer):
    # Base case: reached max depth or terminal state
    if depth == max_depth or len(node.string) == 1:
        return heuristic(node, turn, player_is_maximizer)
    
    # Generate all possible next moves
    children = generate_children(node, is_maximizing)
    
    if is_maximizing:
        # Maximizer tries to maximize score
        return max(minimax(child, depth+1, False, ...) for child in children)
    else:
        # Minimizer tries to minimize score
        return min(minimax(child, depth+1, True, ...) for child in children)
```

#### Alpha-Beta Pruning

**Concept**: Optimizes Minimax by eliminating branches that cannot affect the final decision. Uses two bounds (alpha and beta) to track best guaranteed outcomes.

**Properties**:
- Time Complexity: O(b^(d/2)) in best case (with optimal move ordering)
- Space Complexity: O(d)
- Produces identical results to Minimax but much faster

**Cutoff Conditions**:
- **Beta cutoff**: When maximizing, if alpha ≥ beta, stop exploring (maximizer has better option elsewhere)
- **Alpha cutoff**: When minimizing, if alpha ≥ beta, stop exploring (minimizer has better option elsewhere)

**Implementation Details**:
```python
def alpha_beta(node, depth, alpha, beta, is_maximizing, max_depth, player_is_maximizer):
    if depth == max_depth or len(node.string) == 1:
        return heuristic(node, turn, player_is_maximizer)
    
    children = generate_children(node, is_maximizing)
    
    if is_maximizing:
        value = -infinity
        for child in children:
            value = max(value, alpha_beta(child, depth+1, alpha, beta, False, ...))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff - prune remaining branches
        return value
    else:
        value = +infinity
        for child in children:
            value = min(value, alpha_beta(child, depth+1, alpha, beta, True, ...))
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff - prune remaining branches
        return value
```

### Move Generation and Selection

**For AI Moves**:
1. Generate all possible moves from current state
2. Evaluate each move using Minimax or Alpha-Beta (depth = 4)
3. Select move with highest evaluation score
4. If multiple moves have same score, choose randomly among them

**For Player Moves**:
1. Player selects index position
2. Validate move is legal (index in valid range)
3. Apply game rules to transform string
4. Update scores accordingly
5. Add new state to game history

## Experimental Analysis

### Methodology

**Experimental Design**:
- 20 total experiments (10 per algorithm)
- Variables: String length (15-25), turn order (player/AI first), algorithm choice
- Metrics tracked: Nodes visited, execution time per move, game outcome
- Control: Consistent starting configurations for fair comparison

**Data Collection**:
- Instrumented code to count node visits
- Measured execution time for each AI move
- Recorded final scores and winner for each game

### Results Summary

**Minimax Performance**:
- Win Rate: 90% (9 wins, 1 loss in 10 games)
- Node Exploration: 48,272 to 750,776 nodes depending on string length
- Response Time: 0.026s to 0.222s per move
- Observation: Performance degrades significantly with longer strings

**Alpha-Beta Performance**:
- Win Rate: 90% (9 wins, 1 draw in 10 games)
- Node Exploration: 8,567 to 70,419 nodes (83-91% reduction vs Minimax)
- Response Time: 0.006s to 0.030s per move (5-10x faster)
- Observation: Maintains efficiency across all string lengths

### Key Findings

1. **Equivalent Strategic Quality**: Both algorithms achieve 90% win rate, demonstrating that Alpha-Beta pruning does not sacrifice decision quality for speed.

2. **Dramatic Efficiency Improvement**: Alpha-Beta explores 83-91% fewer nodes than Minimax while making identical strategic choices.

3. **Scalability**: Minimax struggles with strings longer than 20 bits (750k+ nodes), while Alpha-Beta handles all lengths efficiently (max 70k nodes).

4. **Real-time Performance**: Alpha-Beta maintains sub-30ms response time across all game states, making it suitable for real-time gameplay.

5. **Practical Recommendation**: Alpha-Beta is superior for production use due to its efficiency without strategic compromise.

### Performance Comparison Table

| String Length | Minimax Nodes | Alpha-Beta Nodes | Reduction | Minimax Time | Alpha-Beta Time |
|---------------|---------------|------------------|-----------|--------------|-----------------|
| 15-16 | 48,272 - 95,568 | 8,567 - 18,448 | ~80% | 0.026s - 0.040s | 0.006s - 0.012s |
| 17-21 | 95,568 - 229,408 | 18,448 - 51,616 | ~78% | 0.040s - 0.073s | 0.012s - 0.030s |
| 22-25 | 381,469 - 750,776 | 43,654 - 70,419 | ~91% | 0.123s - 0.222s | 0.024s - 0.030s |

## Design Decisions

**Depth-4 Search**: Balances computational cost (under 0.3s per move) with strategic depth (4-move lookahead), achieving 90% win rate against human players.

**Tkinter GUI**: Chosen for being part of Python standard library (no extra dependencies), cross-platform compatibility, and sufficient functionality for turn-based games.

**Separate GameStates and Game_Tree Classes**: GameStates provides lightweight tracking during gameplay, while Game_Tree stores full structure for analysis and experimentation.

## Files and Code Organization

### Core Game Files

**Main2.py**: Game controller
- Initializes GUI and game state
- Manages turn-based gameplay loop
- Handles player input and AI move execution
- Controls game flow from setup to completion

**GameTree2new.py**: AI algorithms and game logic
- Node and Game_Tree class definitions
- Minimax algorithm implementation
- Alpha-Beta pruning implementation
- Heuristic evaluation function
- Move generation logic
- AI move selection

**GameStates.py**: Game state management
- GameStates class definition
- Methods to track game progression
- State history management

**Gui2.py**: User interface
- Setup screen for game configuration
- Gameplay screen with string display and move input
- End screen with results and replay option
- Error handling and validation

### Documentation

**docs/Report.pdf**: Complete analysis document including:
- Detailed game description
- Screenshots demonstrating gameplay
- Algorithm explanations with code
- Complete experimental results
- Performance analysis and conclusions

## Troubleshooting

### Common Issues

**"tkinter not found"**:
- Reinstall Python with tcl/tk support enabled
- On Linux: Install python3-tk package
- On macOS: Tkinter should be included; verify Python installation

**Game feels slow**:
- Use shorter strings (15-18 bits)
- Select Alpha-Beta algorithm instead of Minimax
- Ensure no other CPU-intensive applications are running

**Invalid move error**:
- Ensure index is between 0 and (current_string_length - 2)
- Remember string length decreases by 1 after each move
- Only positions with adjacent pairs can be selected

## Possible Future Enhancements

- Transposition tables for caching repeated game states
- Iterative deepening for flexible time management
- Adjustable AI difficulty levels (variable search depth)
- Move hint system for learning
- Game replay and analysis mode
- Web-based interface for online play
- Machine learning-based heuristic optimization

## References and Resources

- Russell, S. & Norvig, P. "Artificial Intelligence: A Modern Approach" - Game-playing algorithms and heuristic design
- Course Materials: Fundamentals of Artificial Intelligence, RTU ORTUS

## License

This project is part of academic coursework at Riga Technical University. Available for educational reference and non-commercial use.


**Built with Python | Powered by AI Algorithms | Riga Technical University 2025**
