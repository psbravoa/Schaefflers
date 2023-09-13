*** Settings ***
Documentation    Image recognition
Library    SeleniumLibrary
Library    Functions.py

*** Variables ***
${ImagesPath}    ${CURDIR}${/}ImagesTest
${url}      https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}    firefox

*** Test Cases ***
Image recognition test
    [Documentation]    Test to compare two images
    [Tags]    test_images_recognition
    Start
    Wait Until Element Is Visible    xpath://img[contains(@alt,'company-branding')] 
    SeleniumLibrary.Capture Element Screenshot    xpath://img[contains(@alt,'company-branding')]    ${CURDIR}${/}ImagesTest/element.png
    SeleniumLibrary.Capture Page Screenshot    ${CURDIR}${/}ImagesTest/page.png
    Compare with python function     ${CURDIR}${/}ImagesTest/page.png     ${CURDIR}${/}ImagesTest/element.png
    #Get image information     ${CURDIR}${/}ImagesTest/page.png     ${CURDIR}${/}ImagesTest/element.png
    Finish

*** Keywords ***
Start
    Log    TEST START
    Open Browser    ${url}      ${browser}
    maximize browser window
    Title Should Be    OrangeHRM
    Set Selenium Implicit Wait  10
    Set Selenium Speed    0.1s

Compare with python function
    [Documentation]    Test using DocTest Library
    [Tags]    test_DocTest_Library
    [Arguments]    ${imagen1_r}    ${imagen2_r}
    CompareTwoImages     ${imagen1_r}     ${imagen2_r}
    
Get image information
    [Arguments]    ${imagen1_r}    ${imagen2_r}
    ImageMatchPercentage     ${imagen1_r}     ${imagen2_r}
    
Finish
    Log    TEST END
    sleep   5
    Close Browser