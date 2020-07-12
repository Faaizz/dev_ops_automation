# MISCALLANEOUS FUNCTIONS

#==============================================================================
# IMPORTS
import requests, string, os, tarfile, shutil


#==============================================================================
def create_temp_dir(dir_path):
    try:
        os.mkdir(dir_path)

    except FileExistsError:
        print("Temporary directory at '{0}' already exists\n"
                        .format(dir_path)
                        )


#==============================================================================
def download_package(file_path, url):
    """
    Download package at specified 'url' and stream content into 
    the specified 'file'
    @param url: URL of the package to download
    @param file: File resource open for writing in binary mode

    @return None
    @throws 
    """

    # Check if file already exists
    if(not os.path.exists(file_path)):
        # If not, fetch the file online
        with open(file_path, mode="wb") as temp_file:
            # Log
            print("Downloading package from {0} to {1}...\n"
                        .format(url, file_path)
                        )
            # Download package
            try:
                # Make GET request
                res= requests.get(url, stream=True)

                # Stream data into file
                for chunk in res.iter_content(chunk_size=256):
                    temp_file.write(chunk)

            except requests.exceptions.RequestException as ex:
                print("Error Fetching Package at '{0}'...\nAborting...\n"
                                .format(url)
                )
                quit()

    else:
        print("Package already exists... \nSkipping download...\n")

    

#==============================================================================
def extract_downloaded_file(file_path, dst_path):
    """
    Extract downloaded file
    """
    with tarfile.open(file_path) as tar_file:
        try:
            # Create inner temp directory if it doesn't already exist
            if( not os.path.exists(dst_path)):
                os.mkdir(dst_path)

            # Log
            print("Extracting package {0} to {1}...\n"
                        .format(file_path, dst_path)
                        )
            # Extract files
            tar_file.extractall(path=dst_path)

        except tarfile.TarError as ex:
            print("An Error occured while extracting the package...\n")
            raise ex


#==============================================================================
def copy_files(src_dir, dst_dir):
    """
    Recursively copy rxtracted files
    """
    # Recursively copy the content of src_dir to dest_dir
    try:
        # Log
        print("Copying files from {0} to {1}...\n"
                    .format(src_dir, dst_dir)
                    )
        # Copy operation
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

    except (FileExistsError, shutil.Error) as err:
        print("An error occured during copy operation from {0} to {1}...\n"
                        .format(src_dir, dst_dir)
        )
        raise err


#==============================================================================
def cleanup(temp_path):
    """
    Delete temp directory and its contents
    """
    try:
         # Log
        print("Deleting files from {0}...\n"
                    .format(temp_path)
                    )

        # Delete operation
        shutil.rmtree(os.path.abspath(temp_path))

    except shutil.Error as err:
        print("An error occured during cleanup")
        raise err
    

#==============================================================================
def populate_template(src_path, dst_path, replacements):
    """
    Populate pre-existing templates which follow string.Template 
    placeholder style
    @param src_path: Path to template file
    @param dst_path: Path to new file with replacements made
    @params replacements: Dictionary of identifiers and replacements

    @return None
    """

    try:
        # Open existing template file
        with open(src_path, "r") as t_fp:

            # Read entire file as text
            lines= t_fp.read()
            # Perform template substitution
            new_lines= string.Template(lines).substitute(replacements)

            # Write new text to destination file
            with open(dst_path, "w") as d_fp:
                d_fp.write(new_lines)

    except FileNotFoundError as err:
        raise err


#==============================================================================
def populate_mysql_template(src_path, dst_path, db_name, db_user, db_pass):
    """
    Calls populate_template() with a dictionary as follow:
    {
        "db_name": @param db_name,
        "db_user": @param db_user,
        "db_pass": @param db_pass
    }
    """

    # Setup replacements
    reps= {
        "db_name": db_name,
        "db_user": db_user,
        "db_pass": db_pass
    }

    # Populate template
    populate_template(src_path, dst_path, reps)
