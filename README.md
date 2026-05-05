# Multimodal Quiz Agent
A finite-state multimodal dialogue system for a virtual robot quiz game, combining speech, visual feedback, animations, and mouse/keyboard interaction.
![Demo](docs/demo.gif)

## Key Features

- Finite-state dialogue manager for structured interaction flow
- Non-blocking Pygame input handling for keyboard and mouse events
- Multimodal output using audio, screen content, and robot animations
- YAML-based dialogue script for separating content from logic
- Score and prize calculation based on quiz progression
- Synchronization mechanism to prevent audio and animation overlap

## Architecture

The system is structured around three main components:

- Dialogue Manager: finite-state machine controlling the interaction flow.
- Perception Module: handles keyboard and mouse input.
- Expressiveness Module: synchronizes speech, screen content, and animations.

![State diagram](docs/state_diagram.png)
