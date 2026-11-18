from tkinter import CASCADE

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Generation(Base):
    __tablename__ = "generations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Texto unico e indexado (EJ: "generation-III")
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # Diccionario bilingüe (JSONB)
    names: Mapped[dict[str, str]]
    
    # Relaciones
    version_groups: Mapped[list["VersionGroup"]] = relationship(back_populates="generation")

class VersionGroup(Base):
    __tablename__ = "version_groups"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Texto unico e indexado (EJ: "emerald")
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id"))
    
    # Relaciones
    generation: Mapped["Generation"] = relationship(back_populates="version_groups")
    
    games: Mapped[list["Game"]] = relationship(back_populates="version_group")
    
class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Texto unico e indexado (EJ: "esmeralda")
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    pokeapi_slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    names: Mapped[dict[str, str]]
    cover_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version_group_id: Mapped[int] = mapped_column(ForeignKey("version_groups.id", ondelete="CASCADE"))
    
    # Relaciones
    version_group: Mapped["VersionGroup"] = relationship(back_populates="games")

class Type(Base):
    __tablename__ = "types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Texto unico e indexado (EJ: "esmeralda")
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    names: Mapped[dict[str, str]]
    introduced_generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)

class TypeEfficacy(Base):
    __tablename__ = "type_efficacies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id", ondelete="RESTRICT"), index=True)
    attacking_type_id: Mapped[int] = mapped_column(ForeignKey("types.id"))
    defending_type_id: Mapped[int] = mapped_column(ForeignKey("types.id"))
    damage_factor: Mapped[int] = mapped_column(Integer, default=100)
    
    # Relaciones
    __table_args__ = (
        UniqueConstraint("generation_id", "attacking_type_id", "defending_type_id", name="uq_type_efficacy_gen"),
        CheckConstraint("damage_factor IN (0, 50, 100, 200)", name="ck_damage_factor_valid")
    )