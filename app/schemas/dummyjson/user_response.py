from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Hair(BaseModel):
    color: str
    type: str

class Coordinates(BaseModel):
    lat: float
    lng: float

class Address(BaseModel):
    address: str
    city: str
    state: str
    stateCode: str
    postalCode: str
    country: str
    coordinates: Coordinates

class Company(BaseModel):
    department: str
    name: str
    title: str
    address: Address

class Bank(BaseModel):
    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str

class Crypto(BaseModel):
    coin: str
    wallet: str
    network: str

class DummyUserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    maidenName: Optional[str] = Field(None, description="Lead maiden name")
    age: Optional[int] = Field(None, description="Lead age")
    gender: Optional[str] = Field(None, description="Lead gender")
    email: Optional[EmailStr] = Field(None, description="Lead email")
    phone: Optional[str] = Field(None, description="Lead phone")
    username: Optional[str] = Field(None, description="Lead username")
    password: Optional[str] = Field(None, description="Lead password")
    birthDate: Optional[str] = Field(None, description="Lead birth date")
    image: Optional[str] = Field(None, description="Lead image")
    bloodGroup: Optional[str] = Field(None, description="Lead blood group")
    height: Optional[float] = Field(None, description="Lead height")
    weight: Optional[float] = Field(None, description="Lead weight")
    eyeColor: Optional[str] = Field(None, description="Lead eye color")
    hair: Optional[Hair] = Field(None, description="Lead hair")
    ip: Optional[str] = Field(None, description="Lead IP address")
    address: Optional[Address] = Field(None, description="Lead address")
    macAddress: Optional[str] = Field(None, description="Lead MAC address")
    university: Optional[str] = Field(None, description="Lead university")
    bank: Optional[Bank] = Field(None, description="Lead bank")
    company: Optional[Company] = Field(None, description="Lead company")
    ein: Optional[str] = Field(None, description="Lead EIN")
    ssn: Optional[str] = Field(None, description="Lead SSN")
    userAgent: Optional[str] = Field(None, description="Lead user agent")
    crypto: Optional[Crypto] = Field(None, description="Lead crypto")
    role: Optional[str] = Field(None, description="Lead role")
    
class DummyUserSearchResponse(BaseModel):
    users: list[DummyUserResponse]
    total: int
    skip: int
    size: int