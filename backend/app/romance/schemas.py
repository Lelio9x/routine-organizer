from pydantic import BaseModel, ConfigDict, Field


class RomanceQuoteCreate(BaseModel):
    quote: str = Field(min_length=5)
    author: str = Field(min_length=2, max_length=120)
    book_title: str = Field(min_length=2, max_length=160)


class RomanceQuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quote: str
    author: str
    book_title: str