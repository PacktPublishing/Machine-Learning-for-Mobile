
# coding: utf-8

# In this tutorial we'll show how to export squeezenet which is implemented and trained in pytorch to run on mobile devices.
# Before we start, you should have [pytorch](https://github.com/pytorch/pytorch), [caffe2](https://github.com/caffe2/caffe2), [onnx](https://github.com/onnx/onnx) and [onnx-caffe2](https://github.com/onnx/onnx-caffe2) installed in your environment and cloned [AICamera](https://github.com/bwasti/AICamera).
# Please checkout their github page for installation instructions.

# In[1]:


# Some standard imports
import io
import numpy as np
import torch.onnx


# The following implementation of squeezenet is from [torchvision](https://github.com/pytorch/vision/blob/master/torchvision/models/squeezenet.py).

# In[ ]:


import math
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.utils.model_zoo as model_zoo


__all__ = ['SqueezeNet', 'squeezenet1_0', 'squeezenet1_1']


model_urls = {
    'squeezenet1_0': 'https://download.pytorch.org/models/squeezenet1_0-a815701f.pth',
    'squeezenet1_1': 'https://download.pytorch.org/models/squeezenet1_1-f364aa15.pth',
}


class Fire(nn.Module):

    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes):
        super(Fire, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)


class SqueezeNet(nn.Module):

    def __init__(self, version=1.0, num_classes=1000):
        super(SqueezeNet, self).__init__()
        if version not in [1.0, 1.1]:
            raise ValueError("Unsupported SqueezeNet version {version}:"
                             "1.0 or 1.1 expected".format(version=version))
        self.num_classes = num_classes
        if version == 1.0:
            self.features = nn.Sequential(
                nn.Conv2d(3, 96, kernel_size=7, stride=2),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(96, 16, 64, 64),
                Fire(128, 16, 64, 64),
                Fire(128, 32, 128, 128),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(256, 32, 128, 128),
                Fire(256, 48, 192, 192),
                Fire(384, 48, 192, 192),
                Fire(384, 64, 256, 256),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(512, 64, 256, 256),
            )
        else:
            self.features = nn.Sequential(
                nn.Conv2d(3, 64, kernel_size=3, stride=2),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(64, 16, 64, 64),
                Fire(128, 16, 64, 64),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(128, 32, 128, 128),
                Fire(256, 32, 128, 128),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=False),
                Fire(256, 48, 192, 192),
                Fire(384, 48, 192, 192),
                Fire(384, 64, 256, 256),
                Fire(512, 64, 256, 256),
            )
        # Final convolution is initialized differently form the rest
        final_conv = nn.Conv2d(512, self.num_classes, kernel_size=1)
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            final_conv,
            nn.ReLU(inplace=True),
            nn.AvgPool2d(13)
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x.view(x.size(0), self.num_classes)


def squeezenet1_0(pretrained=False, **kwargs):
    r"""SqueezeNet model architecture from the `"SqueezeNet: AlexNet-level
    accuracy with 50x fewer parameters and <0.5MB model size"
    <https://arxiv.org/abs/1602.07360>`_ paper.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = SqueezeNet(version=1.0, **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['squeezenet1_0']))
    return model


def squeezenet1_1(pretrained=False, **kwargs):
    r"""SqueezeNet 1.1 model from the `official SqueezeNet repo
    <https://github.com/DeepScale/SqueezeNet/tree/master/SqueezeNet_v1.1>`_.
    SqueezeNet 1.1 has 2.4x less computation and slightly fewer parameters
    than SqueezeNet 1.0, without sacrificing accuracy.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = SqueezeNet(version=1.1, **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['squeezenet1_1']))
    return model


# We can get the torch model by calling the following function:

# In[2]:


# Get pretrained squeezenet model
torch_model = squeezenet1_1(True)


# and export the pytorch model as onnx model:

# In[3]:


from torch.autograd import Variable
batch_size = 1    # just a random number

# Input to the model
x = Variable(torch.randn(batch_size, 3, 224, 224), requires_grad=True)

# Export the model
torch_out = torch.onnx._export(torch_model,             # model being run
                               x,                       # model input (or a tuple for multiple inputs)
                               "squeezenet.onnx",       # where to save the model (can be a file or file-like object)
                               export_params=True)      # store the trained parameter weights inside the model file


# After that, we can prepare and run the model and verify that the result of the model running on pytorch matches the result running on onnx-caffe2 backend.

# In[4]:


import onnx
import onnx_caffe2.backend
from onnx import helper

# Load the ONNX GraphProto object. Graph is a standard Python protobuf object
model = onnx.load("squeezenet.onnx")

# prepare the caffe2 backend for executing the model this converts the ONNX graph into a
# Caffe2 NetDef that can execute it. Other ONNX backends, like one for CNTK will be
# availiable soon.
prepared_backend = onnx_caffe2.backend.prepare(model)

# run the model in Caffe2

# Construct a map from input names to Tensor data.
# The graph itself contains inputs for all weight parameters, followed by the input image.
# Since the weights are already embedded, we just need to pass the input image.
# last input the grap
W = {model.graph.input[0].name: x.data.numpy()}

# Run the Caffe2 net:
c2_out = prepared_backend.run(W)[0]

# Verify the numerical correctness upto 3 decimal places
np.testing.assert_almost_equal(torch_out.data.cpu().numpy(), c2_out, decimal=3)


# Then we can export the model to run on mobile devices, leveraging the cross-platform capability of caffe2.

# In[5]:


# Export to mobile
from onnx_caffe2.backend import Caffe2Backend as c2

init_net, predict_net = c2.onnx_graph_to_caffe2_net(model.graph, True)
with open("squeeze_init_net.pb", "wb") as f:
    f.write(init_net.SerializeToString())
with open("squeeze_predict_net.pb", "wb") as f:
    f.write(predict_net.SerializeToString())


# You'll see squeeze_init_net.pb and squeeze_predict_net.pb in the same directory of this notebook. Let's make sure it can run with predictor since that's what we'll use in the Mobile App.
# Verify it runs with predictor
with open("squeeze_init_net.pb") as f:
    init_net = f.read()
with open("squeeze_predict_net.pb") as f:
    predict_net = f.read()
from caffe2.python import workspace
p = workspace.Predictor(init_net, predict_net)
# The following code should run:
# img = np.random.rand(1, 3, 224, 224).astype(np.float32)
# p.run([img])

# After we are sure that it runs with predictor, we can copy squeeze_init_net.pb and squeeze_predict_net.pb to 
# AICamera/app/src/main/assets.
# Now we can open Android Studio and import the AICamera project, run the app by clicking the green play button.
