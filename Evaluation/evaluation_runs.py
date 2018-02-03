import pandas as pd
import numpy as np
from Evaluation import nearest_neighbor
from Pipeline import evaluateMatching
import Pipeline
import traceback

""" settings for eval runs """
settings_DEM = [[False, None], [True, 50], [True, 100], [True, 200]] # use_pca, #n_pca_components


def run_evaluation(path_to_pickle, use_pca=False, n_components=50, label_column_name="category", features_column_name="hidden_repr"):
  df = pd.read_pickle(path_to_pickle)

  if use_pca:
   df = nearest_neighbor.transform_vectors_with_inter_class_pca(df, class_column=label_column_name, n_components=n_components)

  labels = list(df[label_column_name].values)
  features = np.asarray([rep[0] for rep in df[features_column_name].values])

  return evaluateMatching(feature_vectors=features, labels=labels)


def run_eval_DEM_model(path_to_pickle):
  LABEL_COLUMN_NAME = "category"
  FEATURES_COLUMN_NAME = "hidden_repr"
  dicts = []
  for setting in settings_DEM:
    logger.info('Starting to evaluate matching results. Data used: {}, pca active:{}, pca components:{}'.format(path_to_pickle, setting[0], setting[1]))
    dict = run_evaluation(path_to_pickle=path_to_pickle, use_pca=setting[0], n_components=setting[1],
                   label_column_name=LABEL_COLUMN_NAME, features_column_name=FEATURES_COLUMN_NAME)
    logger.info('Finished matching evaluation. Results: \n{}'.format(dict))
    dicts.append(dict)


def run_fisher_vector_gmm_model(path_to_fv, features_type, model):
  fv, labels = Pipeline.loadFisherVectors(path_to_fv)
  logger.info(
    'Starting to evaluate matching results. Data used: {} Features used: {} Model type: {}'.format(path_to_fv, features_type, model))
  dict = evaluateMatching(feature_vectors=fv, labels=labels)
  logger.info('Finished matching evaluation. Results: \n{}'.format(dict))
  del fv # delete the memmap to close


if __name__ == '__main__':
  # set up logging
  logger = Pipeline.setup_logger(logfile_name='pipelineRuns.log')

  try:
    run_fisher_vector_gmm_model(path_to_fv="/PDFData/rothfuss/fisher_vector/fv_resnet_20bn_val", features_type="ResNet",
                                model="FisherVectorGMM50Comp")
  except Exception as e:
    logger.error(traceback.format_exc())

  try:
    run_eval_DEM_model("/PDFData/rothfuss/selected_trainings/8_20bn_gdl_optical_flow/valid_run/metadata_and_hidden_rep_df_08-09-17_17-00-24_valid.pickle")
  except Exception as e:
    logger.error(traceback.format_exc())

  try:
    run_eval_DEM_model("/PDFData/rothfuss/selected_trainings/7_20bn_mse/valid_run_backup/metadata_and_hidden_rep_df_07-26-17_16-52-09_valid.pickle")
  except Exception as e:
    logger.error(traceback.format_exc())






