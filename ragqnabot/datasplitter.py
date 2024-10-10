from typing import List

class DocumentSplitter:
    """
    A class for splitting text data into smaller chunks with optional overlap and start index tracking.
    """

    def __init__(self, data: str, chunk_size: int = 1000, overlap: int = 200, add_start_index: bool = True):
        """
        Initialize the DocumentSplitter.

        Args:
            data (str): The text data to be split.
            chunk_size (int): The size of each chunk in characters. Default is 1000.
            overlap (int): The number of overlapping characters between chunks. Default is 200.
            add_start_index (bool): Whether to include the start index in the output chunks. Default is True.
        """
        self.data = data
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.add_start_index = add_start_index

    def split_data(self) -> List[str]:
        """
        Split the data into chunks with optional overlap. Optionally includes the start index in each chunk.

        Returns:
            List[Union[str, Dict[str, Union[str, int]]]]:
            A list of chunks, either as plain text strings or dictionaries containing the chunk text.
        """
        chunks = []
        data_length = len(self.data)
        start_index = 0

        while start_index < data_length:
            end_index = min(start_index + self.chunk_size, data_length)
            chunk = self.data[start_index:end_index]

            if self.add_start_index:
                chunks.append({
                    'text': chunk,
                    'start_index': start_index
                })
            else:
                chunks.append(chunk)

            start_index += self.chunk_size - self.overlap

        return chunks