import os


class DatasetCatalog(object):
    DATASETS = {
        "custom_dataset_train": {
            "images_dir": "core/data/datasets/Agriculture-Vision-2021/train/images/rgb",
            "masks_dir": "core/data/datasets/Agriculture-Vision-2021/train/labels/weed_cluster",
            "classes": ['background', 'foreground'],
            "split": "train",
        },
        "custom_dataset_val": {
            "images_dir": "/path/to/custom_dataset/val/img",
            "masks_dir": "/path/to/custom_dataset/val/mask",
            "classes": ['background', 'foreground'],
            "split": "val",
        },
        "custom_dataset_test": {
            "images_dir": "core/data/datasets/Agriculture-Vision-2021/val/images/rgb",
            "masks_dir": "core/data/datasets/Agriculture-Vision-2021/val/labels/weed_cluster",
            "classes": ['background', 'foreground'],
            "split": "test",
        },
    }

    @staticmethod
    def get(name):
        if 'custom_dataset' in name:
            attrs = DatasetCatalog.DATASETS[name]
            return dict(
                factory="CustomDataset",
                args=attrs,
            )
        raise RuntimeError("Dataset not available: {}".format(name))
