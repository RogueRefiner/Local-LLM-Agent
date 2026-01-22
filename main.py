from data.example.database.models import Base


def get_model_docs():
    docs = {}
    for model in Base.__subclasses__():
        docs[model.__name__] = (
            model.__doc__.strip() if model.__doc__ else "No description available."
        )
    return docs


def main():
    model_info = get_model_docs()
    for name, doc in model_info.items():
        print(f"Model: {name}\nDescription: {doc}\n\n")


if __name__ == "__main__":
    main()
