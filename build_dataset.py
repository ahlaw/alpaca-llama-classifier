import argparse
import random
import os
import shutil


SIZE = 250

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data_dir', required=True,
        help="Directory with original dataset")
parser.add_argument('-o', '--output_dir', required=True,
        help="Where to write new data")


def copy_files(fnames, data_dir, output_dir):
    """Copies files listed in `fnames` from `data_dir` to `output_dir`"""
    for fname in fnames:
        src = os.path.join(data_dir, fname)
        dest = os.path.join(output_dir, fname)
        shutil.copyfile(src, dest)


if __name__ == '__main__':
    args = vars(parser.parse_args())

    train_dir = os.path.join(args['output_dir'], 'train')
    validation_dir = os.path.join(args['output_dir'], 'validation')
    test_dir = os.path.join(args['output_dir'], 'test')

    if not os.path.exists(args['output_dir']):
        os.mkdir(args['output_dir'])
    else:
        print("Warning: output dir {} already exists".format(
            args['output_dir']))
    os.mkdir(train_dir)
    os.mkdir(validation_dir)
    os.mkdir(test_dir)

    random.seed(42)
    animals = ['alpaca', 'llama']

    for animal in animals:
        orig_dataset_dir = os.path.join(args['data_dir'], animal)
        fnames = os.listdir(orig_dataset_dir)

        fnames.sort()
        random.shuffle(fnames)
        split_1 = int(0.6 * len(fnames))
        split_2 = int(0.8 * len(fnames))

        train_fnames = fnames[:split_1]
        validation_fnames = fnames[split_1:split_2]
        test_fnames = fnames[split_2:]

        class_train_dir = os.path.join(train_dir, animal)
        class_validation_dir = os.path.join(validation_dir, animal)
        class_test_dir = os.path.join(test_dir, animal)

        os.mkdir(class_train_dir)
        os.mkdir(class_validation_dir)
        os.mkdir(class_test_dir)

        copy_files(train_fnames, orig_dataset_dir, class_train_dir)
        copy_files(validation_fnames, orig_dataset_dir, class_validation_dir)
        copy_files(test_fnames, orig_dataset_dir, class_test_dir)

        print('total training {} images: {}'.format(animal,
            len(os.listdir(class_train_dir))))
        print('total validation {} images: {}'.format(animal, 
            len(os.listdir(class_validation_dir))))
        print('total test {} images: {}'.format(animal, 
            len(os.listdir(class_test_dir))))
