from pypdf import PdfReader, PdfWriter

reader = PdfReader("example.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.mediabox.right /= 2
    writer.add_page(page)

    page.mediabox.right *= 2
    page.mediabox.left = page.mediabox.right / 2
    writer.add_page(page)

with open("result.pdf", "wb") as fp:
    writer.write(fp)
