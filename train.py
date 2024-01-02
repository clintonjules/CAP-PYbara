from fastai.vision.all import *

def main(filepath: str, modelpath: str, show_results:bool = False):
    # Define the path to your images
    path = Path(filepath)

    # Load your data
    dls = ImageDataLoaders.from_folder(path, train='.', valid_pct=0.2, item_tfms=Resize(224))

    # Create a learner
    learn = vision_learner(dls, resnet34, metrics=error_rate)

    # Train the model
    learn.fine_tune(4)

    # Evaluate and Export
    if show_results:
        learn.show_results()
        plt.show()
        
    learn.export(modelpath)
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])