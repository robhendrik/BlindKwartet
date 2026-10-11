# Strategy comparison summary

games completed: 40
decisions inspected: 550
mean events: 20.00

## Outcomes

- game 0: driver=local seed=123 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 1: driver=local seed=124 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 2: driver=local seed=125 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 3: driver=local seed=126 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 4: driver=local seed=127 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 5: driver=local seed=128 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 6: driver=local seed=129 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 7: driver=local seed=130 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 8: driver=local seed=131 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 9: driver=local seed=132 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 10: driver=1 seed=123 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 11: driver=1 seed=124 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 12: driver=1 seed=125 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 13: driver=1 seed=126 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 14: driver=1 seed=127 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 15: driver=1 seed=128 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 16: driver=1 seed=129 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 17: driver=1 seed=130 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 18: driver=1 seed=131 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 19: driver=1 seed=132 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 20: driver=2 seed=123 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 21: driver=2 seed=124 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 22: driver=2 seed=125 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 23: driver=2 seed=126 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 24: driver=2 seed=127 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 25: driver=2 seed=128 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 26: driver=2 seed=129 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 27: driver=2 seed=130 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 28: driver=2 seed=131 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 29: driver=2 seed=132 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 30: driver=3 seed=123 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 31: driver=3 seed=124 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 32: driver=3 seed=125 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 33: driver=3 seed=126 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 34: driver=3 seed=127 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 35: driver=3 seed=128 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 36: driver=3 seed=129 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 37: driver=3 seed=130 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 38: driver=3 seed=131 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 39: driver=3 seed=132 scores=(2, 1, 0) winners=(0,) events=17 end=terminal

## Deviations

local vs depth 1: 20
local vs depth 2: 270
local vs depth 3: 100
depth 1 vs depth 2: 290
depth 2 vs depth 3: 280

Chronological deviations:

- game 0, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 0, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 0, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 0, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 0, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 0, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 1, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 1, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 1, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 1, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 1, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 1, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 1, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 1, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 1, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 2, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 2, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 2, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 2, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 2, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 2, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 2, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 2, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 2, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 3, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 3, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 3, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 3, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 3, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 3, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 3, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 3, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 3, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 4, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 4, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 4, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 4, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 4, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 4, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 4, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 4, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 4, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 5, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 5, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 5, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 5, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 5, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 5, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 5, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 5, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 5, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 6, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 6, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 6, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 6, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 6, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 6, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 6, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 6, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 6, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 7, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 7, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 7, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 7, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 7, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 7, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 7, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 7, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 7, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 8, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 8, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 8, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 8, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 8, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 8, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 8, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 8, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 8, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 9, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: local
- game 9, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 9, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 9, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 9, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 9, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 9, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: local
- game 9, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 9, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 10, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 10, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 10, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 10, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 10, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 10, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 10, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 10, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 10, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 11, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 11, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 11, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 11, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 11, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 11, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 11, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 11, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 11, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 12, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 12, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 12, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 12, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 12, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 12, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 12, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 12, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 12, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 13, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 13, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 13, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 13, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 13, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 13, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 13, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 13, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 13, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 14, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 14, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 14, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 14, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 14, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 14, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 14, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 14, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 14, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 15, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 15, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 15, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 15, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 15, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 15, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 15, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 15, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 15, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 16, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 16, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 16, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 16, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 16, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 16, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 16, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 16, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 16, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 17, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 17, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 17, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 17, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 17, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 17, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 17, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 17, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 17, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 18, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 18, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 18, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 18, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 18, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 18, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 18, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 18, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 18, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 19, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 1
- game 19, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 19, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 19, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 19, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 19, event 10, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 19, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 1
- game 19, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 19, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 20, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 20, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 20, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 20, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 20, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 20, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 21, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 21, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 21, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 21, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 21, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 21, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 22, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 22, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 22, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 22, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 22, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 22, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 23, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 23, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 23, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 23, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 23, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 23, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 24, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 24, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 24, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 24, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 24, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 24, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 25, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 25, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 25, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 25, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 25, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 25, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 26, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 26, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 26, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 26, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 26, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 26, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 27, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 27, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 27, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 27, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 27, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 27, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 28, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 28, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 28, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 28, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 28, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 28, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 29, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 2
- game 29, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  driver: 2
- game 29, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 29, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 29, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  driver: 2
- game 29, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 30, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 30, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 30, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 30, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 30, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 30, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 30, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 30, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 31, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 31, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 31, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 31, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 31, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 31, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 31, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 31, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 32, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 32, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 32, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 32, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 32, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 32, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 32, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 32, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 33, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 33, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 33, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 33, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 33, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 33, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 33, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 33, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 34, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 34, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 34, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 34, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 34, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 34, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 34, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 34, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 35, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 35, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 35, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 35, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 35, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 35, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 35, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 35, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 36, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 36, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 36, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 36, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 36, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 36, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 36, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 36, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 37, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 37, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 37, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 37, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 37, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 37, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 37, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 37, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 38, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 38, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 38, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 38, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 38, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 38, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 38, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 38, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 39, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  driver: 3
- game 39, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 39, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 39, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 39, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 39, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 39, event 12, actor P1, |D|=560: local-vs-3, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 39, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
