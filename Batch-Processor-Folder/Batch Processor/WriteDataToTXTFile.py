def write_to_file(data, filename = "output.txt" ):
    """
    Writes the provided data to a local file.

    Args:
    - filename (str): The name of the file to write to.
    - data (str): The data to write to the file.
    """
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Example usage
if __name__ == "__main__":
    data = "This is the content to be written to the file."
    write_to_file(data)