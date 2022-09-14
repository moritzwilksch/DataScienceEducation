#%%
import numpy as np
import matplotlib.pyplot as plt

#%%
x = np.arange(0, 6 * np.pi, 0.025)
y_true = np.sin(x)
y = y_true + np.random.normal(scale=1, size=len(x))

plt.scatter(x, y, color="k")
plt.plot(x, y_true, color="red")


#%%
np.random.seed(42)
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor

model = HistGradientBoostingRegressor(random_state=42, max_iter=20, max_leaf_nodes=64, min_samples_leaf=30)
model.fit(x.reshape(-1, 1), y)
preds = model.predict(x.reshape(-1, 1))

plt.scatter(x, y)
plt.plot(x, preds, color="red")

#%%

def gen_one_frame(use_fraction: float, left_to_right: bool):

    use_fraction = round(use_fraction, 3)

    print(use_fraction)

    if left_to_right:
        visible_idx = np.arange(0, len(preds) * use_fraction).astype("int")
    else:
        visible_idx = np.arange(len(preds) * use_fraction, len(preds)).astype("int")


    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(x, y, color="k", alpha=0.1)
    ax.plot(x[visible_idx], preds[visible_idx], color="blue")
    ax.set_title(f"frac = {use_fraction}")
    fig.savefig(
        f"ML-Basics/frames/{'ltr' if left_to_right else 'rtl'}_frame_{use_fraction}.png"
    )
    plt.close()


for f in np.arange(0.01, 1, 0.005):
    gen_one_frame(use_fraction=f, left_to_right=True)
for f in np.arange(0.01, 1, 0.005):
    gen_one_frame(use_fraction=f, left_to_right=False)



#%%
import glob
from PIL import Image

# filepaths
fp_in = "ML-Basics/frames/*.png"
fp_out = "ML-Basics/out_gif.gif"


imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
img = next(imgs)  # extract first image from iterator
img.save(fp=fp_out, format="GIF", append_images=imgs, save_all=True, duration=100, loop=0)
