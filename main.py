import os
import filecmp
from jinja2 import Environment, FileSystemLoader, select_autoescape

def compare_files(path1, path2):
    return filecmp.cmp(path1, path2)

def should_compare(author1, author2, matrix_opmerkingen):
    return author1 != author2 and not matrix_opmerkingen[author2][author1]

def build_matrix(directory):
    authors = sorted(os.listdir(directory))
    matrix_opmerkingen = {author: {other_author: [] for other_author in authors} for author in authors}

    for i, author1 in enumerate(authors):
        for j, author2 in enumerate(authors):
            if should_compare(author1, author2, matrix_opmerkingen):
                file1 = os.path.join(directory, author1, os.listdir(os.path.join(directory, author1))[0])
                file2 = os.path.join(directory, author2, os.listdir(os.path.join(directory, author2))[0])

                if os.path.basename(file1) == os.path.basename(file2) and compare_files(file1, file2):
                    matrix_opmerkingen[author1][author2].append("identieke file en naam " + os.path.basename(file1))
                elif os.path.basename(file1) == os.path.basename(file2):
                    matrix_opmerkingen[author1][author2].append("identieke naam " + os.path.basename(file1))
                elif compare_files(file1, file2):
                    matrix_opmerkingen[author1][author2].append("identieke file " + os.path.basename(file1))

    return authors, matrix_opmerkingen

def generate_html_output(authors, matrix_opmerkingen, output_filename):
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )

    template = env.get_template("outputtemplate.html")
    output_html = template.render(authors=authors, matrix_opmerkingen=matrix_opmerkingen)

    output_filepath = f"{output_filename}.html"
    with open(output_filepath, "w") as output_file:
        output_file.write(output_html)

    print(f"HTML file generated: {output_filepath}")

def main():
    directory_path = input("Enter the path to the analysis directory: ")
    output_filename = input("Enter the desired filename for the HTML output (without extension): ")

    authors, matrix_opmerkingen = build_matrix(directory_path)
    generate_html_output(authors, matrix_opmerkingen, output_filename)

if __name__ == "__main__":
    main()
