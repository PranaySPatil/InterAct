"""
After moving all the files using the 1_ file, we run this one to extract
the images from the videos and also create a data file we can use
for training and testing later.
"""
import csv
import glob
import os
import os.path
from subprocess import call

def extract_files():
    """After we have all of our videos split between train and test, and
    all nested within folders representing their classes, we need to
    make a data file that we can reference when training our RNN(s).
    This will let us keep track of image sequences and other parts
    of the training process.

    We'll first need to extract images from each of the videos. We'll
    need to record the following data in the file:

    [train|test], class, filename, nb frames

    Extracting can be done with ffmpeg:
    `ffmpeg -i video.mpg image-%04d.jpg`
    """
    data_file = []
    folders = ['train', 'test']

    for folder in folders:
        class_folders = glob.glob(os.path.join(folder, '*'))

        for vid_class in class_folders:
            class_files = glob.glob(os.path.join(vid_class, '*.mp4'))
            # print (class_files)
            for video_path in class_files:
                # Get the parts of the file.
                print(video_path)
                video_parts = get_video_parts(video_path)

                train_or_test, classname, filename_no_ext, filename = video_parts

                # Only extract if we haven't done it yet. Otherwise, just get
                # the info.
                if not check_already_extracted(video_parts):
                    # Now extract it.
                    src = os.path.join(train_or_test, classname, filename)
                    dest = os.path.join(train_or_test, classname,
                        filename_no_ext + '-%04d.jpg')
                    call(["ffmpeg", "-i", src, "-vf", "mpdecimate,setpts=N/FRAME_RATE/TB", "-s", "700:700", dest])

                # Now get how many frames it is.
                nb_frames = get_nb_frames_for_video(video_parts)

                data_file.append([train_or_test, classname, filename_no_ext, nb_frames])

                print("Generated %d frames for %s" % (nb_frames, filename_no_ext))

    with open('data_file.csv', 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))

def extract_file():
    data_file = []

    print("getting input video file")
    video_parts = get_video_parts("demo.mp4")

    print("got video file")
    train_or_test, classname, filename_no_ext, filename = video_parts

    # Only extract if we haven't done it yet. Otherwise, just get
    # the info.
    # Now extract it.
    # src = os.path.join(filename)
    src = "C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\" + filename
    print("Source filename is")
    print(src)
    dest = os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                        filename_no_ext + '-%04d.jpg')
    call(["ffmpeg", "-i", src, "-vf", "mpdecimate,setpts=N/FRAME_RATE/TB", "-s", "500:500", dest])

    # Now get how many frames it is.
    nb_frames = get_nb_frames_for_video(video_parts)

    data_file.append([train_or_test, classname, filename_no_ext, nb_frames])

    print("Generated %d frames for %s" % (nb_frames, filename_no_ext))
    print(data_file)
    new_data_file = compare_images(data_file)
    print(new_data_file)

    with open('C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\data_file.csv', 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerows(new_data_file)

    print("Extracted and wrote %d video files." % (len(new_data_file)))

def get_nb_frames_for_video(video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    train_or_test, classname, filename_no_ext, _ = video_parts
    print("###########################")
    print(os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                                filename_no_ext + '*.jpg'))
    generated_files = glob.glob(os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                                filename_no_ext + '*.jpg'))
    print("generated files: ")
    print(len(generated_files))
    print("###########################")

    print("###########################")
    print(os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                     filename_no_ext + '*diff_*.jpg'))
    generated_diff_files = glob.glob(os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                     filename_no_ext + '*diff_*.jpg'))
    print("diff generated files: ")
    print(len(generated_diff_files))
    print("###########################")

    return len(generated_files)

def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split(os.path.sep)
    filename = video_path
    filename_no_ext = filename.split('.')[0]
    classname = "no_class"
    train_or_test = "test"

    return train_or_test, classname, filename_no_ext, filename

def check_already_extracted(video_parts):
    """Check to see if we created the -0001 frame of this file."""
    train_or_test, classname, filename_no_ext, _ = video_parts
    return bool(os.path.exists(os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                               filename_no_ext + '-0001.jpg')))

import PIL.Image as Image
import PIL.ImageChops as ImageChops

def compare_images(data_file):
    """
    Compares to images and saves a diff image, if there
    is a difference

    @param: path_one: The path to the first image
    @param: path_two: The path to the second image
    """
    new_data_file = []
    for [train_or_test, classname, filename_no_ext, number_of_frames] in data_file:
        image_one = None
        print("Number of frames")
        print(number_of_frames)
        print("Filename no ext")
        print(filename_no_ext)
        for i in range(1, number_of_frames - 1):
            if not image_one:
                previous = os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                                        filename_no_ext + ('-{:0>4d}.jpg'.format(i)))
                image_one = Image.open(previous)

            current = os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                                   filename_no_ext + ('-{:0>4d}.jpg'.format(i + 1)))
            image_two = Image.open(current)

            diff_save_location = os.path.join("C:\\Users\\pranpati\\Documents\\Projects\\ASL\\data\\test\\no_class\\",
                                              filename_no_ext + ('_diff_-{:0>4d}.jpg'.format(i)))

            diff = ImageChops.difference(image_one, image_two)
            #if diff.getbbox():
            diff.save(diff_save_location)

            image_one = image_two

        new_data_file.append([train_or_test, classname, filename_no_ext + '_diff_', number_of_frames - 1])

    return new_data_file

def main():
    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    extract_files()

if __name__ == '__main__':
    main()
