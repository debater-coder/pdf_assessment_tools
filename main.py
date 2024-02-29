from pypdf import PdfReader, PdfWriter
import click


def reorder(n):
    pages_order = []
    i = 0
    while i < n:
        pages_order.append(2 * n - i)
        pages_order.append(i + 1)
        pages_order.append(i + 2)
        pages_order.append(2 * n - i - 1)
        i += 2

    return [pages_order.index(i + 1) for i in range(2 * n)]


@click.command()
@click.option('--reverse', is_flag=True, help="Was it scanned in reverse order?")
@click.argument('input_filename', type=click.Path(exists=True))
@click.argument('output_filename')
def main(reverse, input_filename, output_filename):
    reader = PdfReader(input_filename)
    writer = PdfWriter()

    pages = reader.pages
    if reverse:
        pages = reader.pages[::-1]

    if len(reader.pages) % 2 != 0:
        raise Exception("Number of pages not even - Ensure you scan both sides of each side")

    indices = reorder(len(reader.pages))

    for index in indices:
        if index % 2 == 0:
            page = pages[int(index / 2)]

            page.mediabox.right /= 2
            writer.add_page(page)
            page.mediabox.right *= 2
        else:
            page = pages[int((index - 1) / 2)]
            page.mediabox.left = page.mediabox.right / 2
            writer.add_page(page)
            page.mediabox.left = 0

    with open(output_filename, "wb") as fp:
        writer.write(fp)


if __name__ == '__main__':
    main()
