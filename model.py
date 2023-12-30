from fastai.vision.all import *

def main(modelpath: str, image_path: str, print_pred: bool = True) -> (str, float):
    # Load the trained model
    path_to_pkl = modelpath
    learn = load_learner(path_to_pkl)

    # Load the image and predict
    image_path = image_path
    img = PILImage.create(image_path)
    pred, pred_idx, probs = learn.predict(img)

    # Print out the prediction and probability
    if print_pred:
        print(f'Prediction: {pred}')
        print(f'Probability: {probs[pred_idx]:.04f}')
    
    return pred, probs[pred_idx]

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])