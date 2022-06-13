# Spatio-Temporal EEG Representation Learning on Riemannian Manifold and Euclidean Space (TF v1.14.0)

[Spatio-Temporal EEG Representation Learning on Riemannian Manifold and Euclidean Space](https://arxiv.org/abs/2008.08633)

<p align="center">
  <img 
    width="800"
    height="300"
    src="/doc/architecture.jpg"
  >
</p>


This repository contains the source code of the above mentioned paper with some modifications done for NN final project, using following datasets:

- Motor Imagery: 

    - [BCI-IV 2a](https://www.bbci.de/competition/iv/#dataset1): 9 subjects were involved in motor-imagery experiment (left hand, right hand, feet and tongue). 22 EEG recordings were collected at sampling rate of 250Hz. 


    - [BCI-IV 2b](https://www.bbci.de/competition/iv/#dataset1): 9 subjects were involved in motor-imagery experiment (left hand and right hand). 3 EEG channels were recorded at sampling rate of 250Hz. 


## Prerequisites
Please follow the steps below in order to be able to train the models:


1 - Install Requirements

```
pip3 install -r ./requirements.txt
```


2 - Download dataset, install biosig toolbox by downloading and running install.m, and run conversion.m to convert from gdf to mat BCI_IV datasets. Store .mat files in /code/DATA/BCI_IV_2a or /code/DATA/BCI_IV_2b folders. Download labels for the dataset and place them in the corresponding true_label folders. Create separate folders (e.g., '/train/EEG/' and '/train/Extracted Features') for each dataset train and test folders. Check if data and labels are placed correctly with the address shown in functions 'load_dataset_signal_addr' and 'load_dataset_feature_addr' from [utils](./code/utils.py). 

3 - To [load data](./code/load_data.py), proprocess data through [filter bank](./code/library/signal_filtering.py), then perform [feature extraction](./code/library/feature_extraction.py), just run test_filewise.py changing dataset name.

4 - Perform a hyper-parameters search for each information stream. 

(1) For spatial information stream, run `python3 ./main_spatial_val.py --dataset datasetname` to search for the rank of EEG covariance matrices. For example, run the following command
```
python3 ./main_spatial_val.py --dataset BCI_IV_2a --cpu-seed 0 --gpu-seed 12345 --lr 0.001 --batch-size 32 --epochs 200 --early-stopping 20 --riemannian_dist
```
for the BCI_IV_2a dataset using Riemannian projection. 

(2) For temporal information stream, run `python3 ./main_temporal_val.py --dataset datasetname` to obtain the result for different LSTM settings. For example, run the following command
```
python3 ./main_temporal_val.py --dataset BCI_IV_2a --cpu-seed 0 --lr 0.001 --batch-size 8 --epochs 200 --early-stopping 20 --layer-num 2
```

Validation results will be automatically saved in the address in functions 'save_spatial_val_result' and 'save_temporal_val_result' from [utils](./code/utils.py). The parameters are saved and updated in [dataset_params](./code/dataset_params.yaml).

5 - Run the experiments for test data. For example, run the following command
```
python3 ./main.py --dataset BCI_IV_2b --cpu-seed 0 --lr 0.001 --batch-size 32 --epochs 200 --early-stopping 100 --riemannian_dist 
```
for the BCI-IV 2b dataset.


 ## Document Description
 
- `\code\library`:   Riemannian embedding estimation, feature preprocessing and extraction files
 
- `\code\model`:     Models for spatial, temporal and spatio-temporal streams of our architecture. 
 


If you find this material useful, please cite the following article:

## Citation
```
@article{zhang2020rfnet, 
  title={Spatio-Temporal EEG Representation Learning on Riemannian Manifold and Euclidean Space},
  author={Zhang, Guangyi and Etemad, Ali},
  journal={arXiv preprint arXiv:2008.08633},
  year={2020}
}
```




## Contact
Should you have any questions, please feel free to contact the author at [guangyi.zhang@queensu.ca](mailto:guangyi.zhang@queensu.ca).
For any question regarding this repository contact me [bota.duisenbay@gmail.com](mailto:bota.duisenbay@gmail.com).



<!-- <img src="/doc/architecture.pdf" width="400" height="200">
 -->
