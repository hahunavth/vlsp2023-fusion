import os
import sys 
sys.path.append(os.getcwd()) # NOQA

import argparse
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from src.fusion.dataloader import TrainingDataLCNN, ValidationDataLCNN
from src.fusion.LCNN.model.lcnn import LCNN

# From ngocquan with love
from src.naive_dnn.utils import compute_eer,load_embeddings,load_pickle
from src.fusion.train import train
def main(args):

    mode = args.mode
    type_data = args.type
    if mode != "train" and mode != "test" :
        print("Type the mode equals train or test, run again")
        # Fast return
        return None
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LCNN(input_dim= 1, num_label= 2).to(device) 
    
    training_file = load_pickle(args.training_file)
    validation_file = load_pickle(args.validation_file)
    stft_embedding = load_pickle(args.stft_embedding) 
    cqt_embedding = load_pickle(args.cqt_embedding)
    stft_embedding_val = load_pickle(args.stft_embedding_val) 
    cqt_embedding_val = load_pickle(args.cqt_embedding_val)
    
    training_data = TrainingDataLCNN(path_list= training_file, stft_embedding= stft_embedding, cqt_embedding= cqt_embedding, type= type_data)
    validation_data = TrainingDataLCNN(path_list= validation_file, stft_embedding=stft_embedding_val, cqt_embedding=cqt_embedding_val)
    validation_loader = DataLoader(dataset= validation_data, batch_size= 1, shuffle= False)
    train_loader = DataLoader(dataset= training_data, batch_size= 32, shuffle= True)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr= 1e-5)
    
    if mode == "train" :
        train(model= model, optimizer= optimizer, criterion= criterion, data_loader= train_loader, num_epochs= 50, validation_loader= validation_loader)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Speaker Detection from Lab914")

    parser.add_argument(
        "--mode",
        dest="mode",
        type=str,
        help="string, only receive value train or test, depend on training or testing",
        default="train",
    )
    parser.add_argument(
        "--type",
        dest="type",
        type=str,
        help="string, only receive value stft or cqt",
        default="train",
    )

    parser.add_argument(
        "--training_file",
        dest="training_file",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    parser.add_argument(
        "--stft_embedding",
        dest="stft_embedding",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    parser.add_argument(
        "--cqt_embedding",
        dest="cqt_embedding",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    parser.add_argument(
        "--stft_embedding_val",
        dest="stft_embedding_val",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    parser.add_argument(
        "--cqt_embedding_val",
        dest="cqt_embedding_val",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    parser.add_argument(
        "--validation_file",
        dest="validation_file",
        type=str,
        help="",
        default="Dien di dung luoi :) ",
    )
    main(parser.parse_args())