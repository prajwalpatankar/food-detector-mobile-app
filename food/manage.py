#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import torch.nn as nn
import torchvision.models as models


class Classifier(nn.Module):
    def init(self):
        super().init()
        self.network = models.wide_resnet101_2(pretrained=True)
        number_of_features =  self.network.fc.in_features
        self.network.fc = nn.Linear(number_of_features, 101)

    def forward(self, xb):
        return self.network(xb)

    def freeze(self):
        for param in self.network.parameters():
            param.requires_grad=False
        for param in self.network.fc.parameters():
            param.requires_grad=True

    def unfreeze(self):
        for param in self.network.parameters():
            param.requires_grad=True


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
