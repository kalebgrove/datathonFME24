import pandas as pd
from fastai.tabular.all import *
from fastai.vision.all import *
 
# Load the datasets
product_data = pd.read_csv("./product_data.csv")  # Replace with actual file path
attribute_data = pd.read_csv("./attribute_data.csv")  # Replace with actual file path

# Merge datasets
data = pd.merge(product_data, attribute_data, on="cod_modelo_color", how="left")

# Extract image filename information
data['image_file'] = data['image_name']  # Assuming the column with filenames is `image_name`

# Handle missing attributes by setting them to INVALID
data['des_value'].fillna("INVALID", inplace=True)

# Create test_id column
data['test_id'] = data['cod_modelo_color'] + "_" + data['attribute_name']

# Encode categorical variables and target
cat_names = ['cod_modelo_color', 'attribute_name', 'category', 'sub_category']
cont_names = []  # Add continuous variables here if any exist

# Preprocessing steps
procs = [Categorify, FillMissing, Normalize]

# Encode target values
des_values = data['des_value'].unique()
des_value_mapping = {value: idx for idx, value in enumerate(des_values)}
data['des_value_idx'] = data['des_value'].map(des_value_mapping)

# Split the data into train and validation sets
train_df, valid_df = train_test_split(data, test_size=0.2, stratify=data['des_value'])

# Prepare the image paths
train_df['image_path'] = "path/to/images/" + train_df['image_file']  # Replace with actual image directory
valid_df['image_path'] = "path/to/images/" + valid_df['image_file']

# Define DataBlock for mixed tabular and image data
def get_x(row):
    return row['image_path'], row[cat_names + cont_names]

def get_y(row):
    return row['des_value_idx']

dblock = DataBlock(
    blocks=(ImageBlock, TabularBlock(cat_names=cat_names, cont_names=cont_names, procs=procs), CategoryBlock),
    get_x=get_x,
    get_y=get_y,
    splitter=RandomSplitter(seed=42),
    item_tfms=Resize(224),  # Resize images for CNN
    batch_tfms=aug_transforms()
)

# Create DataLoaders
dls = dblock.dataloaders(train_df, bs=64)

# Define and train the model
learn = cnn_learner(
    dls, resnet34, metrics=accuracy
)

# Fine-tune the model
learn.fine_tune(5)

# Predictions for the validation set
test_dl = dls.test_dl(valid_df)
preds, _ = learn.get_preds(dl=test_dl)
predicted_labels = [des_values[int(pred.argmax())] for pred in preds]

# Prepare the submission file
valid_df['predicted_des_value'] = predicted_labels
submission = valid_df[['test_id', 'predicted_des_value']]
submission.columns = ['test_id', 'des_value']

# Save submission
submission.to_csv("submission.csv", index=False)