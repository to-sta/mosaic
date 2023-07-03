from src.mosaic import generate_mosaic
import cv2 as cv

def main():
    generate_mosaic(
        base_img_path = 'resources/base_image/test_image_1.jpg'
        path_to_mosaic_image = 'resources/mosaic_images'
        desired_height = 40
        desired_width =  20
    )

if __name__ == "__main__":
    main()