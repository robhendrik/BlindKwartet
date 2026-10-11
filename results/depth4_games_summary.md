# Strategy comparison summary

games completed: 5
decisions inspected: 77
mean events: 22.40

## Outcomes

- game 0: driver=local seed=123 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 1: driver=1 seed=123 scores=(3, 0, 0) winners=(0,) events=24 end=terminal
- game 2: driver=2 seed=123 scores=(1, 0, 2) winners=(2,) events=15 end=terminal
- game 3: driver=3 seed=123 scores=(2, 1, 0) winners=(0,) events=17 end=terminal
- game 4: driver=4 seed=123 scores=(2, 1, 0) winners=(0,) events=32 end=terminal

## Deviations

local vs depth 1: 2
local vs depth 2: 34
local vs depth 3: 17
local vs depth 4: 10
depth 1 vs depth 2: 36
depth 2 vs depth 3: 37
depth 3 vs depth 4: 13

Chronological deviations:

- game 0, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: NO value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: local
- game 0, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P3 asks A1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 0, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks A2 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: local
- game 0, event 10, actor P1, |D|=560: local-vs-3, local-vs-4, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: local
- game 0, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 4: NO value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 0, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, local-vs-4, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks B1 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: local
- game 0, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 4: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: local
- game 1, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: NO value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 1, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 1, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 1
- game 1, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P3 asks A1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 1, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks A2 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 1
- game 1, event 10, actor P1, |D|=560: local-vs-3, local-vs-4, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 1
- game 1, event 11, actor P2, |D|=310: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: NO value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 4: NO value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 1, event 12, actor P2, |D|=124: local-vs-2, local-vs-3, local-vs-4, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P3 asks C1 value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  depth 3: P3 asks B2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks B1 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 1
- game 1, event 14, actor P1, |D|=12: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks B3 value=WIN
  depth 1: P2 asks B3 value=[[0, 1, 2, 0, 0], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks C1 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 3: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  depth 4: P2 asks B3 value=[[0, 2, 1, 0, 0], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 1
- game 2, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: NO value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 2
- game 2, event 2, actor P1, |D|=9032: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: quartet A value={'kind': 'quartet', 'category': 0}
  depth 1: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: quartet A value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 4: quartet A value=[[0, 1, 0, 0, -1], [0, 1, 0, 0, -1], [0, 0, 1, 0, 0]]
  driver: 2
- game 2, event 3, actor P2, |D|=4818: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 1, -1], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  depth 4: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 2, 0, 0]]
  driver: 2
- game 2, event 5, actor P1, |D|=42: local-vs-2, local-vs-3, depth-1_vs_2, depth-3_vs_4
  local: P2 asks A2 value=LOSS
  depth 1: P2 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 2, 0, 0], [0, 0, 0, 0, -2]]
  depth 2: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P3 asks A2 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 4: P2 asks A2 value=[[0, 1, 0, 0, -1], [0, 1, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 2
- game 2, event 7, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A1 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 4: P1 asks A1 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 2, event 9, actor P3, |D|=8: local-vs-1, depth-1_vs_2
  local: P1 asks A3 value=WIN
  depth 1: P2 asks C1 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 2: P1 asks A3 value=[[0, 1, 0, 0, -1], [0, 0, 0, 0, -1], [0, 1, 1, 0, 0]]
  depth 3: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  depth 4: P1 asks A3 value=[[0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0]]
  driver: 2
- game 3, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: NO value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 3, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 3, event 4, actor P2, |D|=6720: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 3, event 6, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A1 value=WIN
  depth 1: P2 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P2 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 3
- game 3, event 8, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P2 asks A3 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 3
- game 3, event 10, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks A2 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 3, event 12, actor P1, |D|=560: local-vs-3, local-vs-4, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 3
- game 3, event 13, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2, depth-3_vs_4
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: NO value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 3
- game 3, event 14, actor P1, |D|=124: local-vs-4, depth-3_vs_4
  local: quartet B value={'kind': 'quartet', 'category': 1}
  depth 1: quartet B value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 2: quartet B value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 3: quartet B value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: P3 asks C1 value=[[2, 3, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 3
- game 4, event 1, actor P2, |D|=18064: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: NO value=False
  depth 1: NO value=[[0, 0, 0, 0, -3], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: YES value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: NO value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: NO value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 4
- game 4, event 2, actor P2, |D|=9032: local-vs-2, local-vs-3, depth-1_vs_2, depth-2_vs_3, depth-3_vs_4
  local: P1 asks A2 value=LOSS
  depth 1: P1 asks A2 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P1 asks B1 value=[[0, 0, 0, 0, -2], [0, 1, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P3 asks A1 value=[[0, 0, 0, 1, -1], [0, 1, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P1 asks A2 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 4
- game 4, event 4, actor P1, |D|=1120: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P2 asks A3 value=WIN
  depth 1: P2 asks A3 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P3 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P2 asks A3 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  driver: 4
- game 4, event 6, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A1 value=WIN
  depth 1: P3 asks A1 value=[[0, 0, 1, 0, -2], [0, 0, 0, 0, -3], [0, 0, 0, 0, -3]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 4: P3 asks A1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  driver: 4
- game 4, event 8, actor P1, |D|=560: local-vs-2, depth-1_vs_2, depth-2_vs_3
  local: P3 asks A2 value=WIN
  depth 1: P3 asks A2 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 1, 1, 1, 0], [0, 0, 0, 1, -1], [0, 0, 0, 1, -1]]
  depth 3: P3 asks A2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 4: P3 asks A2 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 4
- game 4, event 10, actor P1, |D|=560: local-vs-3, local-vs-4, depth-2_vs_3
  local: P2 asks B1 value=LOSS
  depth 1: P2 asks B1 value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P2 asks B1 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks B1 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: P3 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 4, event 11, actor P3, |D|=310: local-vs-2, local-vs-3, depth-1_vs_2, depth-3_vs_4
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: YES value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  depth 4: NO value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 4, event 12, actor P3, |D|=186: local-vs-3, local-vs-4, depth-2_vs_3
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P1 asks B2 value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P2 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  depth 4: P2 asks B1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 4, event 14, actor P3, |D|=126: local-vs-4, depth-3_vs_4
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P1 asks B2 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  depth 3: P1 asks B2 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  depth 4: P1 asks C1 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 4, event 15, actor P1, |D|=81: local-vs-2, local-vs-3, local-vs-4, depth-1_vs_2
  local: NO value=False
  depth 1: NO value=[[0, 1, 0, 0, -2], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: YES value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: YES value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 4: YES value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  driver: 4
- game 4, event 16, actor P3, |D|=45: local-vs-3, depth-2_vs_3, depth-3_vs_4
  local: P1 asks B2 value=LOSS
  depth 1: P1 asks B2 value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 2: P1 asks B2 value=[[0, 1, 1, 0, -1], [0, 0, 0, 0, -2], [0, 0, 0, 0, -2]]
  depth 3: P1 asks C2 value=[[0, 1, 1, 0, 0], [0, 0, 0, 0, -1], [0, 1, 0, 0, -1]]
  depth 4: P1 asks B2 value=[[0, 2, 0, 0, -1], [0, 0, 0, 0, -1], [0, 0, 0, 0, -1]]
  driver: 4
- game 4, event 24, actor P1, |D|=6: local-vs-3, depth-2_vs_3, depth-3_vs_4
  local: P2 asks C2 value=LOSS
  depth 1: P2 asks C2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 2: P2 asks C2 value=[[0, 2, 0, 0, -1], [0, 0, 1, 0, 0], [0, 0, 0, 0, -1]]
  depth 3: P3 asks C2 value=[[2, 2, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 0]]
  depth 4: P2 asks C2 value=[[2, 2, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]
  driver: 4
