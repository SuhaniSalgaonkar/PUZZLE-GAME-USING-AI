Sliding Puzzle Game with AI Solver
Technologies Used: Python, Pygame (for GUI), A* Algorithm (for AI), OOP Principles
Project Overview: Developed an interactive Sliding Puzzle Game (8-puzzle / NxN puzzle) using Python and Pygame, featuring both player gameplay and an AI solver powered by the A Search Algorithm* with the Manhattan Distance heuristic.

The project includes two simultaneous puzzle boards:

One for the player to interactively solve by moving tiles.

One where the AI solves the puzzle step-by-step upon command.

The game is visually rich, with a clean graphical interface, move counters, timers, and a real-time comparison pop-up at the end showing the performance of the player versus the AI.

Key Functionalities: 🎮 Player Features: Interactive Puzzle Board: Users can click adjacent tiles to move the empty space and solve the puzzle.

Timer & Move Counter: Tracks how long the user takes and how many moves they use.

Reset & Shuffle Options: Randomizes or resets the board to default state.

Win Detection: Stops the timer when the puzzle is solved.

🧠 AI Features: A Solver Implementation:* Uses Manhattan Distance to determine the shortest path to the solution.

Visual Solving: Animates the AI solving the puzzle step-by-step with a delay between moves.

Time and Move Tracking: Logs how long the AI took and how many moves were used.

🪟 Pop-up Comparison Summary: Once both the player and AI solve their puzzles, a popup window displays a side-by-side comparison:

Time taken by player vs AI

Number of moves used

Provides a gamified and competitive experience.

🧱 Architecture & Logic: Object-Oriented Design: The Puzzle class encapsulates all board-related logic such as move generation, state cloning, and goal checking.

A Solver Module:* Clean separation of logic in ai_solver.py for maintainability.

Responsive Game Loop: Uses Pygame's event handling and Clock to maintain smooth rendering.

Highlights & Achievements: Built a fully playable and intelligent sliding puzzle using Pygame from scratch.

Applied AI search algorithms effectively in a real-time gaming environment.

Implemented real-time graphics and animations for user and AI interaction.

Demonstrated strong understanding of:

GUI programming in Python

AI and pathfinding algorithms

Game logic and user experience design

Created a fun and educational tool to understand A* pathfinding.

✅ Potential Enhancements (Future Scope): Add difficulty selection (e.g., 3x3, 4x4, 5x5 puzzles).

Track high scores across sessions.

Enable pause/resume functionality.

Integrate sound effects for tile movement and puzzle completion.
