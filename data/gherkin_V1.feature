Feature: value jump
  Test events following a value jump, under varying conditions
    
  Background: default state of the experiment
    Given global default parameters
      | parameter    | value  |
      | V0           | 100    |
      | delta_slow   | 500    |
      | delta_fast   | 250    |
      | delta_eps    | 10     |
      | trigger_time | 5000   |
    Given there are 4 participants
      and default parameters
        | parameter  | value  |
        | status     | out    |
        | speed      | slow   |
        | bid0       | 99     |
        | offer0     | 101    |
      and session lasts 10 seconds
            
  Scenario Outline: 1 fast maker and 1 slow sniper
    Given default parameters for users
      but participant <maker> has status updated to make
      and participant <maker> has speed updated to fast
      and participant <sniper> has status updated to snipe
    When V jumps to 110 at trigger_time
      and market state is recorded at
        | time1                             | time2                             |
        | trigger_time+delta_slow-delta_eps | trigger_time+delta_slow+delta_eps |
      and session runs to completion
    Then at time1 system is in initial state except V is 110
      and at time2 participant <maker> has profit <profit>
      and at time2 participant <maker> has bid <bid>
      and at time2 participant <maker> has offer <offer>
      and at time2 participants besides <maker> have profit 0
    
    Examples:
      | maker | bid | offer | profit | sniper |
      | 1     | 109 | 111   | 0      | 2      |
      | 2     | 109 | 111   | 0      | 3      |
      | 3     | 109 | 111   | 0      | 4      |
      | 4     | 109 | 111   | 0      | 1      |

