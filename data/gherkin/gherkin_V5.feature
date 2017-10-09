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

  Scenario Outline: 1 slow maker and 2 fast snipers
    Given default parameters for users
      but participant <maker> has status updated to make
      and participant <sniper1> has status updated to snipe
      and participant <sniper1> has speed updated to fast
      and participant <sniper2> has status updated to snipe
      and participant <sniper2> has speed updated to fast
    When V jumps to 110 at trigger_time
      and market state is recorded at
        | time1                             | time2                             |
        | trigger_time+delta_slow-delta_eps | trigger_time+delta_slow+delta_eps |
      and session runs to completion
    Then at time1 system is in initial state except V is 110
      and at time2 participant <maker> has bid <bid>
      and at time2 participant <maker> has offer <offer>
      and at time2 participant <maker> has profit <profitM> and <sniper1> has profit <profitS1> and <sniper2> has profit <profitS2> where <profitM> and <profitS1> and <profitS2> are one of the following cases
        | profitM      | profitS1     | profitS2     |
        | <offer>-110  | 110-<offer>  | 0            |
        | <offer>-110  | 0            | 110-<offer>  |
    
  Examples:
    | maker | bid | offer | sniper1 | sniper2 |
    | 1     | 109 | 111   | 2       | 3       |
    | 2     | 109 | 111   | 3       | 1       |
#    | 3     | 109 | 111   | 4       | 1       |
#    | 4     | 109 | 111   | 1       | 2       |
        