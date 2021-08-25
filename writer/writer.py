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


class ExcelPhoneWriter(ExcelWriter):
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
                if isinstance(value, list):
                    value = " ".join(value)
                worksheet.write(row, column, value)
                column += 1
            column = 0
            row += 1
        workbook.close()

    @staticmethod
    def __write_headers(worksheet):
        worksheet.write(0, 0, "Name")
        worksheet.write(0, 1, "Network Technology")
        worksheet.write(0, 2, "Announced")
        worksheet.write(0, 3, "Status")
        worksheet.write(0, 4, "Dimensions")
        worksheet.write(0, 5, "Weight")
        worksheet.write(0, 6, "Build")
        worksheet.write(0, 7, "Sim")
        worksheet.write(0, 8, "Type")
        worksheet.write(0, 9, "Size")
        worksheet.write(0, 10, "Resolution")
        worksheet.write(0, 11, "Protection")
        worksheet.write(0, 12, "OS")
        worksheet.write(0, 13, "Chipset")
        worksheet.write(0, 14, "CPU")
        worksheet.write(0, 15, "GPU")
        worksheet.write(0, 16, "Card Slot")
        worksheet.write(0, 17, "Internal Memory")
        worksheet.write(0, 18, "Main Camera Type")
        worksheet.write(0, 19, "Main Camera Details")
        worksheet.write(0, 20, "Main Camera Features")
        worksheet.write(0, 21, "Main Camera Video")
        worksheet.write(0, 22, "Selfie Camera Type")
        worksheet.write(0, 23, "Selfie Camera Details")
        worksheet.write(0, 24, "Selfie Camera Features")
        worksheet.write(0, 25, "Selfie Camera Video")
        worksheet.write(0, 26, "Loudspeaker")
        worksheet.write(0, 27, "3.5mm jack")
        worksheet.write(0, 28, "WLAN")
        worksheet.write(0, 29, "Bluetooth")
        worksheet.write(0, 30, "GPS")
        worksheet.write(0, 31, "NFC")
        worksheet.write(0, 32, "Radio")
        worksheet.write(0, 33, "USB")
        worksheet.write(0, 34, "Sensors")
        worksheet.write(0, 35, "Features Other")
        worksheet.write(0, 36, "Battery Type")
        worksheet.write(0, 37, "Charging")
        worksheet.write(0, 38, "Stand By")
        worksheet.write(0, 39, "Music Play")
        worksheet.write(0, 40, "Colors")
        worksheet.write(0, 41, "Models")
        worksheet.write(0, 42, "Price")
        worksheet.write(0, 43, "Image Url")
        return worksheet
