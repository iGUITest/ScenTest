from MobileKG.GenerateKG.operation.FeatureExtract import FeatureExtract
from MobileKG.GenerateKG.operation.GenerateGraph import GenerateGraph
import os
from MobileKG.Config.RunConfig import *
from MobileKG.GenerateKG.operation.RelationExtract import RelationExtract


# data transformation
def analyze():
    """
    This function is responsible for preprocessing the data, calling the FeatureExtract class for feature extraction.
    It reads data from the original data path and saves the results to the analysis data path.

    - original_data_path: The path to the original data
    - analyze_data_path: The path where the result is saved
    """
    print('Begin Transformation')
    original_path = original_data_path
    result_path = analyze_data_path
    trans = FeatureExtract(None, original_path, result_path)
    trans.execute()
    print('Transformation Complete')
    return


def connect():
    """
    This function handles the data connection operation. It traverses the data directories, retrieves subdirectories,
    and performs connection operations using the RelationExtract class to generate connected data.

    - dirs: A list of subdirectory paths
    - ocr_similarity, opt_similarity, operation_input_similarity, connect_data_path, generate_supply_path: Parameters for RelationExtract
    """
    print('Begin Connection')
    root = analyze_data_path + '/'
    dirs = []
    apps = os.listdir(root)
    for app in apps:
        path = os.listdir(root + app)
        for p in path:
            dirs.append(root + app + '/' + p)
    # dirs=[root+'MaoYan/MaoYan-01']
    c = RelationExtract(dirs, ocr_similarity, opt_similarity, operation_input_similarity, connect_data_path, generate_supply_path)
    c.execute()
    print('Connection Complete')


def generate():
    """
    This function is responsible for calling the GenerateGraph class to generate a knowledge graph (KG).
    It will perform the graph generation operation in the specified path.

    - generate_data_path: The path where the generated graph data will be saved
    """
    print('Begin KG Generation')
    gen = GenerateGraph(generate_data_path)
    gen.execute()
    print('KG Generation Complete')
    return


# analyze()
# connect()
generate()
