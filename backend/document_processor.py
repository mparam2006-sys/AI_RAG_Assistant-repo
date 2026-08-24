import os

import pymupdf

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============================================================
# Extract Text
# ============================================================

def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()


    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    if extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    elif extension == ".pdf":

        document = pymupdf.open(
            file_path
        )


        pages = []


        for page in document:

            pages.append(
                page.get_text()
            )


        document.close()


        return "\n".join(
            pages
        )


    return ""


# ============================================================
# Split Text
# ============================================================

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )


    chunks = splitter.split_text(
        text
    )


    return chunks