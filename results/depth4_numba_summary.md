# Strategy comparison summary

games completed: 2
decisions inspected: 38
mean events: 31.00
projection backend: numba

## Outcomes

- game 0: driver=local seed=123 scores=(3, 0, 0) winners=(0,) events=27 end=terminal
- game 1: driver=4 seed=123 scores=(2, 1, 0) winners=(0,) events=35 end=terminal

## Deviations

local vs depth 4: 6

Chronological deviations:

- game 0, event 11, actor P1, |D|=560: local-vs-4
  local: P2 asks B1 value=LOSS
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: local
- game 0, event 13, actor P2, |D|=124: local-vs-4
  local: P1 asks B2 value=LOSS
  depth 4: P3 asks B1 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 1, event 11, actor P1, |D|=560: local-vs-4
  local: P2 asks B1 value=LOSS
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 1, event 13, actor P3, |D|=186: local-vs-4
  local: P1 asks B2 value=LOSS
  depth 4: P2 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 1, event 15, actor P3, |D|=126: local-vs-4
  local: P1 asks B2 value=LOSS
  depth 4: P1 asks C1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 1, event 16, actor P1, |D|=81: local-vs-4
  local: NO value=False
  depth 4: YES value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
