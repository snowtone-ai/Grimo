"""Shared reference segmentation; source images are never modified.

The RGB plates have no ground-truth alpha. The neutral floor-shadow exclusion
is restricted to their lower support band; their masks remain provisional.
"""
import numpy as np
from PIL import Image, ImageDraw

def reference_mask(image):
    a=np.asarray(image.convert('RGBA'))
    if a[:,:,3].min()<255:
        return a[:,:,3]>127
    rgb=a[:,:,:3].astype(int)
    low=rgb.min(2);chroma=rgb.max(2)-low
    background=(low>=249)&(chroma<5)
    # Below the fleece: retain chromatic cocoa hooves, remove neutral floor.
    background[1030:,:]|=(low[1030:,:]>120)&(chroma[1030:,:]<35)
    barrier=Image.fromarray(np.where(background,0,255).astype('uint8'))
    # A padded flood-fill handles all border-connected white background once.
    padded=Image.new('L',(barrier.width+2,barrier.height+2),0)
    padded.paste(barrier,(1,1));ImageDraw.floodfill(padded,(0,0),128)
    return np.asarray(padded)[1:-1,1:-1]!=128
