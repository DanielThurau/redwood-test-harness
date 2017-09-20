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


  Scenario Outline: 1 slow maker and 1 fast sniper and investor arrival before snipe
    Given default parameters for users
      but participant <maker> has status updated to make
      and participant <sniper> has status updated to snipe
      and participant <sniper> has speed updated to fast
    When V jumps to 110 at trigger_time
      and an investor arrives to buy at trigger_time+delta_fast-delta_eps
      and market state is recorded at
        | time1                             | time2                             |
        | trigger_time+delta_slow-delta_eps | trigger_time+delta_slow+delta_eps |
      and session runs to completion
    Then at time1 participant <maker> has spread <spread>
      and at time1 participant <maker> has profit 110 - <offer>
      and at time1 participants besides <maker> have profit 0
      
  Examples:
    | maker | offer | sniper | spread |
    | 1     | 111   | 2      |   2    |
    | 2     | 111   | 3      |   2    |
    | 3     | 111   | 4      |   2    |
    | 4     | 111   | 1      |   2    |
