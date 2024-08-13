import pandas as pd

def wrap_urls_in_excel(input_file_path, output_file_path):
    try:
        # Read Excel file
        df = pd.read_excel(input_file_path, header=None)  # Assuming URLs are in the first column without a header

        # Wrap URLs with quotes and commas
        df[0] = df[0].apply(lambda url: f"'{url}',")

        # Write to a new Excel file
        df.to_excel(output_file_path, index=False, header=False)

        print(f"URLs have been processed and saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = ''  # Replace with the path to your input Excel file
output_file = ''  # Replace with the desired output Excel file path

wrap_urls_in_excel(input_file, output_file)
