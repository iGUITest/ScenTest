import os
from MobileKG.WidAnalysis.CNN import CNN

cnn = CNN()

input_path = ''
result = []


def get_classification(image):
    # for i in os.listdir(input_path):
    y = cnn.predict(image)
    return y


