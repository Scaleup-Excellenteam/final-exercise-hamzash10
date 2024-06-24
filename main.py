import Presentation as presentation


def main():
    file_path = "Chapter_4.pptx"
    content = presentation.read_pptx(file_path)
    print(content)


if __name__ == '__main__':
    main()
