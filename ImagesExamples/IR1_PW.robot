*** Settings ***
Documentation    Image recognition
Library    SeleniumLibrary
Library    Functions.py
Library    String

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
        ${strNum} =    String.Remove String     ${strNum}     ${SPACE}     ${EMPTY}
        ${nameImage} =     Catenate    SEPARATOR=       ${Captures_url}    ${strNum}
        ${nameImage} =     Catenate      SEPARATOR=      ${nameImage}    .png
        #${percentage} =    ImageMatchPercentage     ${CURDIR}${/}ImagesTest/pwScreenShoot.png         https://opensource-demo.orangehrmlive.com/web/index.php/auth/login        ${i}         ${nameImage} 
        ${percentages} =   Using_methods_IR         ImagesTest/pwScreenShoot.png     https://opensource-demo.orangehrmlive.com/web/index.php/auth/login    ${i}     ${nameImage} 
        
        #Present the percentage
        #${int} =    Builtin.Convert To Integer   ${percentage}
        Log To Console  ${i}

        ${str} =    Builtin.Convert To String    ${percentages}[0]
        ${frase}=    Catenate    Percentage Similarity SSIM -->   ${str}
        ${frase}=    Catenate    ${frase}    %
        Log To Console   ${frase}
        ${str} =    Builtin.Convert To String    ${percentages}[1]
        ${frase}=    Catenate    Percentage Similarity RMSE -->   ${str}
        ${frase}=    Catenate    ${frase}    %
        Log To Console   ${frase}
        ${str} =    Builtin.Convert To String    ${percentages}[2]
        ${frase}=    Catenate    Percentage Similarity SRE -->   ${str}
        ${frase}=    Catenate    ${frase}    %
        Log To Console   ${frase}
        ${str} =    Builtin.Convert To String    ${percentages}[3]
        ${frase}=    Catenate    Percentage Similarity Match points -->   ${str}
        ${frase}=    Catenate    ${frase}    %
        Log To Console   ${frase}
    END
    
