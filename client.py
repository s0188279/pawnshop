import json
import re


class Client:

    def __init__(
        self,
        client_id: int,
        last_name: str,
        first_name: str,
        passport_series: str,
        passport_number: str,
        phone: str,
        patronymic: str | None = None,
        email: str | None = None,
    ):

        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.phone = phone
        self.email = email

    # валидация

    @staticmethod
    def _validate_regex(value: str, pattern: str, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Поле '{field_name}' должно быть строкой.")
        if not re.match(pattern, value):
            raise ValueError(f"Некорректный формат поля '{field_name}': {value}")

    @staticmethod
    def validate_id(client_id: int) -> None:
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом.")

    @staticmethod
    def validate_name(name: str, field_name: str = "ФИО") -> None:
        pattern = r"^[A-Za-zА-Яа-яЁё\-]+$"
        Client._validate_regex(name, pattern, field_name)

    @staticmethod
    def validate_phone(phone: str) -> None:
        pattern = r"^(\+7|8)\d{10}$"
        Client._validate_regex(phone, pattern, "Номер телефона")

    @staticmethod
    def validate_passport_series(series: str) -> None:
        Client._validate_regex(series, r"^\d{4}$", "Серия паспорта")

    @staticmethod
    def validate_passport_number(number: str) -> None:
        Client._validate_regex(number, r"^\d{6}$", "Номер паспорта")

    @staticmethod
    def validate_email(email: str | None) -> None:
        if email is not None:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            Client._validate_regex(email, pattern, "Email")

    # геттеры сеттеры

    @property
    def client_id(self) -> int:
        return self._client_id

    @client_id.setter
    def client_id(self, value: int) -> None:
        self.validate_id(value)
        self._client_id = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        self.validate_name(value, "Фамилия")
        self._last_name = value.capitalize()

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self.validate_name(value, "Имя")
        self._first_name = value.capitalize()

    @property
    def patronymic(self) -> str | None:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str | None) -> None:
        if value:
            self.validate_name(value, "Отчество")
            self._patronymic = value.capitalize()
        else:
            self._patronymic = None

    @property
    def passport_series(self) -> str:
        return self._passport_series

    @passport_series.setter
    def passport_series(self, value: str) -> None:
        self.validate_passport_series(value)
        self._passport_series = value

    @property
    def passport_number(self) -> str:
        return self._passport_number

    @passport_number.setter
    def passport_number(self, value: str) -> None:
        self.validate_passport_number(value)
        self._passport_number = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.validate_phone(value)
        self._phone = value

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        self.validate_email(value)
        self._email = value

    # альтернативные конструкторы

    @classmethod
    def from_dict(cls, data: dict) -> "Client":
        return cls(
            client_id=int(data["client_id"]),
            last_name=data["last_name"],
            first_name=data["first_name"],
            passport_series=str(data["passport_series"]),
            passport_number=str(data["passport_number"]),
            phone=str(data["phone"]),
            patronymic=data.get("patronymic"),
            email=data.get("email"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Client":
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_string(cls, str_data: str, sep: str = ";") -> "Client":
        parts = [p.strip() for p in str_data.split(sep)]
        if len(parts) < 7:
            raise ValueError("Недостаточно данных для создания Client.")
        return cls(
            client_id=int(parts[0]),
            last_name=parts[1],
            first_name=parts[2],
            patronymic=parts[3] if parts[3] and parts[3] != "None" else None,
            passport_series=parts[4],
            passport_number=parts[5],
            phone=parts[6],
            email=parts[7] if len(parts) > 7 and parts[7] and parts[7] != "None" else None,
        )



    def get_initials(self) -> str:
        patr = f" {self.patronymic[0]}." if self.patronymic else ""
        return f"{self.last_name} {self.first_name[0]}.{patr}"

    def to_short(self) -> "ClientShort":
        # cоздание краткой проекции из полной сущности
        return ClientShort(
            client_id=self.client_id,
            initials=self.get_initials(),
            phone=self.phone,
        )

    def __str__(self) -> str:
        return (
            f"Клиент #{self.client_id}: {self.last_name} {self.first_name} {self.patronymic or ''} | "
            f"Паспорт: {self.passport_series} {self.passport_number} | Тел: {self.phone}"
        ).strip()

    def __repr__(self) -> str:
        return (
            f"Client(id={self.client_id}, name='{self.get_initials()}', "
            f"passport='{self.passport_series} {self.passport_number}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Client):
            return False
        return (
            self.passport_series == other.passport_series
            and self.passport_number == other.passport_number
        )


class ClientShort:
    # краткая форма сущности

    def __init__(self, client_id: int, initials: str, phone: str):
        self._client_id = client_id
        self._initials = initials
        self._phone = phone

    @classmethod
    def from_client(cls, client: Client) -> "ClientShort":
        # альтернативное создание краткой формы из полной
        return cls(
            client_id=client.client_id,
            initials=client.get_initials(),
            phone=client.phone,
        )

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def initials(self) -> str:
        return self._initials

    @property
    def phone(self) -> str:
        return self._phone

    def __str__(self) -> str:
        return f"#{self.client_id} {self.initials} | {self.phone}"

    def __repr__(self) -> str:
        return f"ClientShort(id={self.client_id}, initials='{self.initials}', phone='{self.phone}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClientShort):
            return False
        return self.client_id == other.client_id and self.phone == other.phone
