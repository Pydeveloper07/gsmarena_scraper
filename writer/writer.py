from abc import ABC, abstractmethod
import xlsxwriter


class ExcelWriter(ABC):
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.data = data

    @abstractmethod
    def write(self):
        pass


class ExcelBrandWriter(ExcelWriter):
    def __init__(self, file_name, data):
        super().__init__(file_name, data)

    def write(self):
        workbook = xlsxwriter.Workbook(f"files/{self.file_name}")
        worksheet = workbook.add_worksheet()
        worksheet = self.__write_headers(worksheet)
        row = 1
        column = 0
        for datum in self.data:
            for key, value in datum.items():
                worksheet.write(row, column, value)
                column += 1
            column = 0
            row += 1
        workbook.close()

    @staticmethod
    def __write_headers(worksheet):
        worksheet.write(0, 0, "Brand Name")
        worksheet.write(0, 1, "Number of Devices")
        worksheet.write(0, 2, "Url")
        return worksheet
