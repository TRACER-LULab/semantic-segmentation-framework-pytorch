from __future__ import division
from segmentation_models_pytorch.utils.train import ValidEpoch
from segmentation_models_pytorch.utils.metrics import Fscore
from segmentation_models_pytorch.utils.losses import DiceLoss
import torch
import numpy as np
import segmentation_models_pytorch as smp
from PIL import Image


def do_custom_dataset_prediction(
    model, data_loader, device, output_folder, logger, dataset_name, **kwargs
):
    metrics = [
        Fscore(threshold=0.5, ignore_channels=(0,)),  # Ignore background channel
    ]
    test_epoch = ValidEpoch(
        model=model, metrics=metrics, device=device, loss=DiceLoss()
    )
    for item in test_epoch.run(data_loader):
        if (
            "predictions" in item.keys()
            and "filenames" in item.keys()
            and "ground_truth" in item.keys()
        ):
            for prediction, ground_truth, file_name in zip(
                item["predictions"], item["ground_truth"], item["filenames"]
            ):
                prediction_mask = np.argmax(prediction, axis=0)
                ground_truth_mask = np.argmax(ground_truth, axis=0)
                out_img = Image.fromarray(prediction_mask.astype("uint8"))
                # out_img.putpalette(custom_palette)
                # You can save prediction_mask to your specified path.
        else:
            test_logs = item
            str_logs = ["{} - {:.4}".format(k, v) for k, v in test_logs.items()]
            meters = "\t".join(str_logs)
            logger.info(
                "\t".join(["Test:", "{meters}", "max mem: {memory:.0f}",]).format(
                    meters=meters,
                    memory=torch.cuda.max_memory_allocated() / 1024.0 / 1024.0,
                )
            )
