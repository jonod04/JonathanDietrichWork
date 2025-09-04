import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms



def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    data = datasets.FashionMNIST('./data', train=training, download=True, transform=transform)
    data_loader = torch.utils.data.DataLoader(data, batch_size=64, shuffle=training)
    return data_loader



def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28*28, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10)
    )
    return model


def build_deeper_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    deep_model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28*28, 256),
        nn.ReLU(),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 10)
    )
    return deep_model


def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    
    total_dataset_size = len(train_loader.dataset)
    for epoch in range(T):
        running_loss = 0.0
        correct = 0
        total = 0
        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * data.size(0)
            _, predicted = torch.max(output, 1)
            correct += (predicted == target).sum().item()
            total += data.size(0)
        
        avg_loss = running_loss / total
        accuracy = 100.0 * correct / total
        print(f"Train Epoch: {epoch} Accuracy: {correct}/{total}({accuracy:.2f}%) Loss: {avg_loss:.3f}")


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item() * data.size(0)
            _, predicted = torch.max(output, 1)
            correct += (predicted == target).sum().item()
            total += data.size(0)
    avg_loss = test_loss / total
    accuracy = 100.0 * correct / total
    if show_loss:
        print(f"Average loss: {avg_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
    model.eval()

    image = test_images[index].unsqueeze(0)
    output = model(image)
    probabilities = F.softmax(output, dim=1)

    top_probs, top_indices = torch.topk(probabilities, k=3, dim=1)
    top_probs = top_probs.squeeze(0)
    top_indices = top_indices.squeeze(0)
    for i in range(3):
        label = class_names[top_indices[i].item()]
        prob = top_probs[i].item() * 100
        print(f"{label}: {prob:.2f}%")

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
    
    train_loader = get_data_loader(training=True)
    test_loader = get_data_loader(training=False)
    
    model = build_model()
    train_model(model, train_loader, criterion, T=5)
    
    evaluate_model(model, test_loader, criterion, show_loss=True)
    
    test_images, _ = next(iter(test_loader))
    print("\nPrediction on one test image:")
    predict_label(model, test_images, index=1)