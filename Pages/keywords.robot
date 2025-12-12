*** Settings ***
Library   String
Resource    ./actions.robot

*** Keywords ***

Select Location After Enter Search Field
    [Arguments]   ${value}
    Accept Privacy Button
    Enter Value To Search Field   ${value['location']}
    Select Location From Search Result   ${value['location']}

Set Fahrenheit Value
    [Arguments]   ${value}
    Click Threedot Menu
    Click Settings
    Select Value In Suggestion List   ${value['unit-setting']}
    Click Logo Button On Header

Navigation And Select Item In Menu
    [Arguments]   ${value}
    Select Item In Navigation Menu   ${value['menu-item']}
