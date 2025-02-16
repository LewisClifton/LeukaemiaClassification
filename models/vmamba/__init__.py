
import torch
import torch.nn as nn
import yaml

from .vmamba import VSSM as vmamba

SMALL_URL = "https://github.com/MzeroMiko/VMamba/releases/download/%23v2cls/vssm_small_0229_ckpt_epoch_222.pth"
BASE_UL = "https://github.com/MzeroMiko/VMamba/releases/download/%23v2cls/vssm_base_0229_ckpt_epoch_237.pth"
TINY_URL = "https://github.com/MzeroMiko/VMamba/releases/download/%23v2cls/vssm1_tiny_0230s_ckpt_epoch_264.pth"

def build_model(num_classes, vssm_config):
    return vmamba(
        depths=[2, 2, 8, 2], dims=96, drop_path_rate=0.2, 
        patch_size=4, in_chans=3, num_classes=1000, 
        ssm_d_state=1, ssm_ratio=1.0, ssm_dt_rank="auto", ssm_act_layer="silu",
        ssm_conv=3, ssm_conv_bias=False, ssm_drop_rate=0.0, 
        ssm_init="v0", forward_type="v05_noz", 
        mlp_ratio=4.0, mlp_act_layer="gelu", mlp_drop_rate=0.0, gmlp=False,
        patch_norm=True, norm_layer="ln2d", 
        downsample_version="v3", patchembed_version="v2", 
        use_checkpoint=False, posembed=False, imgsize=224, 
    )

    return vmamba(
        drop_path_rate = vssm_config["MODEL"]["DROP_PATH_RATE"],
        dims = vssm_config["MODEL"]["VSSM"]["EMBED_DIM"],
        depths = vssm_config["MODEL"]["VSSM"]["DEPTHS"],
        ssm_d_state = vssm_config["MODEL"]["VSSM"]["SSM_D_STATE"],
        ssm_dt_rank = vssm_config["MODEL"]["VSSM"]["SSM_DT_RANK"],
        ssm_ratio = vssm_config["MODEL"]["VSSM"]["SSM_RATIO"],
        ssm_conv = vssm_config["MODEL"]["VSSM"]["SSM_CONV"],
        ssm_conv_bias = vssm_config["MODEL"]["VSSM"]["SSM_CONV_BIAS"],
        forward_type = vssm_config["MODEL"]["VSSM"]["SSM_FORWARDTYPE"],
        mlp_ratio = vssm_config["MODEL"]["VSSM"]["MLP_RATIO"],
        downsample_version = vssm_config["MODEL"]["VSSM"]["DOWNSAMPLE"],
        pachembed_version = vssm_config["MODEL"]["VSSM"]["PATCHEMBED"],
        norm_layer = vssm_config["MODEL"]["VSSM"]["NORM_LAYER"],
    )
    

def get_vmamba(num_classes):

    config_path = 'models/vmamba/pretrained/vmambav2v_tiny_224.yaml'
    weights_url = TINY_URL # change if required

    # Build the model using the architecture specified
    with open(config_path, 'r') as yml:
        vssm_config = yaml.safe_load(yml)  
    model = build_model(num_classes, vssm_config)

    # Load the weights from the URL
    weights = torch.hub.load_state_dict_from_url(weights_url, model_dir='models/vmamba/pretrained/', file_name=weights_url.split('/')[-1])['model']
    model.load_state_dict(weights)

    # Edit final FC with correct number of classes
    model.head = nn.Linear(model.head.in_features, num_classes)

    return model