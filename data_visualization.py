import os, math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class DataVisualization:
    def __init__(self):
        os.makedirs("charts", exist_ok=True)
        
    @staticmethod
    def _safe_attrs(character: dict) -> list[float]:
        attrs = character.get("attributes") or character.get("base_attributes", [0]*5)
        if len(attrs) < 5:
            attrs = list(attrs) + [0] * (5 - len(attrs))
        return [float(v) for v in attrs[:5]]

    @staticmethod
    def _bar_color(index: int) -> str:
        palette = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]
        return palette[index % len(palette)]
    
    def radar_chart(self, character: dict, save: bool = True) -> str | None:
        attrs = self._safe_attrs(character)
        name = character.get("name", "Unknown")
        labels = ["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]
        N = len(labels)

        max_val = max(attrs) if max(attrs) > 0 else 1
        values = [v / max_val for v in attrs]
        values += values[:1]

        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.set_theta_offset(math.pi / 2)
        ax.set_theta_direction(-1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=11, fontweight="bold")
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["25%", "50%", "75%", "100%"], size=7, color="grey")
        ax.set_ylim(0, 1)

        ax.plot(angles, values, linewidth=2, linestyle="solid", color="#4e79a7")
        ax.fill(angles, values, alpha=0.35, color="#4e79a7")

        for i, (angle, value, raw) in enumerate(zip(angles[:-1], values[:-1], attrs)):
            ax.annotate(f"{raw:.1f}", xy=(angle, value),
                        xytext=(angle, value + 0.08),
                        ha="center", va="center", fontsize=9, color="#333333")

        title_text = (
            f"{name}\n"
            f"{character.get('race','?')} {character.get('class','?').title()} "
            f"– Lvl {character.get('level', '?')}"
        )
        ax.set_title(title_text, size=13, fontweight="bold", pad=20)

        plt.tight_layout()
        if save:
            path = os.path.join("charts", f"{name.replace(' ','_')}_radar.png")
            plt.savefig(path, dpi=120, bbox_inches="tight")
            plt.close()
            return path
        plt.show()
        plt.close()
        return None
    
    def bar_chart(self, character: dict, save: bool = True) -> str | None:
        attrs = self._safe_attrs(character)
        name = character.get("name", "Unknown")
        colors = [self._bar_color(i) for i in range(len(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]))]

        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"], attrs, color=colors, edgecolor="white", height=0.6)

        for bar, val in zip(bars, attrs):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}", va="center", ha="left", fontsize=10)

        ax.set_xlabel("Stat Value", fontsize=11)
        ax.set_title(
            f"{name} – Stat Overview\n"
            f"{character.get('race','?')} {character.get('class','?').title()} "
            f"Lvl {character.get('level','?')}",
            fontsize=13, fontweight="bold"
        )
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(0, max(attrs) * 1.2 if attrs else 10)
        plt.tight_layout()

        if save:
            path = os.path.join("charts", f"{name.replace(' ','_')}_bar.png")
            plt.savefig(path, dpi=120, bbox_inches="tight")
            plt.close()
            return path
        plt.show()
        plt.close()
        return None

    def comparison_chart(self, characters: list[dict], save: bool = True) -> str | None:
        if not characters:
            print("No characters to compare.")
            return None

        n_chars = len(characters)
        x = np.arange(len(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]))
        width = 0.8 / n_chars

        fig, ax = plt.subplots(figsize=(10, 5))

        for i, char in enumerate(characters):
            attrs = self._safe_attrs(char)
            offset = (i - n_chars / 2 + 0.5) * width
            bars = ax.bar(x + offset, attrs, width, label=char.get("name","?"),
                            color=self._bar_color(i), edgecolor="white", alpha=0.9)
            for bar, val in zip(bars, attrs):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                        f"{val:.1f}", ha="center", va="bottom", fontsize=7)

        ax.set_xticks(x)
        ax.set_xticklabels(["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"], fontsize=11)
        ax.set_ylabel("Stat Value", fontsize=11)
        ax.set_title("Character Stat Comparison", fontsize=14, fontweight="bold")
        ax.legend(loc="upper right")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()

        if save:
            names = "_vs_".join(c.get("name","?").replace(" ","_") for c in characters)
            path = os.path.join("charts", f"{names}_comparison.png")
            plt.savefig(path, dpi=120, bbox_inches="tight")
            plt.close()
            return path
        plt.show()
        plt.close()
        return None
    
    def class_distribution_chart(self, characters: list[dict], save: bool = True) -> str | None:
        from collections import Counter
        counts = Counter(c.get("class", "unknown") for c in characters)
        labels = [k.title() for k in counts.keys()]
        sizes = list(counts.values())
        colors = [self._bar_color(i) for i in range(len(labels))]

        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct="%1.1f%%", startangle=140,
            wedgeprops=dict(edgecolor="white", linewidth=1.5)
        )
        for t in autotexts:
            t.set_fontsize(10)
        ax.set_title("Class Distribution", fontsize=14, fontweight="bold")
        plt.tight_layout()

        if save:
            path = os.path.join("charts", "class_distribution.png")
            plt.savefig(path, dpi=120, bbox_inches="tight")
            plt.close()
            return path
        plt.show()
        plt.close()
        return None
    
    def level_progression_chart(self, characters: list[dict], save: bool = True) -> str | None:
        if not characters:
            return None

        sorted_chars = sorted(characters, key=lambda c: c.get("level", 0), reverse=True)
        names = [c.get("name", "?") for c in sorted_chars]
        levels = [c.get("level", 0)  for c in sorted_chars]
        colors = [self._bar_color(i) for i in range(len(names))]

        fig, ax = plt.subplots(figsize=(8, max(3, len(names) * 0.6)))
        bars = ax.barh(names, levels, color=colors, edgecolor="white", height=0.6)

        for bar, lvl in zip(bars, levels):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                    f"Lvl {lvl}", va="center", ha="left", fontsize=9)

        ax.set_xlabel("Level", fontsize=11)
        ax.set_title("Character Level Progression", fontsize=14, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(0, max(levels) * 1.2 + 1 if levels else 10)
        plt.tight_layout()

        if save:
            path = os.path.join("charts", "level_progression.png")
            plt.savefig(path, dpi=120, bbox_inches="tight")
            plt.close()
            return path
        plt.show()
        plt.close()
        return None