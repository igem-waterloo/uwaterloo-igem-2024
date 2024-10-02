import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

class MethaneDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        data = self.data[idx]
        label = self.labels[idx]

        data = torch.tensor(data, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.float32)

        return data, label
    
class MethaneModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.batch_norm1 = nn.BatchNorm1d(64)

        self.fc2 = nn.Linear(64, 32)
        self.batch_norm2 = nn.BatchNorm1d(32)

        self.fc3 = nn.Linear(32, 16)
        self.batch_norm3 = nn.BatchNorm1d(16)

        self.output = nn.Sequential(
            nn.Linear(16, 1),
            nn.Softplus()
        )

        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        x = F.relu(self.batch_norm1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.batch_norm2(self.fc2(x)))
        x = self.dropout(x)
        x = F.relu(self.batch_norm3(self.fc3(x)))
        x = self.output(x)
        return x
 

class MethaneDenseModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.batch_norm1 = nn.BatchNorm1d(128)

        self.fc2 = nn.Linear(128 + input_size, 64)
        self.batch_norm2 = nn.BatchNorm1d(64)

        self.fc3 = nn.Linear(128 + input_size + 64, 16)
        self.batch_norm3 = nn.BatchNorm1d(16)

        self.output = nn.Sequential(
            nn.Linear(16, 1),
            nn.Softplus()
        )

        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        x1 = F.relu(self.batch_norm1(self.fc1(x)))
        x1 = self.dropout(x1)

        x2_input = torch.cat((x, x1), dim=1)
        x2 = F.relu(self.batch_norm2(self.fc2(x2_input)))
        x2 = self.dropout(x2)

        x3_input = torch.cat((x2, x2_input), dim=1)
        x3 = F.relu(self.batch_norm3(self.fc3(x3_input)))
        
        x3 = self.output(x3)
        return x3
    

class MethaneResNet(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.batch_norm1 = nn.BatchNorm1d(128)

        self.fc2 = nn.Linear(128, 64)
        self.batch_norm2 = nn.BatchNorm1d(64)

        self.fc3 = nn.Linear(64, 16)
        self.batch_norm3 = nn.BatchNorm1d(16)

        self.output = nn.Sequential(
            nn.Linear(16, 1),
            nn.Softplus()
        )

        self.dropout = nn.Dropout(0.5)

        self.skip1 = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU()
        )
    
    def forward(self, x):
        skip = self.skip1(x)

        x = F.relu(self.batch_norm1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.batch_norm2(self.fc2(x)))
        x = self.dropout(x)
        x = F.relu(self.batch_norm3(self.fc3(x)))
        x = self.output(x + skip)

        return x