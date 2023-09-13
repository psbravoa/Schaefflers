*** Settings ***
Documentation    Image recognition
Library    SeleniumLibrary
Library    Functions.py

*** Variables ***
${ImagesPath}    ${CURDIR}${/}ImagesTest
${browser}    firefox
${xpathLogo}     //img[contains(@alt,'company-branding')]
${xpathUserName}    //input[contains(@name,'username')]
${xpathfooter}    //div[contains(@class,'orangehrm-login-footer-sm')]
${xpathForgotPassword}    //p[contains(.,'Forgot your password?')]
${xpathOrange}    //div[contains(@class,'orangehrm-login-slot-wrapper')]
${url}      https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
#${xpathAdminPassword}    (//div[contains(.,'Username : AdminPassword : admin123')])[9]
${percentage}    0
${Captures_url} =     ImagesTest/

*** Test Cases ***
Image recognition test
    [Documentation]    Test to compare two images
    [Tags]    test_images_recognition
    ${int}=    BuiltIn.Set Variable    0
    ${num}=    BuiltIn.Set Variable    0
    ${num1}=    BuiltIn.Set Variable    1
    ${img2}=    BuiltIn.Set Variable    ""
    @{list1}=     Create List     ${xpathLogo}    ${xpathUserName}    ${xpathfooter}    ${xpathForgotPassword}    ${xpathOrange}    ${url}    #${xpathAdminPassword}    

    FOR    ${i}    IN    @{list1}
        #Exit For Loop If    ${percentage} > 90
        ${num} =     Evaluate    int(${num}) + int(${num1})
        ${strNum} =    Builtin.Convert To String    ${num}
        ${nameImage} =     Catenate       ${Captures_url}    strip(${strNum})
        ${nameImage} =     Catenate    SEPARATOR=    ${nameImage}    .png
        ${percentage} =    ImageMatchPercentage     ${CURDIR}${/}ImagesTest/pwScreenShoot.png     https://opensource-demo.orangehrmlive.com/web/index.php/auth/login    ${i}     ${nameImage}       #  #ImagesTest/imageToCompare.png
        
        #Present the percentage
        ${int} =    Builtin.Convert To Integer   ${percentage}
        ${str} =    Builtin.Convert To String    ${int}
        ${frase}=    Catenate    Percentage Similarity -->   ${str}
        ${frase}=    Catenate    ${frase}    %

        Log To Console  ${i}
        Log To Console   ${frase}
    END
    
