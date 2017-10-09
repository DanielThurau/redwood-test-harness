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

  Scenario Outline: 2 fast makers and 1 fast sniper
    Given default parameters for users
      but participant <maker1> has status updated to make
      and participant <maker1> has speed updated to fast
      and participant <maker2> has status updated to make
      and participant <maker2> has speed updated to fast
      and participant <sniper> has status updated to snipe
      and participant <sniper> has speed updated to fast
    When V jumps to 110 at trigger_time
      and session runs to completion
        | time1                             | time2                             |
        | trigger_time+delta_fast-delta_eps | trigger_time+delta_fast+delta_eps |
     Then at time1 system is in initial state except V is 110
      and at time2 participant <maker1> has bid <bid>
      and at time2 participant <maker1> has offer <offer>
      and at time2 participant <maker2> has bid <bid>
      and at time2 participant <maker2> has offer <offer>
      and at time2 participant <maker1> has profit <profitM1> and <maker2> has profit <profitM2> and <sniper> has profit <profitS> where <profitM1> and <profitM2> and <profitS> are one of the following cases
        | profitM1 | profitM2 | profitS |
        | 0        | 0        | 0       |
        | -1       | 0        | 1       |
        | 0        | -1       | 1       |          
  Examples:
    | maker1 | maker2 | bid | offer | sniper |
    | 1      | 2      | 109 | 111   | 3      |
    | 2      | 3      | 109 | 111   | 4      |
#    | 3      | 4      | 109 | 111   | 2      |
#    | 4      | 1      | 109 | 111   | 2      |
