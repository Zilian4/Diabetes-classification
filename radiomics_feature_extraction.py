import os
import csv
import json
from radiomics import featureextractor
import argparse

def extract_features_from_folder(input_folder: str, mask_folder: str, output_csv: str):
    """
    Extracts radiomic features for all image files in the input folder and saves them to a CSV file.

    Parameters:
    - input_folder (str): Path to the folder containing image files.
    - mask_folder (str): Path to the folder containing mask files (corresponding to each image).
    - output_csv (str): Path where the CSV file will be saved.
    """
    
    # Initialize PyRadiomics feature extractor with default settings
    extractor = featureextractor.RadiomicsFeatureExtractor()

    # Open the CSV file for writing
    with open(output_csv, mode='w', newline='') as csv_file:
        writer = None
        
        # Loop through each file in the input folder
        for filename in os.listdir(input_folder):
            # Process only image files
            if filename.endswith(('.nii', '.nii.gz', '.mha', '.mhd', '.dcm')):
                image_path = os.path.join(input_folder, filename)
                mask_path = os.path.join(mask_folder, filename)  # Assuming mask names match image names

                # Ensure mask file exists
                if not os.path.isfile(mask_path):
                    print(f"Mask file not found for {filename}, skipping...")
                    continue
                
                # Extract features
                try:
                    features = extractor.execute(image_path, mask_path)
                except:
                    print(f"Extraction error{filename}")
                
                
                # Write headers and feature values to CSV
                if writer is None:
                    # Write the header
                    writer = csv.DictWriter(csv_file, fieldnames=['Image'] + list(features.keys()))
                    writer.writeheader()
                
                # Write the row for the current image
                writer.writerow({'Image': filename, **features})
                print(f"Extracted features for {filename}")
    print(f"Radiomics features saved to {output_csv}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract radiomic features from all images in a folder and save them to a CSV.")
    parser.add_argument('-i', '--input_folder', required=True, help="Folder containing image files.")
    parser.add_argument('-m', '--mask_folder', required=True, help="Folder containing mask files corresponding to images.")
    parser.add_argument('-o', '--output_csv', default='radiomics_features.csv', help="Output path for the CSV file (default: radiomics_features.csv).")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    extract_features_from_folder(input_folder=args.input_folder, mask_folder=args.mask_folder, output_csv=args.output_csv)
