import json
import pytest
from _pytest.fixtures import SubRequest

from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from api_functions import getS3BucketBody
from api_functions import numAndClassNameFiltered
from api_functions import fileNameAndClassNameFiltered
from api_functions import imgSizeRangeFiltered
from api_functions import aircraftPositionFilter
from api_functions import getNumRandomImages

# All Info filterd test
@pytest.mark.parametrize('filename,wifth,height,className,xmin,xmax,ymin,ymax',[('4a042db1cef213a1ed865422e6355f76',0,0,'',0,0,0,0)])
def test_getAwsS3BucketBody(filename,wifth,height,className,xmin,xmax,ymin,ymax):
    json_reponse = {'249': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F117', 'xmin': '165', 'ymin': '910', 'xmax': '496', 'ymax': '1013'}, '250': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F16', 'xmin': '35', 'ymin': '744', 'xmax': '234', 'ymax': '840'}, '251': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F16', 'xmin': '158', 'ymin': '735', 'xmax': '260', 'ymax': '827'}, '252': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F16', 'xmin': '376', 'ymin': '735', 'xmax': '625', 'ymax': '825'}, '253': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F16', 'xmin': '1325', 'ymin': '744', 'xmax': '1563', 'ymax': '835'}, '254': {'filename': '4a042db1cef213a1ed865422e6355f76', 'width': '1600', 'height': '1043', 'class': 'F117', 'xmin': '616', 'ymin': '59', 'xmax': '751', 'ymax': '110'}}
    
    assert getS3BucketBody.getS3BucketBodyInfo(filename,wifth,height,className,xmin,xmax,ymin,ymax) == json_reponse

@pytest.mark.parametrize('filename,className',[(1,2),("",""),("","F16"),("","helloworld")])
def test_getAwsS3BucketBody(filename,className):

    assert getS3BucketBody.getS3BucketBodyInfo(filename,className) != {}


# Num and Class Name filterd test
@pytest.mark.parametrize('num,className',[(1,2),("",""),(3,"F16"),("","helloworld")])
def test_AircraftNumandClassNameInput(num,className):

    assert numAndClassNameFiltered.getNumAndClassFilteredResult(num,className) != {}


# File Name and Class Name filterd test
@pytest.mark.parametrize('filename,className',[(11,12),("",""),("","F16"),("4a042db1cef213a1ed865422e6355f76","helloworld"),("4a042db1cef213a1ed865422e6355f76","F117")])
def test_fileNameAndClassNameRequest(filename,className):

    assert fileNameAndClassNameFiltered.getFileNameClassNameFilteredResult(filename,className) != {}


# Image Size Range filterd test
@pytest.mark.parametrize('width,height',[(0,0),(1000,1000),(9999,9999),(-1,-1),("1","hello"),('','')])
def test_imgSizeRangeRequest(width,height):

    assert imgSizeRangeFiltered.getimgSizeRangeFilteredResult(width,height) != {}


# Image Size Range filterd test
@pytest.mark.parametrize('xmin,ymin,xmax,ymax',[(0,0,0,0),(1,1,500,500),(-1,-1,1,1),("1","hello",999,999),('','','','')])
def test_aircraftPositionFilter(xmin,ymin,xmax,ymax):

    assert aircraftPositionFilter.getAircraftPositionFilterResult(xmin,ymin,xmax,ymax) != {}


# Image Size Range filterd test
@pytest.mark.parametrize('num',[5,8,20,-1,'123','hello'])
def test_randNumAircraftsInfoRequest(num):

    assert getNumRandomImages.getNumRandomImageFileNames(num) != {}



if __name__=='__main__':
     pytest.main()