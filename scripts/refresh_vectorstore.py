from src.Sports import Sports


if __name__ == '__main__':
    for sport in Sports:
        print(f'Embedding {sport.value.league_name} rules to vectorstore...')
        sport.value.embed_document()