# 📖 Check Your Shelf 📖 - Python Bookshelf scanner 

Overview
Book Scanner is an application designed to scan and analyze images of bookshelves to identify books and determine their potential for resale. The application uses YOLO image sementation and then a multimodal image&text-to-text LLM to extract book titles and authors from images and compare them against a database to find matches.


<img src="https://github.com/NovaTrail/Check_Your_Shelf/blob/main/Book%20Vision.gif" alt="Alt text" width="380" height="390">

---
## Features
- Upload images of bookshelves in PNG, JPG, or JPEG formats.
- Segment the image into subimages representing different shelves.
- Analyze each subimage to identify books.
- Display the results in a table format, showing book titles, authors, and potential resale value.

Uses parallel processing to improve efficiency.
Please note the book resale database is not included. 

## License
This project is licensed under the MIT License. See the LICENSE file for details.

*This repository's contents are provided “as is”, without warranty or guarantee of any kind.* 

---

Acknowledgements
We would like to express our gratitude to the following Open Source Libraries
- Hugging Face Hub: For accessing pre-trained models and datasets.
- Streamlit: For providing an easy-to-use framework for building interactive web applications.
- RapidFuzz: For efficient fuzzy string matching.
