*** Settings ***
Library   OperatingSystem
Library   Collections
Library   String
Library   BuiltIn
Library   Share
Resource   ../Pages/keywords.robot

*** Keywords ***

Test Suite Setup
    ${env}=   Load Env
    FOR   ${key}   IN   @{env.keys()}
       ${key_upercase}=   Convert To Upper Case   ${key}
       Set Global Variable   ${${key_upercase}}   ${env['${key}']}
    END
    Navigate To URL

Test Suite Teardown
    Close Browser

Get Core Project Path
    ${core_path}=   Get Core Path
    Set Global Variable   ${CORE_PROJECT_PATH}   ${core_path}

Get Local Setup Data
    ${file}=    Get File   ${EXECDIR}${/}Resources${/}setup.json
    ${tmp}=   Evaluate   json.loads('''${file}''')    json
    Set Global Variable   ${local_setup_data}   ${tmp}

Single Testcase Setup
    Get Test Suite Name
    Get Current Tag
    Set Data

Get Test Suite Name
    ${results}=   Convert To Lower Case   ${SUITE_NAME}
    @{words}=   Split String   ${results}   .
    Set Global Variable   ${CURRENT_SUITE_NAME}   ${words[1]}

Get ${module} Data
    ${file}=    Get File   ${EXECDIR}${/}Resources${/}${module}.json
    ${json_data}=   Evaluate   json.loads('''${file}''')    json
    Set Global Variable   ${data}   ${json_data}
    RETURN   ${json_data}

Set Data
    ${tmp}=  Get ${CURRENT_SUITE_NAME} Data
    Set Test Variable   ${data}   ${tmp['${current_tag}']}

Get Current Tag
    ${tag}=   Set Variable   @{TEST TAGS}
    Set Test Variable   ${current_tag}   ${tag}

Navigate To URL
    Start Browser
    Go To   ${base_url}
