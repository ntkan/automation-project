*** Settings ***

Library   BuiltIn
Library   OperatingSystem
Library   Collections
Library   String
Resource  ./locators.robot

*** Keywords ***

Enter Value To Search Field
    [Arguments]   ${value}
    Wait Until Element Is Visible   ${search-input}
    Input Text   ${search-input}   ${value}

Select Location From Search Result
    [Arguments]   ${location}
    ${locator}=    Replace String   ${search-location-result}   <<param>>    ${location}
    Wait Until Element Is Visible    ${locator}
    Click Element   ${locator}

Accept Privacy Button
    ${exists}=    Run Keyword And Return Status    Wait Until Element Is Visible    ${accept-privacy-button}    timeout=3s
    IF    ${exists}
        Click Element    ${accept-privacy-button}
    END

Select Item In Navigation Menu
    [Arguments]   ${item}
    ${item_lower}=   Convert To Lower Case   ${item}
    ${locator}=    Replace String   ${menu-items}   <<param>>    ${item_lower}
    Wait Until Element Is Visible    ${locator}
    Click Element   ${locator}

Retrieve Link Weather For All Days
    Wait Cards Ready   ${content-module}
    ${weather_data}=    Create List
    ${days_elements}=    Get WebElements    ${content-modules}
    FOR    ${day_element}    IN    @{days_elements}
        ${day_info}=    Get Element Attribute   ${day_element}   href
        Append To List    ${weather_data}    ${day_info}
    END
    RETURN    ${weather_data}

Retrieve Weather Information For All Days
    [Arguments]   ${days}
    ${weather_data}=    Create List
    FOR    ${day}    IN    @{days}
        ${day_info}=    Extract Day Weather Information    ${day}
        Append To List    ${weather_data}    ${day_info}
    END
    RETURN    ${weather_data}

Close Ads If Any
    ${dismiss_ads_button}=   Is Element Visible In Time   ${dismiss-ads-button}
    IF   ${dismiss_ads_button} is ${TRUE}
        Click Element   ${dismiss-ads-button}
    END

Click Logo Button On Header
    Wait Until Element Is Visible   ${logo-icon}
    Click Element   ${logo-icon}

Click Threedot Menu
    Wait Until Element Is Visible   ${threedot-menu}
    Click Element   ${threedot-menu}

Click Settings
    Wait Until Element Is Visible   ${settings}
    Click Element   ${settings}

Select Value In Suggestion List
    [Arguments]   ${value}
    Wait Until Element Is Visible   ${unit-setting}
    Select Dropdown List Value   ${unit-setting}   ${value}

Extract Day Weather Information
    [Arguments]   ${day_element}
    Go To   ${day_element}
    Wait Cards Ready   ${content-module}
    ${weather_info}=   Create Dictionary
    ${day_value}=   Get Text   ${day-label}
    ${original_temperature}=   Get Text   ${temperature-label}
    ${temperature}=   Split String   ${original_temperature}   °Hi
    ${original_real_feel}=   Get Text   ${real-feel-label}
    ${real_feel}=   Split String   ${original_real_feel}   \n
    ${main_weather}=   Get Text   ${main-weather-label}
    ${humidity}=   Extract Humidity If Include
    ${day_info}=    Create Dictionary
    ...    day_value=${day_value}
    ...    temperature=${temperature[0]}
    ...    main_weather=${main_weather}
    ...    real_feel=${real_feel[0]}
    ...    humidity=${humidity}
    RETURN    ${day_info}

Extract Humidity If Include
    ${morning_visible}=      Run Keyword And Return Status    Element Should Be Visible    ${morning-button}
    ${afternoon_visible}=    Run Keyword And Return Status    Element Should Be Visible    ${afternoon-button}
    Run Keyword If    not (${morning_visible} or ${afternoon_visible})
    ...    Return From Keyword   N/A
    ${target_button}=    Run Keyword If    ${morning_visible}    Set Variable    ${morning-button}
    ...    ELSE    Set Variable    ${afternoon-button}
    ${day_url}=    Get Element Attribute    ${target_button}    href
    Go To    ${day_url}
    Wait Cards Ready   ${content-module}
    ${humidity}=    Get Text    ${humidity-label}
    RETURN    ${humidity}

Validate Temperature Data
    [Arguments]    ${weather_data}
    FOR    ${day_data}    IN    @{weather_data}
        ${temp_f}=    Extract Temperature Value    ${day_data['temperature']}
        ${temp_c}=    Convert Fahrenheit To Celsius    ${temp_f}
        Log    Day: ${day_data['day_value']}, Temp F: ${temp_f}°F, Temp C: ${temp_c}°C
        # Validate temperature is reasonable
        Should Be True    ${temp_f} >= -50 and ${temp_f} <= 150    Temperature ${temp_f}°F seems unreasonable
        Should Be True    ${temp_c} >= -45 and ${temp_c} <= 65    Temperature ${temp_c}°C seems unreasonable
        Set To Dictionary    ${day_data}    temperature_celsius    ${temp_c}
    END

Save Weather Information To File
    [Arguments]    ${weather_data}
    Create Weather Report File    ${weather_data}

Generate Summary Report
    [Arguments]    ${weather_data}
    ${total_days}=    Get Length    ${weather_data}
    ${summary}=    Create Weather Summary    ${weather_data}
    Log    Total days processed: ${total_days}
    Log    Weather Summary: ${summary}

Get Current Weather Information
    Wait Cards Ready   ${content-module}
    ${current_temp}=   Get Text   ${current-temperature}
    ${current_desc}=   Get Text   ${current-weather}
    ${current_time}=    Get Text    ${current-time}
    ${current_weather}=    Create Dictionary
    ...    timestamp=${current_time}
    ...    temperature=${current_temp}
    ...    description=${current_desc}
    RETURN    ${current_weather}
