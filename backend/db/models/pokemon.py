from typing import Any
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

class PokemonSpecies(Base):
    __tablename__ = "pokemon_species"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    names: Mapped[dict[str, str]]
    
    introduced_generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)
    is_legendary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_mythical: Mapped[bool] = mapped_column(Boolean, default=False)
    evolution_chain_id: Mapped[int] = mapped_column(Integer, index=True)
    
    # Relaciones
    varieties: Mapped[list["Pokemon"]] = relationship(back_populates="species")

class Pokemon(Base):
    __tablename__ = "pokemons"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    species_id: Mapped[int] = mapped_column(ForeignKey("pokemon_species.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # Distinguimos entre formas base de las alternativas (Deoxys forma ataque, Meowth de alola, etc)
    is_default: Mapped[bool] = mapped_column(Boolean, default=True)
    # Altura en decimetro
    height: Mapped[int] = mapped_column(Integer)
    # Peso en hectogramos = 100gr (Nos aseguramos que sean valores enteros)
    weight: Mapped[int] = mapped_column(Integer)
    
    # Relaciones
    species: Mapped["PokemonSpecies"] = relationship(back_populates="varieties")
    stats: Mapped[list["PokemonStats"]] = relationship(back_populates="pokemon")
    types: Mapped[list["PokemonType"]] = relationship(back_populates="pokemon")
    game_data: Mapped[list["PokemonGameData"]] = relationship(back_populates="pokemon")

class PokemonStats(Base):
    __tablename__ = "pokemon_stats"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id", ondelete="CASCADE"), index=True)
    generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)
    
    hp: Mapped[int] = mapped_column(Integer)
    attack: Mapped[int] = mapped_column(Integer)
    special_attack: Mapped[int] = mapped_column(Integer)
    defense: Mapped[int] = mapped_column(Integer)
    special_defense: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)
    
    # Relaciones
    pokemon: Mapped["Pokemon"] = relationship(back_populates="stats")
    
    # Restricciones
    __table_args__ = (
        UniqueConstraint("pokemon_id", "generation_id", name="uq_pokemon_stats_gen"),
    )

class PokemonType(Base):
    __tablename__ = "pokemon_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id", ondelete="CASCADE"), index=True)
    generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)
    
    slot: Mapped[int] = mapped_column(Integer)
    type_id: Mapped[int] = mapped_column(ForeignKey("types.id", ondelete="RESTRICT"), index=True)
    
    # Relaciones
    pokemon: Mapped["Pokemon"] = relationship(back_populates="types")
    
    # Restricciones
    __table_args__ = (
        UniqueConstraint("pokemon_id", "generation_id", "slot", name="uq_pokemon_type_slot"),
        CheckConstraint("slot IN (1, 2)", name="ck_pokemon_type_slot_valid"),
    )

class PokemonGameData(Base):
    __tablename__ = "pokemon_game_data"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.id", ondelete="CASCADE"), index=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    
    # Puede ser None si el pokemon es transferible al juego pero no se puede capturar
    regional_dex_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    # Entrada de la pokedex (Puede ser null por si una forma alterna no tiene entrada de la pokedex)
    flavor_text: Mapped[dict[str, str] | None]
    sprites: Mapped[dict[str, Any]]
    
    # Relaciones
    pokemon: Mapped["Pokemon"] = relationship(back_populates="game_data")
    
    # Restricciones
    __table_args__ = (
        UniqueConstraint("pokemon_id", "game_id", name="uq_pokemon_game_data"),
    )

class Evolution(Base):
    __tablename__ = "evolutions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_species_id: Mapped[int] = mapped_column(ForeignKey("pokemon_species.id", ondelete="CASCADE"), index=True)
    to_species_id: Mapped[int] = mapped_column(ForeignKey("pokemon_species.id", ondelete="CASCADE"), index=True)
    min_generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)
    
    trigger: Mapped[str] = mapped_column(String(50))
    conditions: Mapped[dict[str, Any]]
    
    # Relaciones
    from_species: Mapped["PokemonSpecies"] = relationship(foreign_keys=[from_species_id])
    to_species: Mapped["PokemonSpecies"] = relationship(foreign_keys=[to_species_id])