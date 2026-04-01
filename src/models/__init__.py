import pandas as pd

# Bu sütunlar asla model feature'ı olmaz (CLAUDE.md EXCLUDE_COLS)
EXCLUDE_COLS = [
    "direction", "daily_return", "ticker",
    "open", "high", "low", "close", "date",
]


def get_feature_columns(df: pd.DataFrame) -> list:
    """
    EXCLUDE_COLS dışındaki tüm sütunları döndürür.
    Bunlar modele girecek feature sütunlarıdır.
    """
    return [col for col in df.columns if col not in EXCLUDE_COLS]
