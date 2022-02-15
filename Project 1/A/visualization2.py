import numpy as np


def readCSV(filepath, delimiter=";"):
    title = filepath.split(".")[0]
    print(title)

    with open(filepath, 'r') as file:
        line = file.readline()

        headers = line.split(delimiter)
        for col in range(len(headers)):
            headers[col] = headers[col].strip()

        file.close()

    data = np.genfromtxt(filepath, skip_header=1, delimiter=delimiter, dtype=None)
    print(data[0])
    return title, headers

readCSV("student-mat.csv")

class CSV():
    filePath = None
    delimiter = None
    headers = None


    def __init__(self, filepath, delimiter):
        self.filePath = filepath
        self.delimiter = delimiter

    def __getHeaders(self):
        if self.filePath:
            with open(self.filePath, 'r') as file:
                line = file.readline()

                headers = line.split(self.delimiter)
                for col in range(len(headers)):
                    headers[col] = headers[col].strip()

                file.close()

            self.headers = headers

    def __getTitle(self):
        self.title = self.filePath.split(".")[0]

    def __get_data(self):
        self.data = np.genfromtxt(self.filePath, skip_header=1, delimiter=self.delimiter )



if __name__ == '__main__':
