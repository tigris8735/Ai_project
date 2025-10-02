# app/ml/poker_model.py
import torch
import torch.nn as nn

class PokerPredictor(nn.Module):
    """Нейросеть для предсказания покерных решений"""
    
    def __init__(self, input_dim=47, hidden_dim=128, output_dim=4):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim//2),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim//2, output_dim)  # [FOLD, CHECK, CALL, RAISE]
        )
    
    def forward(self, x):
        return self.network(x)