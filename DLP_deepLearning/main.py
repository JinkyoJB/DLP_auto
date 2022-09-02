import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
from customDataset import customDataset
from subFunction import *
from CNN import *
import torch.nn.functional as F
import torchvision.transforms as transforms

import GPUtil
GPUtil.showUtilization()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# hyperparameters
in_channel = 3
num_classes = 5
num_epochs = 100
batch_sizes = [16]
learning_rates = [0.0001]
classes = ['normal', 'sub_normal', 'critical', 'pore', 'minor_defect']

trans = transforms.Compose(
    [transforms.ToTensor(), transforms.Resize(128), transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

# load data
dataset = customDataset(csv_file='output.csv', root_dir='./7_DLP_dataset/', transform=trans)

# 학습용 이미지를 batchsize 1개만큼 무작위로 가져오기
# train_size = int(0.8 * len(dataset))
# val_size = int(0.1 * len(dataset))
# test_size = len(dataset) - train_size - val_size
#
# train_set, val_set, test_set = torch.utils.data.random_split(dataset, [train_size, val_size, test_size])
# train_loader = DataLoader(dataset=train_set, batch_size=8, shuffle=True)
# dataiter = iter(train_loader)
# images, labels = dataiter.next()
# tensor_imshow(images[0])
#
# exit()
# ----------------------------여기까지가 데이터셋 입력 관련 코드, 이제는 학습관련 코드-------------------------------------
for batch_size in batch_sizes:
    train_size = int(0.8 * len(dataset))
    # val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size  # - val_size

    train_set, test_set = torch.utils.data.random_split(dataset, [train_size, test_size])
    # train_set, val_set, test_set = torch.utils.data.random_split(dataset, [train_size, val_size, test_size])
    train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

    print(len(train_set))
    # print(len(val_set))
    print(len(test_set))
    for learning_rate in learning_rates:
        step = 0
        # model = alexnet
        # model = ResNet50()
        # model = densenet
        # model = googlenet
        model = ResNet152().to(device)

        model.to(device=device)
        model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-4)
        writer = SummaryWriter(f'runs/ResNet152-bat16-220825-100ep')

        for epoch in range(num_epochs):
            losses = []
            accuracies = []
            for batch_idx, (data, targets) in enumerate(train_loader):
                data = data.to(device=device)
                targets = targets.to(device=device)

                scores = model(data)
                # scores = scores.logits  # googlenet용
                loss = criterion(scores, targets)
                losses.append(loss.item())

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                features = data.reshape(data.shape[0], -1)
                class_labels = [classes[label] for label in targets]
                _, prediction = scores.max(1)
                num_correct = (prediction == targets).sum()
                running_train_acc = float(num_correct) / float(data.shape[0])
                accuracies.append(running_train_acc)

                writer.add_histogram('fc', model.fc.weight)
                # writer.add_histogram('fc', model.classifier.weight) # DENSENET 용
                writer.add_scalar('Training Loss', loss, global_step=step)
                writer.add_scalar('Training Accuracy', running_train_acc, global_step=step)

                # if batch_idx == 725:
                    # writer.add_embedding(features, metadata=class_labels, label_img=data, global_step=batch_idx)

                step += 1
            writer.add_hparams({'lr': learning_rate, 'bsize': batch_size},
                               {'accuracy': sum(accuracies) / len(accuracies),
                                'loss': sum(losses) / len(losses)})

            print(f'mean loss  this epoch was {sum(losses) / len(losses)}-{epoch}')
            path = f'./0825_ResNet152(100){batch_size}{learning_rate}.pth'
            torch.save(model.state_dict(), path)

# ------------------------------여기까지가 training code, 이제는 test 코드----------------------------------

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

batch_size = 16
learning_rate = 0.0001

train_set, test_set = torch.utils.data.random_split(dataset, [train_size, test_size])
test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

load_path = '0825_ResNet152(100)160.0001.pth'
# model = ResNet50().to(device)
model = ResNet152().to(device)
# model = googlenet.to(device)
# model = densenet.to(device)
# model = alexnet.to(device)
model.load_state_dict(torch.load(load_path))

step = 0
writer = SummaryWriter(f'runs/ResNet152/batchSize {batch_size} Lr {learning_rate}-0825')

num_correct = 0
num_samples = 0
class_probs = []
class_label = []
correct_num = 0
uncorrect_num = 0
model.eval()

loader = test_loader

with torch.no_grad():
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        output = model(images)
        class_probs_batch = [F.softmax(el, dim=0) for el in output]

        _, predictions = output.max(1)
        num_correct += (predictions == labels).sum()
        num_samples += predictions.size(0)

        class_probs.append(class_probs_batch)
        class_label.append(labels)

        print(f'{predictions} - {labels}')
        for i, e, a in zip(predictions, labels,images):
            if i == e:
                correct_num = correct_num +1
                print(f"correct_num = {correct_num}")
            else:
                uncorrect_num = uncorrect_num +1
                print(f"uncorrect_num = {uncorrect_num}")
                print(f"prediction is {i}, but true is{e}")
                # tensor_imshow(a.to('cpu'))
                tensor_img_save(a, i, e)

    test_probs = torch.cat([torch.stack(batch) for batch in class_probs])
    test_label = torch.cat(class_label)
    print(f"Got {num_correct} / {num_samples} with accuracy {float(num_correct) / float(num_samples) * 100:.2f}")

for i in range(len(classes)):
    tensorboard_truth = test_label == i
    tensorboard_probs = test_probs[:, i]

    writer.add_pr_curve(classes[i], tensorboard_truth, tensorboard_probs, global_step=0)
    i = i + 1