import numpy as np
from torch.utils.data.dataset import Dataset
np.set_printoptions(threshold=sys.maxsizegit )
import pandas as pd
import torch

# Create the training dataset for pytorch
# Deals with one image at a time


# Clip to patch for its center pixel
def img_to_patches_to_tensor(index, list_id, image, patch_size):
    id = list_id[index]
    i = int(id/(len(image[0][0])-(patch_size-1)))
    j = id % (len(image[0][0])-(patch_size-1))
    patch = image[:, i:(i+patch_size), j:(j+patch_size)]
    return patch


# Trnsfrom numpy array to tensor
def toTensor(pic):
    if isinstance(pic, np.ndarray):
        pic = pic.astype(float)
        img = torch.from_numpy(pic).float()
        return img


# Class of the dataset
class ImageDataset(Dataset):
    def __init__(self, image, patch_size, image_id, samples_list):
        self.patch_size = patch_size
        # I create pandas dataframe to be able to iterate through indices when loading patches
        self.sample_len = len(samples_list) # Nbr patches extracted from this image
        self.image_id = image_id            # Image ID
        self.tmp_df = pd.DataFrame(
            {'patch_idx': list(range(self.sample_len*self.image_id, self.sample_len*(self.image_id+1))), 'patch_id': (list(samples_list))})
        self.image = image
        self.X = self.tmp_df['patch_idx']   # Uniqie IDs for every patch for the whole dataset
        self.id = self.tmp_df['patch_id']   # Position of the central pixel of the patch

    def X(self):
        return self.X

    def __getitem__(self, index):
        # get patch for a pixel
        img = img_to_patches_to_tensor((self.X[index]-self.image_id*self.sample_len), self.id, self.image, self.patch_size)
        img_tensor = toTensor(img)
        return img_tensor, self.image_id, self.X[index]

    def __len__(self):
        return len(self.X.index)
