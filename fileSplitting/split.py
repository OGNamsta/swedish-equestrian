import os

# Function to split URLs into separate files


def split_urls_into_files(input_file):
    # Create a directory to store the individual URL files
    output_directory = "url_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Open the input file containing URLs
    with open(input_file, 'r') as f:
        urls = f.readlines()

    # Determine the number of files needed
    num_urls = len(urls)
    num_files = num_urls // 100
    remainder = num_urls % 100

    # Write URLs to separate files (100 per file)
    for i in range(num_files):
        output_file = os.path.join(output_directory, f"urls_{i + 1}.txt")
        with open(output_file, 'w') as f_out:
            for url in urls[i * 100: (i + 1) * 100]:
                f_out.write(url.strip() + '\n')

    # Write remaining URLs to a separate file
    if remainder > 0:
        output_file = os.path.join(output_directory, f"urls_{num_files + 1}.txt")
        with open(output_file, 'w') as f_out:
            for url in urls[num_files * 100:]:
                f_out.write(url.strip() + '\n')


file_path = "organisation_ids_to_split"

# Call the function with the input file containing URLs
split_urls_into_files(f"{file_path}.txt")

