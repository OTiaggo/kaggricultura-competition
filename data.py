"""Dados estáticos e funções de consulta para o ambiente Kaggriculture.

Os identificadores seguem exatamente o formato usado nas observações e ações do
ambiente (por exemplo, ``WHEAT`` e ``BUY_SEED``).  Os dicionários são pensados
para apoiar agentes, análises e estratégias sem depender do simulador.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final


# Produtos vegetais que podem ser plantados.  ``max_yield`` é o máximo por
# colheita/planta; nos cultivos contínuos, ``scheduled_yields`` limita o total
# de ciclos de produção.
CROPS: Final[dict[str, dict[str, Any]]] = {
    "WHEAT": {
        "yield_type": "one_time",
        "seed_cost": 10,
        "base_market_price": 25,
        "first_yield_day": 2,
        "max_yield_day": 4,
        "scheduled_yield_interval_days": None,
        "scheduled_yields": 1,
        "max_yield": 6,
        "max_yield_without_fertilizer": 4,
        "action_cost": 1,
        "yield_per_tile_per_day": 0.80,
    },
    "CARROT": {
        "yield_type": "one_time",
        "seed_cost": 20,
        "base_market_price": 35,
        "first_yield_day": 2,
        "max_yield_day": 3,
        "scheduled_yield_interval_days": None,
        "scheduled_yields": 1,
        "max_yield": 4,
        "max_yield_without_fertilizer": 3,
        "action_cost": 1,
        "yield_per_tile_per_day": 0.75,
    },
    "TOMATO": {
        "yield_type": "ongoing",
        "seed_cost": 50,
        "base_market_price": 60,
        "first_yield_day": 8,
        "max_yield_day": 11,
        "scheduled_yield_interval_days": 1,
        "scheduled_yields": 4,
        "max_yield": 4,
        "action_cost": 1,
        "yield_per_tile_per_day": 0.33,
    },
    "STRAWBERRY": {
        "yield_type": "ongoing",
        "seed_cost": 100,
        "base_market_price": 120,
        "first_yield_day": 10,
        "max_yield_day": 16,
        "scheduled_yield_interval_days": 2,
        "scheduled_yields": 4,
        "max_yield": 4,
        "action_cost": 1,
        "yield_per_tile_per_day": 0.24,
    },
    "MELON": {
        "yield_type": "one_time",
        "seed_cost": 80,
        "base_market_price": 250,
        "first_yield_day": 10,
        "max_yield_day": 10,
        "scheduled_yield_interval_days": None,
        "scheduled_yields": 1,
        "max_yield": 6,
        "action_cost": 1,
        "yield_per_tile_per_day": 0.55,
    },
}


# Animais compráveis e sua produção. ``max_held`` é o limite de produto ainda
# não coletado no respectivo tile, e não uma produção máxima vitalícia.
ANIMALS: Final[dict[str, dict[str, Any]]] = {
    "GOOSE": {
        "product": "EGG",
        "purchase_cost": 300,
        "base_market_price": 50,
        "first_yield_day": 4,
        "yield_interval_days": 1,
        "max_held": 4,
        "structure": "COOP",
        "build_action_cost": 1,
        "yield_per_tile_per_day": 1.00,
    },
    "COW": {
        "product": "MILK",
        "purchase_cost": 400,
        "base_market_price": 160,
        "first_yield_day": 8,
        "yield_interval_days": 2,
        "max_held": 6,
        "structure": "PASTURE",
        "build_action_cost": 1,
        "yield_per_tile_per_day": 0.50,
    },
    "SHEEP": {
        "product": "WOOL",
        "purchase_cost": 500,
        "base_market_price": 200,
        "first_yield_day": 6,
        "yield_interval_days": 3,
        "max_held": 6,
        "structure": "PASTURE",
        "build_action_cost": 1,
        "yield_per_tile_per_day": 0.33,
    },
}

FERTILIZER: Final[dict[str, int]] = {
    "purchase_cost": 100,
    "base_market_price": 100,
    "action_cost": 1,
}

# Parâmetros da função dinâmica de preços por recurso. I0 é o inventário de
# equilíbrio; T é o horizonte de throughput usado na calibração da curva.
MARKET_PARAMS: Final[dict[str, dict[str, Any]]] = {
    "WHEAT": {"base": 25, "I0": 10_000, "T": 400, "below_func": "sqrt", "below_target": 0.80, "above_func": "log", "above_target": 0.20},
    "CARROT": {"base": 35, "I0": 10_000, "T": 450, "below_func": "log", "below_target": 0.20, "above_func": "sqrt", "above_target": 0.70},
    "TOMATO": {"base": 60, "I0": 10_000, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "sqrt", "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": 10_000, "T": 100, "below_func": "sqrt", "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON": {"base": 250, "I0": 10_000, "T": 300, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.60},
    "EGG": {"base": 50, "I0": 10_000, "T": 332, "below_func": "linear", "below_target": 0.40, "above_func": "log", "above_target": 0.20},
    "MILK": {"base": 160, "I0": 10_000, "T": 122, "below_func": "sqrt", "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL": {"base": 200, "I0": 10_000, "T": 105, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": 10_000, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}

BUYABLE_PRODUCTS: Final[tuple[str, ...]] = ("WHEAT", "FERTILIZER")
PRODUCTS: Final[tuple[str, ...]] = tuple(MARKET_PARAMS)
STRUCTURES: Final[tuple[str, ...]] = ("COOP", "PASTURE")
QUADRANTS: Final[tuple[str, ...]] = ("NW", "NE", "SW", "SE")

SHOPS: Final[dict[str, dict[str, int]]] = {
    "BAKERY": {"EGG": 1, "WHEAT": 1},
    "PIZZA_SHOP": {"MILK": 1, "TOMATO": 1, "WHEAT": 1},
    "BRUNCH_SPOT": {"EGG": 1, "WHEAT": 1, "STRAWBERRY": 1},
    "YARN_STORE": {"WOOL": 2},
    "ICE_CREAM_SHOP": {"STRAWBERRY": 1, "MILK": 1, "WHEAT": 1},
    "PET_CAFE": {"CARROT": 2},
    "SMOOTHIE_SHOP": {"STRAWBERRY": 1, "MILK": 1},
    "FARMERS_MARKET": {"WHEAT": 1, "CARROT": 1, "TOMATO": 1, "STRAWBERRY": 1},
}

DEFAULT_CONFIGURATION: Final[dict[str, Any]] = {
    "episodeSteps": 720,
    "boardSize": 10,
    "startingMoney": 3000,
    "maxMarketOrdersPerTurn": 10,
    "turnsPerDay": 24,
    "shedCapacity": 100,
    "weedSpawnChance": 0.005,
    "townShopUnlockInterval": 3,
    "townShopSellInterval": 4,
    "townCenterSellInterval": 24,
    "seed": None,
}

LAND_PURCHASE_COSTS: Final[tuple[int, ...]] = (1_000, 2_000, 4_000)
FARM_HAND_FIBONACCI_COSTS: Final[tuple[int, ...]] = (1, 1, 2, 3, 5, 8, 13, 21)
TOWN_CENTER_DEMAND: Final[dict[str, int]] = {
    product: 1 for product in PRODUCTS if product != "FERTILIZER"
}


def get_crop(crop: str) -> dict[str, Any]:
    """Retorna uma cópia dos dados de uma cultura.

    Raises:
        KeyError: se ``crop`` não for uma cultura conhecida.
    """
    return deepcopy(CROPS[crop])


def get_animal(animal: str) -> dict[str, Any]:
    """Retorna uma cópia dos dados de um animal."""
    return deepcopy(ANIMALS[animal])


def get_market_params(resource: str) -> dict[str, Any]:
    """Retorna uma cópia dos parâmetros de preço de ``resource``."""
    return deepcopy(MARKET_PARAMS[resource])
