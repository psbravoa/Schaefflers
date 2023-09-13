from PIL import Image, ImageChops
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
from playwright.sync_api import Page, expect, sync_playwright
from image_similarity_measures.quality_metrics import rmse, ssim, sre



def CompareTwoImages(Im1, Im2):
    image1 = Image.open(Im1)
    x = np.array(image1.histogram())

    image2 = Image.open(Im2)
    y = np.array(image2.histogram())

    print('Array x')
    print(str(x))
    print("Length array x is: "+str(len(x)))
    for i in (x):
        print(i, end=" ")

    print('Array Y')
    print(str(y))
    print("Length array Y is: "+str(len(y)))
    for i in (y):
        print(i, end=" ")


    try:
        if len(x) == len(y):
            error = np.sqrt(((x-y) ** 2).mean())
            error = str(error)[:2]
            actual_error = float(100) - float(error)
            difference = ImageChops.difference(image1, image2).getbbox()
            print("Diferencia de imágenes -->>" + str(difference))
            if difference:
                print("Not duplicate image")
                print("Matching images in percentage: ", actual_error, "\t%")
                f = plt.figure()
                text_label = str("Matching images percentage" + str(actual_error)+"%")
                plt.suptitle(text_label)
                f.add_subplot(1,2,1)
                plt.imshow(image1)
                f.add_subplot(1,2,2)
                plt.imshow(image2)
                plt.show(block=True)
            else:
                print("Duplicate image")
                print("Matching images in percentage: ", actual_error, "%")
                f = plt.figure()
                text_label = str("Matching images percentage" + str(actual_error)+"%")
                plt.suptitle(text_label)
                f.add_subplot(1,2,1)
                plt.imshow(image1)
                f.add_subplot(1,2,2)
                plt.imshow(image2)
                plt.show(block=True)
        else:
            print("THESE IMAGES ARE NOT MATCHING")
            f = plt.figure()
            text_label = str("Not matching")
            plt.suptitle(text_label)
            f.add_subplot(1,2,1)
            plt.imshow(image1)
            f.add_subplot(1,2,2)
            plt.imshow(image2)
            plt.show(block=True)

    except ValueError as identifier:
        f = plt.figure()
        text_label = str("Matching images percentage" + str(actual_error)+"%")
        plt.suptitle(text_label)
        f.add_subplot(1,2,1)
        plt.imshow(image1)
        f.add_subplot(1,2,2)
        plt.imshow(image2)
        plt.show(block=True)
        
    return actual_error

def ImageMatchSIFT(im1, im2):
    img1 = cv2.imread(im1)  
    img2 = cv2.imread(im2) 

    #img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    #sift
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

    #feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)

    img3 = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:50], img2, flags=2)
    plt.imshow(img3),plt.show()

def Get_percentage_match_points(Img1, Image2Name):
    image_to_compare = cv2.imread(Image2Name)
    original= cv2.imread(Img1)

    # Create sift - SIFT (Scale Invariant Feature Transform) technique.
    sift = cv2.SIFT_create()
    Kp_1, desc_1 = sift.detectAndCompute(original, None)
    Kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

    #Flann
    index_params=dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    #Check if two images are equals
    if original.shape == image_to_compare.shape:
        print("The images have same size and channels")
        difference = cv2.subtract(original, image_to_compare)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
            print("The images are completely equal")
            print("Similarity: 100% (equal size and channels)")
        else:
            print("The images are not equal")
    else:
        print("The images don't have same shape")
        

    print("Keypoints original image: " + str(len(Kp_1)))
    print("Keypoints image to compare: " + str(len(Kp_2)))

    #FLANN is a library for performing fast approximate nearest neighbor searches in high dimensional spaces.
    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.006*n.distance:
            good_points.append(m)
    
    number_keypoints=0
    if len(Kp_1)<= len(Kp_2):
        number_keypoints = len(Kp_1)
    else:
        number_keypoints = len(Kp_2)

    
    percentajeSimilarity = 0
    print("Title: " + Image2Name)
    percentajeSimilarity = int((len(good_points) / number_keypoints) * 100)
    print("Similarity: " + str(int(percentajeSimilarity)) + "%\n")

    text_label = str("Matching images percentage --> " + str(int(percentajeSimilarity))+"%")
    f = plt.figure()
    plt.suptitle(text_label)
    f.add_subplot(1,2,1)
    plt.imshow(original)
    f.add_subplot(1,2,2)
    plt.imshow(image_to_compare)
    plt.show(block=True)

    return  percentajeSimilarity
    
def GetShapeImage(Img1, Img2):

    original= cv2.imread(Img1)
    image_to_compare = cv2.imread(Img2)

    #Get dimensions from the image
    dimensions = original.shape
    print('Image Dimension    : ',dimensions)

    #Get height, width, number of channels in image
    height = original.shape[0]
    width = original.shape[1]
    channels = original.shape[2]
    print('Image Height       : ',height)
    print('Image Width        : ',width)
    print('Number of Channels : ',channels)

    #Get dimensions from the image
    dimensions = image_to_compare.shape
    print('Image Dimension    : ',dimensions)

    #Get height, width, number of channels in image
    height = image_to_compare.shape[0]
    width = image_to_compare.shape[1]
    channels = image_to_compare.shape[2]
    print('Image Height       : ',height)
    print('Image Width        : ',width)
    print('Number of Channels : ',channels)



def Using_methods_IR(Img1, url, xpath, Image2Name):
    CaptureImage(Img1, url, xpath, Image2Name)
    percentajeSimilaritySSIM = get_best_ssim(Img1, Image2Name)
    percentajeSimilarityRMSE = get_best_rmse(Img1, Image2Name)
    percentajeSimilaritySRE = get_best_sre(Img1, Image2Name)
    percentajeSimilarityMP = Get_percentage_match_points(Img1, Image2Name)
    return [percentajeSimilaritySSIM, percentajeSimilarityRMSE, percentajeSimilaritySRE, percentajeSimilarityMP]


def CaptureImage(Img1, url, xpath, Image2Name):
    playwright= sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto(url)
    if url == xpath:
        page.screenshot(path= Image2Name)
    else:
        page.locator(xpath).screenshot(path=Image2Name)
    browser.close()
    playwright.stop() 

def get_best_ssim(test_image_path: str, image_dir: str) -> float:
    '''
    Evaluates SSIM (Structural similarity) between a given test image and all the images in a directory.
    Parameters:
    - test_image_path (str): Path to the test image.
    - image_dir (str): Path to the images directory.
    '''
    test_image = cv2.imread(test_image_path)
    scale_percent = 100
    width = int(test_image.shape[1] * scale_percent / 100)
    height = int(test_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    data_image = cv2.imread(image_dir)
    resized_image = cv2.resize(data_image, dim, interpolation = cv2.INTER_AREA)
    percentage = ssim(test_image, resized_image)
    percentage = int(percentage * 100)

    text_label = str("Matching images percentage --> " + str(percentage)+"%")
    f = plt.figure()
    plt.suptitle(text_label)
    f.add_subplot(1,2,1)
    plt.imshow(test_image)
    f.add_subplot(1,2,2)
    plt.imshow(data_image)
    plt.show(block=True)

    return percentage
        

def get_best_rmse(test_image_path: str, image_dir: str) -> float:
    '''
    Evaluates RMSE (Root-Mean-Squared Error) between a given test image and all the images in a directory.
    Parameters:
    - test_image_path (str): Path to the test image.
    - image_dir (str): Path to the images directory.
    '''
    test_image = cv2.imread(test_image_path)
    scale_percent = 100
    width = int(test_image.shape[1] * scale_percent / 100)
    height = int(test_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    data_image = cv2.imread(image_dir)
    resized_image = cv2.resize(data_image, dim, interpolation = cv2.INTER_AREA)
    percentage = rmse(test_image, resized_image)

    text_label = str("Error metric (0=perfect match) --> " + str(percentage))
    f = plt.figure()
    plt.suptitle(text_label)
    f.add_subplot(1,2,1)
    plt.imshow(test_image)
    f.add_subplot(1,2,2)
    plt.imshow(data_image)
    plt.show(block=True)

    return percentage
        

def get_best_sre(test_image_path: str, image_dir: str) -> float:
    '''
    Evaluates SRE (Signal to Reconstruction Error Ratio) between a given test image and all the images in a directory.
    Parameters:
    - test_image_path (str): Path to the test image.
    - image_dir (str): Path to the images directory.
    '''
    test_image = cv2.imread(test_image_path)
    scale_percent = 100
    width = int(test_image.shape[1] * scale_percent / 100)
    height = int(test_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    data_image = cv2.imread(image_dir)
    resized_image = cv2.resize(data_image, dim, interpolation = cv2.INTER_AREA)
    percentage = sre(test_image, resized_image)
    percentage = int(percentage)
    
    text_label = str("Matching images percentage --> " + str(percentage)+"%")
    f = plt.figure()
    plt.suptitle(text_label)
    f.add_subplot(1,2,1)
    plt.imshow(test_image)
    f.add_subplot(1,2,2)
    plt.imshow(data_image)
    plt.show(block=True)

    return percentage

#ImageMatchSIFT("ImagesTest/page.png", "ImagesTest/1.png")
#GetShapeImage("ImagesTest/page.png", "ImagesTest/1.png")
#porcentaje = get_best_ssim("ImagesTest/page.png", "ImagesTest/1.png")
#print(porcentaje)
