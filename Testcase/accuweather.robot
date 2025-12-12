*** Settings ***
Resource   ../Setup/keywords.robot
Resource   ../Pages/keywords.robot

*** Test Cases ***

Weather Information Retrieve Test
    [Tags]   wearther_daily
    Set Fahrenheit Value   ${data}
    Select Location After Enter Search Field   ${data}
    Navigation And Select Item In Menu   ${data}
    ${weather_link}=    Retrieve Link Weather For All Days
    ${weather_info}=    Retrieve Weather Information For All Days   ${weather_link}
    Validate Temperature Data   ${weather_info}
    Save Weather Information To File    ${weather_info}
    Generate Summary Report    ${weather_info}

Hourly Weather Test Execution
    [Tags]    weather_hourly
    Set Fahrenheit Value   ${data}
    Select Location After Enter Search Field   ${data}
    FOR    ${i}    IN RANGE    1    25    # 24 hours
        Log    Executing hourly test iteration ${i}
        Navigation And Select Item In Menu   ${data}
        ${current_weather}=    Get Current Weather Information
        Log    Current weather: ${current_weather}
        Sleep    3    # Wait 1 hour (for demo, use shorter time)
    END
