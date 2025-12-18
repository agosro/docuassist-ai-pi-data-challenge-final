from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_by_sections(text: str) -> list[str]:
    sections = []
    current = []

    for line in text.splitlines():
        line_stripped = line.strip()

        is_heading = (
            3 < len(line_stripped) < 60 and
            not line_stripped.endswith(".") and
            len(line_stripped.split()) <= 6 and
            (
                line_stripped == line_stripped.title()
                or line_stripped.isupper()
            )
        )

        if is_heading and current:
            sections.append("\n".join(current))
            current = []

        current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections


_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)

def chunk_text(text: str) -> list[str]:
    sections = split_by_sections(text)
    chunks = []

    for section in sections:
        chunks.extend(_splitter.split_text(section))

    return chunks
