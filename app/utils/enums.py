import enum

class PerformanceTypes(str, enum.Enum):
    basic = "basic"
    fast = "fast"
    normal = "normal"
    precise = "precise"

class SearchTypes(str, enum.Enum):
    youtube = "youtube"
    web = "web"
