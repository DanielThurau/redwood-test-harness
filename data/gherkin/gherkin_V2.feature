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


Scenario Outline: 2 slow makers and no snipers
    Given default parameters for users
      but participant <maker1> has status updated to make
      and participant <maker2> has status updated to make
    When V jumps to 110 at trigger_time
      and market state is recorded at
        | time1                             | time2                             |
        | trigger_time+delta_slow-delta_eps | trigger_time+delta_slow+delta_eps |
      and session runs to completion
    Then at time1 system is in initial state except V is 110
#      and at time2 participant <maker1> has bid <bid1>
#      and at time2 participant <maker1> has offer <offer1>
#      and at time2 participant <maker2> has bid <bid2>
#      and at time2 participant <maker2> has offer <offer2>
      and at time2 participant <maker1> has spread <spread1>
      and at time2 participant <maker2> has spread <spread2>
      and at time2 all participants have profit 0
            
  Examples:
    | maker1 | bid1 | offer1 | maker2 | bid2 | offer2 | spread1 | spread2 |
    | 0      | 109  | 111    | 3      | 109  | 111    | 2       | 2       |
    | 1      | 109  | 111    | 0      | 109  | 111    | 2       | 2       | 
#    | 2      | 109  | 111    | 1      | 109  | 111    | 2       | 2       |
#    | 3      | 109  | 111    | 2      | 109  | 111    | 2       | 2       | 

