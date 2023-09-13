*** Settings ***
Documentation    Image recognition
Library    SeleniumLibrary
Library    ImageCompare   
Library    DocTest.VisualTest
#Test Setup    Start
#Test Teardown    Finish 

*** Variables ***
${ImagesPath}    ${CURDIR}${/}ImagesTest
${url}      https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}    firefox

*** Test Cases ***
#Image recognition

Image recognition test
    [Documentation]    Test to compare two images
    [Tags]    test_images_recognition
    Start
    Wait Until Element Is Visible    xpath://img[contains(@alt,'company-branding')] 
    SeleniumLibrary.Capture Element Screenshot    xpath://img[contains(@alt,'company-branding')]    ${CURDIR}${/}ImagesTest/element.png
    SeleniumLibrary.Capture Page Screenshot    ${CURDIR}${/}ImagesTest/page.png
    Compare with DocTest
    Finish

*** Keywords ***
Start
    Log    TEST START
    Open Browser    ${url}      ${browser}
    maximize browser window
    Title Should Be    OrangeHRM
    Set Selenium Implicit Wait  10
    Set Selenium Speed    0.1s

Compare with DocTest
    [Documentation]    Test using DocTest Library
    [Tags]    test_DocTest_Library
    #DocTest.VisualTest.Compare Images    ${CURDIR}${/}ImagesTest/elementCopy.png    ${CURDIR}${/}ImagesTest/element.png
    #DocTest.VisualTest.Compare Images    ${CURDIR}${/}ImagesTest/elementCopy2.png    ${CURDIR}${/}ImagesTest/element.png    #move_tolerance=20
    DocTest.VisualTest.Compare Images    ${CURDIR}${/}ImagesTest/pageCopy.png    ${CURDIR}${/}ImagesTest/page.png
    DocTest.VisualTest.Compare Images    ${CURDIR}${/}ImagesTest/CompareScreen.png    ${CURDIR}${/}ImagesTest/page.png    #move_tolerance=20
   
Finish
    Log    TEST END
    sleep   2
    Close Browser