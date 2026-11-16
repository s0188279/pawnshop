import json
import re

class Client:
    # Умный конструктор для разных типов данных
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            raw = args[0]
            if isinstance(raw, dict):
                self._init_from_dict(raw)
                return
            if isinstance(raw, str):
                raw = raw.strip()
                if raw.startswith("{"):
                    self._init_from_dict(json.loads(raw))
                else:
                    self._init_from_string(raw)
                return
            raise TypeError("Неизвестный формат данных")
        self._init_standard(*args, **kwargs)

    # Стандартная инициализация
    def _init_standard(self, client_id: int, last_name: str, first_name: str, passport_series: str, passport_number: str, phone: str, patronymic: str | None = None, email: str | None = None):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.phone = phone
        self.email = email

    # Распаковка из словаря
    def _init_from_dict(self, data: dict):
        self._init_standard(
            client_id=int(data["client_id"]),
            last_name=data["last_name"],
            first_name=data["first_name"],
            passport_series=str(data["passport_series"]),
            passport_number=str(data["passport_number"]),
            phone=str(data["phone"]),
            patronymic=data.get("patronymic"),
            email=data.get("email"),
        )

    # Парсинг строки с разделителями
    def _init_from_string(self, str_data: str, sep: str = ";"):
        p = [x.strip() for x in str_data.split(sep)]
        self._init_standard(
            client_id=int(p[0]),
            last_name=p[1],
            first_name=p[2],
            patronymic=p[3] if p[3] and p[3] != "None" else None,
            passport_series=p[4],
            passport_number=p[5],
            phone=p[6],
            email=p[7] if len(p) > 7 and p[7] and p[7] != "None" else None,
        )

    @staticmethod
    def _validate_regex(value: str, pattern: str, field_name: str):
        if not isinstance(value, str) or not re.match(pattern, value):
            raise ValueError(f"Косяк в поле {field_name}: {value}")

    @staticmethod
    def validate_id(client_id: int):
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("ID должен быть числом > 0")

    @staticmethod
    def validate_name(name: str, field_name: str = "ФИО"):
        Client._validate_regex(name, r"^[A-Za-zА-Яа-яЁё\-]+$", field_name)

    @staticmethod
    def validate_phone(phone: str):
        Client._validate_regex(phone, r"^(\+7|8)\d{10}$", "Номер телефона")

    @staticmethod
    def validate_passport_series(series: str):
        Client._validate_regex(series, r"^\d{4}$", "Серия паспорта")

    @staticmethod
    def validate_passport_number(number: str):
        Client._validate_regex(number, r"^\d{6}$", "Номер паспорта")

    @staticmethod
    def validate_email(email: str | None):
        if email:
            Client._validate_regex(email, r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "Email")

    @property
    def client_id(self) -> int:
        return self._client_id

    @client_id.setter
    def client_id(self, value: int):
        self.validate_id(value)
        self._client_id = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self.validate_name(value, "Фамилия")
        self._last_name = value.capitalize()

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self.validate_name(value, "Имя")
        self._first_name = value.capitalize()

    @property
    def patronymic(self) -> str | None:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str | None):
        if value:
            self.validate_name(value, "Отчество")
            self._patronymic = value.capitalize()
        else:
            self._patronymic = None

    @property
    def passport_series(self) -> str:
        return self._passport_series

    @passport_series.setter
    def passport_series(self, value: str):
        self.validate_passport_series(value)
        self._passport_series = value

    @property
    def passport_number(self) -> str:
        return self._passport_number

    @passport_number.setter
    def passport_number(self, value: str):
        self.validate_passport_number(value)
        self._passport_number = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self.validate_phone(value)
        self._phone = value

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None):
        self.validate_email(value)
        self._email = value

    def get_initials(self) -> str:
        patr = f" {self.patronymic[0]}." if self.patronymic else ""
        return f"{self.last_name} {self.first_name[0]}.{patr}"

    def __str__(self) -> str:
        return f"Клиент #{self.client_id}: {self.last_name} {self.first_name} | Паспорт: {self.passport_series} {self.passport_number} | Тел: {self.phone}"

    def __repr__(self) -> str:
        return f"Client(id={self.client_id}, name='{self.get_initials()}', passport='{self.passport_series} {self.passport_number}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Client):
            return False
        return self.passport_series == other.passport_series and self.passport_number == other.passport_number


class ClientShort:
    def __init__(self, client_id: int, initials: str, phone: str):
        self._client_id = client_id
        self._initials = initials
        self._phone = phone

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


class ClientMapper:
    # Преобразует полного клиента в шорт-версию
    @staticmethod
    def to_short(client: Client) -> ClientShort:
        return ClientShort(
            client_id=client.client_id,
            initials=client.get_initials(),
            phone=client.phone,
        )
