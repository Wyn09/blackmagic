# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Final Fantasy XIV Black Mage job simulator that models the complex elemental magic system. The simulator tracks mana consumption, elemental phases (Ice/Fire), and skill interactions through keyboard input.

## Running the Application

```bash
python test.py
```

The application runs interactively, listening for keyboard input to cast skills. Press ESC to exit. It will run 20 skill casting iterations by default.

## Core Architecture

### State Management System

The BlackMage class manages a complex state machine with three elemental phases:
- **Ice Phase** (`status < 0`): Values -1 to -3 representing Ice I, II, III
- **Neutral Phase** (`status == 0`): No elemental affinity
- **Fire Phase** (`status > 0`): Values 1 to 3 representing Fire I, II, III

The state transitions follow FFXIV's Black Mage mechanics where:
- Ice spells restore mana in Ice phase and cost mana in Fire phase
- Fire spells cost double mana in Fire phase unless using ice needles
- Transitioning between phases has special mana consumption rules

### Key State Tracking

- `status`: Current elemental phase (-3 to 3)
- `status_list`: History of recent status changes (limited to 5 entries)
- `ice_needle`: Counter for ice needle procs (max 3, consumed to reduce Fire spell costs)
- `paradox`: Determines which spell variant to use when keyboard conflict exists (skills 5, 6, 10 share keyboard "2")
- `magic`: Current mana (0-10000)

### Mana Calculation Logic (`exam_magic`)

Mana consumption varies based on:
1. Current elemental phase
2. Previous elemental phase (from `status_list`)
3. Ice needle availability
4. Skill being cast

Ice spells in Ice phase restore mana: base 3200 + (1600 × ice phase level). Fire spells in Fire phase cost double unless:
- Coming from Ice phase (costs 0)
- Using ice needle charges

### Paradox Resolution (`exam_paradox`)

The paradox system resolves keyboard conflicts for skills 5, 6, and 10 (all bound to "2"):
- Switches to Fire Paradox (skill 10) when: Fire III phase + previous Ice III phase + 3 ice needles
- Switches to Ice Paradox (skill 5) when: Ice III phase + previous Fire III phase
- Defaults to Fire I (skill 6) otherwise

## Data Structure

`skills.json` defines all skills with:
- `type`: "gcd" (global cooldown) or "capability" (off-GCD ability)
- `name`: Skill name (Chinese)
- `cast_time`/`recast_time`: Timing in seconds
- `keyboard`: Input binding
- `consumption`: Base mana cost
- `cd`/`cumulation`: Cooldown properties for capabilities

## Dependencies

- `pynput`: Keyboard input capture
- `json`: Skills data loading

The simulator uses real-time keyboard listening with `pynput.keyboard.Listener`.
