import os
import pandas as pd

class StatisticalAnalyzer:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.df: pd.DataFrame = pd.DataFrame()

    def load_characters(self, characters: tuple | list) -> pd.DataFrame:
        rows = []
        for c in characters:
            attrs = c.get("attributes") or c.get("base_attributes", [0]*5)
            if len(attrs) < 5:
                attrs = list(attrs) + [0] * (5 - len(attrs))
            rows.append({
                "name": c.get("name", "Unknown"),
                "class": c.get("class", "unknown"),
                "race": c.get("race",  "unknown"),
                "level": c.get("level", 1),
                "Damage": round(float(attrs[0]), 2),
                "Dexterity": round(float(attrs[1]), 2),
                "Intelligence": round(float(attrs[2]), 2),
                "Constitution": round(float(attrs[3]), 2),
                "Charisma": round(float(attrs[4]), 2),
                "skills": len(c.get("skills", [])),
                "items": len(c.get("inventory", [])),
            })
        self.df = pd.DataFrame(rows)
        return self.df
    
    def summary_stats(self) -> str:
        if self.df.empty:
            return "No character data loaded."

        stats_df = self.df[["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]].agg(["mean", "median", "max", "min"]).round(2)
        lines = ["=" * 60, f"  ROSTER STATISTICAL SUMMARY  ({len(self.df)} characters)","=" * 60]

        header = f"{'Stat':<16}" + "".join(f"{col.upper():<10}" for col in stats_df.columns)
        lines.append(header)
        lines.append("-" * 60)

        label_map = {"mean": "Mean", "median": "Median", "max": "Max", "min": "Min"}
        for idx, row in stats_df.iterrows():
            row_str = f"{label_map.get(idx, idx):<16}" + "".join(f"{v:<10}" for v in row)
            lines.append(row_str)

        lines.append("=" * 60)
        return "\n".join(lines)

    def top_characters(self, stat: str, n: int = 3) -> str:
        if self.df.empty or stat not in self.df.columns:
            return f"Stat '{stat}' not found."

        top = self.df[["name", "class", "race", "level", stat]].nlargest(n, stat)
        lines = [f"\n  TOP {n} CHARACTERS BY {stat.upper()}", "-" * 45]
        for rank, (_, row) in enumerate(top.iterrows(), 1):
            lines.append(
                f"  {rank}. {row['name']:<18} {row['class'].title():<12} "
                f"Lvl {row['level']:<4} {stat}: {row[stat]}"
            )
        return "\n".join(lines)

    def class_averages(self) -> str:
        if self.df.empty:
            return "No character data loaded."

        grouped = self.df.groupby("class")[["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]].mean().round(2)
        lines = ["\n  AVERAGE STATS BY CLASS", "=" * 55]
        for cls, row in grouped.iterrows():
            lines.append(f"\n  {cls.title()}")
            lines.append("  " + "-" * 40)
            for stat in ["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]:
                bar_len = int(row[stat] / max(grouped[stat].max(), 1) * 20)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                lines.append(f"    {stat:<14} {bar}  {row[stat]}")
        return "\n".join(lines)

    def filter_by_class(self, cls: str) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        return self.df[self.df["class"].str.lower() == cls.lower()]

    def filter_by_level(self, min_level: int = 0, max_level: int = 999) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        return self.df[(self.df["level"] >= min_level) & (self.df["level"] <= max_level)]

    def sort_by(self, column: str, ascending: bool = False) -> pd.DataFrame:
        if self.df.empty or column not in self.df.columns:
            return self.df
        return self.df.sort_values(column, ascending=ascending)

    def print_dataframe(self, df: pd.DataFrame | None = None, title: str = "Character Data") -> None:
        target = df if df is not None else self.df
        if target.empty:
            print("  (No characters to display)")
            return
        print(f"\n  {title}")
        print("  " + "=" * 60)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 120)
        pd.set_option("display.float_format", "{:.2f}".format)
        print(target.to_string(index=False))
        print("  " + "=" * 60)

    def export_csv(self, filename: str = "characters.csv") -> str:
        if self.df.empty:
            return "No data to export."
        path = os.path.join("data", filename)
        self.df.to_csv(path, index=False)
        return path

    def import_csv(self, filename: str = "characters.csv") -> pd.DataFrame | None:
        path = os.path.join("data", filename)
        if not os.path.exists(path):
            return None
        self.df = pd.read_csv(path)
        return self.df
    
    def optimization_tip(self, character: dict) -> str:
        if self.df.empty:
            return "Load the roster first to get optimization tips."

        attrs = character.get("attributes") if character.get("attributes") else character.get("base_attributes", [0]*5)
        lines = [f"\n  OPTIMIZATION TIPS FOR: {character.get('name','?').upper()}", "  " + "-" * 45]

        for i, stat in enumerate(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]):
            val = float(attrs[i]) if i < len(attrs) else 0.0
            avg = self.df[stat].mean()
            diff = val - avg
            symbol = "▲" if diff >= 0 else "▼"
            lines.append(f"  {stat:<16} {val:>6.2f}  (roster avg {avg:>6.2f})  {symbol} {abs(diff):.2f}")

        weak = min(range(len(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"])), key=lambda i: float(attrs[i]) if i < len(attrs) else 0)
        lines.append(f"\n  💡 Consider boosting {["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"][weak]} - it's your lowest stat.")
        return "\n".join(lines)