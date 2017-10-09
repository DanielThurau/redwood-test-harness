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
#      and at time2 participant <maker> has bid <bid>
#      and at time2 participant <maker> has offer <offer>
      and at time2 participant <maker> has spread <spread>
      and at time2 participants besides <maker> have profit 0
    
    Examples:
      | maker | bid | offer | profit | sniper | spread |
      | 0     | 109 | 111   | 0      | 1      | 2      |
      | 1     | 109 | 111   | 0      | 2      | 2      |
      | 2     | 109 | 111   | 0      | 3      | 2      |
      | 3     | 109 | 111   | 0      | 0      | 2      |


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
    | 2      | 109  | 111    | 1      | 109  | 111    | 2       | 2       |
    | 3      | 109  | 111    | 2      | 109  | 111    | 2       | 2       | 



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
    Then at time1 participant <maker> has bid <bid>
      and at time1 participant <maker> has offer0 <offer>
      and at time1 participant <maker> has profit 110 - <offer0>
      and at time1 participants besides <maker> have profit 0
      
  Examples:
    | maker | bid | offer | sniper |
    | 1     | 109 | 111   | 2      |
    | 2     | 109 | 111   | 3      |
    | 3     | 109 | 111   | 4      |
    | 4     | 109 | 111   | 1      |
  
            

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
    | 3      | 4      | 109 | 111   | 2      |
    | 4      | 1      | 109 | 111   | 2      |



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
    | 3     | 109 | 111   | 4       | 1       |
    | 4     | 109 | 111   | 1       | 2       |
        