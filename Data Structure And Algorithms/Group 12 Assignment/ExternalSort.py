# importing dependencies
import os
import random
import sys

class Heapnode:
    def __init__(self, item, file_handler):
        self.item = item
        self.file_handler = file_handler

class ExternalSort:
    def __init__(self):
        self.sorted_chunk_index = 1
        self.chunk_file_directory = self.CreateChunkFileDirectory()

    def CreateFileWithRandomNumbers(self, file_name, file_size):
        
        file_handler = open(file_name, 'wt')
        
        for i in range(file_size):
            file_handler.write(str(random.randint(0, 1000)) + "\n")

        file_handler.close()

        return "File Created Sucessfully."

    def BreakFileToChunks(self, file_name, chunk_size):

        file_handler = open(file_name, 'rt')
        line_number = 1
        chunk = []

        while file_handler:
            line = file_handler.readline().strip()
            
            if line == "":
                file_handler.close()
                return "Broken Files To Chunks."
            else:
                chunk.append(int(line.strip()))
                if line_number % chunk_size == 0:
                    self.CreateChunkFile(file_handler, chunk)
                    chunk = []
                line_number += 1

    def CreateChunkFile(self, file_handler, chunk):
        sorted_chunk = self.Sort(chunk)
        chunk_file_name = 'sorted_chunk_' + str(self.sorted_chunk_index) + '.txt'
        chunk_file_path = os.path.join(self.chunk_file_directory, chunk_file_name)
        chunk_file_handler = open(chunk_file_path, 'wt')

        for i in sorted_chunk:
            chunk_file_handler.write(str(i) + "\n")

        self.sorted_chunk_index += 1

        return chunk_file_name + "created."

    def Sort(self, chunk):
        return sorted(chunk)

    def Heapify(self, arr, i, n):

        left = int(2 * i) + 1
        right = int(2 * i) + 2
        i = int(i)
        
        if left < n and arr[left].item < arr[i].item:
            smallest = left
        else:
            smallest = i

        if right < n and arr[right].item < arr[smallest].item:
            smallest = right

        if i != smallest:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            self.Heapify(arr, smallest, n)

    def ConstructHeap(self, arr):
        l = len(arr) - 1
        mid = l / 2

        while mid >= 0:
            self.Heapify(arr, mid, l)
            mid -= 1

    def KWayMergesort(self, file_name):
        heap_list = []
        self.current_working_directory = os.getcwd()
        sorted_file_handler = open(file_name, 'at')

        for chunk_file_handler in self.GetChunkFileHandelers():
            item = chunk_file_handler.readline().strip()
            
            if item == "":
                item = sys.maxsize
            else:
                item = int(item)
            heap_list.append(Heapnode(item, chunk_file_handler))

        self.ConstructHeap(heap_list)
        index = 1

        while True:
            minimum = heap_list[0]

            if minimum.item == sys.maxsize:
                break

            sorted_file_handler.write(str(minimum.item) + "\n")
            file_handler = minimum.file_handler
            item = file_handler.readline().strip()

            if item == "":
                item = sys.maxsize
            else:
                item = int(item)

            heap_list[0] = Heapnode(item, file_handler)
            self.Heapify(heap_list, 0, len(heap_list))

        sorted_file_handler.close()

        return "Completed K way merge sorting of chunk files"

    def CreateChunkFileDirectory(self):
        current_working_directory = os.getcwd()
        chunk_file_directory = 'chunk_files'
        chunk_files_path = os.path.join(current_working_directory, chunk_file_directory)
        os.mkdir(chunk_files_path)

        return chunk_files_path

    def GetChunkFileHandelers(self):
        chunk_files = os.listdir(self.chunk_file_directory)
        chunk_file_paths = [os.path.join(self.chunk_file_directory, chunk_file) for chunk_file in chunk_files]
        chunk_file_handelers = [open(chunk_file, 'rt') for chunk_file in chunk_file_paths]

        return chunk_file_handelers

# variables
file_name = os.path.join(os.getcwd(), 'sample.txt')
file_size = 10**9
chunk_size = 100000

externalsort = ExternalSort()
externalsort.CreateFileWithRandomNumbers(file_name, file_size)
externalsort.BreakFileToChunks(file_name, chunk_size)
externalsort.KWayMergesort('sorted_file.txt')



    


