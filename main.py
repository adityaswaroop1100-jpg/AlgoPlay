"""
main.py - Entry Point and Primary Application Shell for AlgoPlay.

Assembles multi-tab interface (Sorting & Searching), animation drivers,
Race Mode, benchmark, theme toggler, shortcuts, HintEngine, Progress HUD,
and Pre-Flight Concept & Complexity Briefing before visual representation.
"""

import os, sys, random, glob
os.environ["TK_SILENCE_DEPRECATION"] = "1"
if sys.platform == "darwin":
    for _p in glob.glob("/opt/homebrew/Cellar/python-tk*/*/libexec"):
        if _p not in sys.path: sys.path.insert(0, _p)
    if "opt/homebrew" not in sys.executable and os.path.exists("/opt/homebrew/bin/python3") and not os.environ.get("ALGOPLAY_NO_REEXEC"):
        os.environ["ALGOPLAY_NO_REEXEC"] = "1"; os.execv("/opt/homebrew/bin/python3", ["python3"] + sys.argv)

import tkinter as tk
from typing import Dict, Generator, List, Optional
from theme import FONTS, theme_manager
from stats import StatsTracker; from algorithm_base import AlgorithmStep
from sorting import SORTING_ALGORITHMS; from searching import SEARCHING_ALGORITHMS
from visualizer import VisualizerCanvas; from widgets import FlatButton; from coach import FunCoachPanel
from controls import ControlPanel, StatsPanel, PseudoCodePanel, ComplexityPanel
from quiz import QuizWindow, play_sound; from story_tab import StoryTab
from race_window import RaceWindow
from hint_engine import HintEngine
from progress_hud import ProgressHUD, LearningTicker
from concept_briefing import show_concept_briefing


class AlgoPlayApp:
    """Main Application Controller: tabs, animation, and interactive concept briefing."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root; self.root.title("AlgoPlay — Algorithm Visualizer")
        self.root.geometry("1240x810"); self.root.minsize(980, 640); self.root.configure(bg=theme_manager.get("bg_root"))
        self.data_size = 20; self.original_data = [random.randint(10, 99) for _ in range(self.data_size)]
        self.current_data = list(self.original_data); self.stats = StatsTracker()
        self.is_running = self.is_paused = False; self.active_generator: Optional[Generator[AlgorithmStep, None, None]] = None
        self._card_frames: List[tk.Widget] = []; self._root_frames: List[tk.Widget] = []
        self.hint_engine = HintEngine(root); self.hint_engine.on_pause_change = self._on_quiz_pause
        self.auto_briefing = tk.BooleanVar(value=True); self._briefing_shown_for: Dict[str, bool] = {}
        self._peek_step: Optional[AlgorithmStep] = None; self._build_ui()
        self.select_sort("Bubble Sort"); self.select_search("Linear Search")
        self.sort_canvas.set_algo_name("Bubble Sort")
        self.search_canvas.set_algo_name("Linear Search")
        self._bind_keys(); theme_manager.register_listener(self.apply_theme)

    def _bind_keys(self) -> None:
        for seq, fn in [("<space>", self._kb_step), ("<Right>", self._kb_step), ("<r>", lambda e: self.action_reset()),
                        ("<R>", lambda e: self.action_reset()), ("<s>", lambda e: self.action_randomize()),
                        ("<S>", lambda e: self.action_randomize()), ("<p>", self._kb_pause), ("<P>", self._kb_pause),
                        ("<Return>", lambda e: self.action_start())]: self.root.bind(seq, fn)

    def _kb_step(self, _=None) -> None: (self.action_pause if self.is_running else self.action_step)()
    def _kb_pause(self, _=None) -> None: (self.action_pause if self.is_running else self.action_start)()
    def _on_quiz_pause(self, paused: bool) -> None: (self.action_pause() if paused and self.is_running else None)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        hdr = tk.Frame(self.root, bg=c["bg_card"], padx=16, pady=8, highlightthickness=1, highlightbackground=c["border"]); hdr.pack(fill="x")
        lf = tk.Frame(hdr, bg=c["bg_card"]); lf.pack(side="left")
        self.logo_algo = tk.Label(lf, text="Algo", font=("Avenir Next", 17, "bold"), bg=c["bg_card"], fg="#FFFFFF"); self.logo_algo.pack(side="left")
        self.logo_play = tk.Label(lf, text="Play", font=("Avenir Next", 17, "bold"), bg=c["bg_card"], fg=c["accent"]); self.logo_play.pack(side="left")
        self.tag_lbl   = tk.Label(lf, text="Visualize • Learn • Explore", font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"]); self.tag_lbl.pack(side="left", padx=10)

        tab_f = tk.Frame(hdr, bg=c["bg_card"]); tab_f.pack(side="left", padx=20)
        self.btn_tab_sort   = FlatButton(tab_f, text="↕ Sorting",    font=FONTS["body_bold"], bg=c["accent"],           fg=c["accent_fg"],       padx=14, pady=3, command=lambda: self._switch_tab(0)); self.btn_tab_sort.pack(side="left", padx=3)
        self.btn_tab_search = FlatButton(tab_f, text="🔍 Searching",  font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=14, pady=3, command=lambda: self._switch_tab(1)); self.btn_tab_search.pack(side="left", padx=3)
        self.btn_tab_story  = FlatButton(tab_f, text="📖 Story Mode", font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=12, pady=3, command=lambda: self._switch_tab(2)); self.btn_tab_story.pack(side="left", padx=3)
        self.btn_race       = FlatButton(tab_f, text="🏁 Race",       font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=12, pady=3, command=lambda: RaceWindow(self.root, self.current_data)); self.btn_race.pack(side="left", padx=3)
        self.btn_benchmark  = FlatButton(tab_f, text="📊 Benchmark",  font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=12, pady=3, command=self.show_benchmark); self.btn_benchmark.pack(side="left", padx=3)
        self.btn_quiz       = FlatButton(tab_f, text="🎮 Quiz",       font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=12, pady=3, command=lambda: QuizWindow(self.root)); self.btn_quiz.pack(side="left", padx=3)

        self.lbl_xp   = tk.Label(hdr, text="⚡ 0 XP", font=FONTS["caption_bold"], bg=c["bg_card"], fg=c["warning"]); self.lbl_xp.pack(side="right", padx=6)
        self.lbl_keys = tk.Label(hdr, text="Space=Step  R=Reset  S=Shuffle  P=Pause", font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_dim"]); self.lbl_keys.pack(side="right", padx=8)
        self.btn_theme = FlatButton(hdr, text=theme_manager.get_toggle_icon(), font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=10, pady=3, command=self.toggle_theme); self.btn_theme.pack(side="right", padx=3)

        self.tab_idx = 0
        self.tab_container = tk.Frame(self.root, bg=c["bg_root"]); self.tab_container.pack(fill="both", expand=True, padx=12, pady=(4, 0))
        self.tab_sort = tk.Frame(self.tab_container, bg=c["bg_root"]); self.tab_search = tk.Frame(self.tab_container, bg=c["bg_root"])
        self.tab_sort.pack(fill="both", expand=True)
        self._card_frames.extend([hdr, lf, tab_f]); self._root_frames.extend([self.tab_container, self.tab_sort, self.tab_search])

        (self.sort_canvas, self.sort_comp, self.sort_pseudo, self.sort_stats, self.sort_ctrl,
         self.sort_coach, self.sort_chips, self.sort_cnt, self.sort_hud) = self._setup_tab(self.tab_sort, "bars", SORTING_ALGORITHMS, self.select_sort)
        (self.search_canvas, self.search_comp, self.search_pseudo, self.search_stats, self.search_ctrl,
         self.search_coach, self.search_chips, self.search_cnt, self.search_hud) = self._setup_tab(self.tab_search, "boxes", SEARCHING_ALGORITHMS, self.select_search, has_target=True)
        self.story_tab = StoryTab(self.tab_container); self._root_frames.append(self.story_tab)
        self.ticker = LearningTicker(self.root); self.ticker.pack(fill="x", side="bottom")

    def _setup_tab(self, parent, mode, algos, on_select, has_target=False):
        c = theme_manager.colors
        sel = tk.Frame(parent, bg=c["bg_card"], padx=10, pady=5, highlightthickness=1, highlightbackground=c["border"]); sel.pack(side="top", fill="x", pady=(2, 6))
        tk.Label(sel, text="Algorithm:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_secondary"]).pack(side="left", padx=(4, 8))
        chips = {}
        for name in algos:
            btn = FlatButton(sel, text=name, font=FONTS["caption_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=10, pady=3, command=lambda n=name: on_select(n))
            btn.pack(side="left", padx=3); chips[name] = btn
        FlatButton(sel, text="💡 Concept & Complexity", font=FONTS["caption_bold"], bg=c["btn_secondary_bg"], fg=c["accent"],
                   padx=10, pady=3, command=self.show_current_briefing).pack(side="right", padx=4)
        if has_target:
            tk.Label(sel, text="Target:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_secondary"]).pack(side="left", padx=(12, 4))
            self.entry_target = tk.Entry(sel, width=6, font=FONTS["body"], bg=c["entry_bg"], fg=c["entry_fg"], relief="flat")
            self.entry_target.insert(0, str(self.current_data[len(self.current_data)//2])); self.entry_target.pack(side="left", padx=2)
        ctrl = ControlPanel(parent, on_randomize=self.action_randomize, on_start=self.action_start,
                            on_pause=self.action_pause, on_step=self.action_step, on_reset=self.action_reset,
                            on_custom_load=self.action_load_custom, on_size_change=self.action_size_change,
                            on_info=self.show_info, is_searching=has_target); ctrl.pack(side="bottom", fill="x", pady=(2, 4))
        hud = ProgressHUD(parent); hud.pack(side="bottom", fill="x", pady=(0, 1))
        stats_card = tk.Frame(parent, bg=c["bg_card"], highlightthickness=1, highlightbackground=c["border"]); stats_card.pack(side="bottom", fill="x", pady=2)
        comp = ComplexityPanel(stats_card); comp.pack(side="left", fill="both", expand=True)
        tk.Frame(stats_card, bg=c["border"], width=1).pack(side="left", fill="y", pady=6)
        stats = StatsPanel(stats_card); stats.pack(side="right", fill="both", expand=True)
        split = tk.Frame(parent, bg=c["bg_root"]); split.pack(side="top", fill="both", expand=True)
        right = tk.Frame(split, bg=c["bg_root"], width=310); right.pack(side="right", fill="y", padx=(6, 0))
        pseudo = PseudoCodePanel(right); pseudo.pack(side="top", fill="both", expand=True, pady=(0, 4))
        coach = FunCoachPanel(right, is_searching=has_target); coach.pack(side="bottom", fill="x")
        left = tk.Frame(split, bg=c["bg_root"]); left.pack(side="left", fill="both", expand=True)
        vis_card = tk.Frame(left, bg=c["bg_card"], highlightthickness=1, highlightbackground=c["border"]); vis_card.pack(side="top", fill="both", expand=True)
        v_hdr = tk.Frame(vis_card, bg=c["bg_card"], padx=12, pady=6); v_hdr.pack(fill="x")
        tk.Label(v_hdr, text="📊  Array Visualization", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left")
        lbl_elem = tk.Label(v_hdr, text=f"{self.data_size} elements  📊", font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"]); lbl_elem.pack(side="right")
        canvas = VisualizerCanvas(vis_card, mode=mode); canvas.pack(side="top", fill="both", expand=True, padx=4, pady=(0, 4))
        self._card_frames.extend([sel, stats_card, vis_card, v_hdr]); self._root_frames.extend([split, left, right])
        return canvas, comp, pseudo, stats, ctrl, coach, chips, lbl_elem, hud

    def _switch_tab(self, idx: int) -> None:
        self.tab_idx = idx; c = theme_manager.colors
        for t in (self.tab_sort, self.tab_search, self.story_tab): t.pack_forget()
        (self.tab_sort if idx == 0 else (self.tab_search if idx == 1 else self.story_tab)).pack(fill="both", expand=True)
        for i, b in enumerate((self.btn_tab_sort, self.btn_tab_search, self.btn_tab_story)):
            b.config(bg=c["accent"] if idx==i else c["btn_secondary_bg"], fg=c["accent_fg"] if idx==i else c["btn_secondary_fg"])
        if idx != 2: self.action_reset()
        else: self.story_tab.on_tab_shown()

    def select_sort(self, name: str) -> None:
        self.cur_sort = name; a = SORTING_ALGORITHMS[name]; c = theme_manager.colors; self._briefing_shown_for[name] = False
        for n, btn in getattr(self, "sort_chips", {}).items():
            btn.config(bg=c["accent"] if n==name else c["btn_secondary_bg"], fg=c["accent_fg"] if n==name else c["btn_secondary_fg"])
        self.sort_pseudo.set_code(a.pseudo_code); self.sort_comp.update_info(a.get_info()); self.action_reset()
        if hasattr(self, "sort_canvas"): self.sort_canvas.set_algo_name(name)

    def select_search(self, name: str) -> None:
        self.cur_search = name; a = SEARCHING_ALGORITHMS[name]; c = theme_manager.colors; self._briefing_shown_for[name] = False
        for n, btn in getattr(self, "search_chips", {}).items():
            btn.config(bg=c["accent"] if n==name else c["btn_secondary_bg"], fg=c["accent_fg"] if n==name else c["btn_secondary_fg"])
        self.search_pseudo.set_code(a.pseudo_code); self.search_comp.update_info(a.get_info()); self.action_reset()
        if hasattr(self, "search_canvas"): self.search_canvas.set_algo_name(name)

    def show_current_briefing(self) -> None:
        algo = self.cur_search if (self.tab_idx == 1) else self.cur_sort
        show_concept_briefing(self.root, algo, on_start=self._start_engine, on_step=self.action_step, auto_pref_var=self.auto_briefing)

    def action_randomize(self) -> None:
        self.is_running = False; self.original_data = [random.randint(10, 99) for _ in range(self.data_size)]
        self.current_data = list(self.original_data)
        if hasattr(self, "entry_target"):
            self.entry_target.delete(0, "end"); self.entry_target.insert(0, str(random.choice(self.current_data)))
        self.action_reset()

    def action_size_change(self, size: int) -> None:
        self.data_size = size
        for cnt in (getattr(self, "sort_cnt", None), getattr(self, "search_cnt", None)):
            if cnt: cnt.config(text=f"{self.data_size} elements  📊")
        self.action_randomize()

    def action_load_custom(self, custom: List[int]) -> None:
        self.is_running = False; self.data_size = len(custom)
        for cnt in (getattr(self, "sort_cnt", None), getattr(self, "search_cnt", None)):
            if cnt: cnt.config(text=f"{self.data_size} elements  📊")
        self.original_data = self.current_data = list(custom); self.action_reset()

    def action_reset(self) -> None:
        self.is_running = self.is_paused = False
        self.current_data = list(self.original_data); self.stats.reset(); self.active_generator = None
        self._peek_step = None; self.hint_engine.reset()
        for cv in (getattr(self, "sort_canvas", None), getattr(self, "search_canvas", None)):
            if cv: cv.reset_counters()
        self._update_ui(AlgorithmStep(array=list(self.current_data)))
        self.sort_ctrl.set_running_state(False); self.search_ctrl.set_running_state(False)
        for hud in (getattr(self, "sort_hud", None), getattr(self, "search_hud", None)):
            if hud: hud.reset()

    def action_start(self) -> None:
        if self.is_running: return
        algo = self.cur_search if (self.tab_idx == 1) else self.cur_sort
        if self.auto_briefing.get() and not self._briefing_shown_for.get(algo, False):
            self._briefing_shown_for[algo] = True
            show_concept_briefing(self.root, algo, on_start=self._start_engine, on_step=self.action_step, auto_pref_var=self.auto_briefing)
            return
        self._start_engine()

    def _start_engine(self) -> None:
        if self.is_running: return
        self.is_running, self.is_paused = True, False; self.stats.start()
        is_s = (self.tab_idx == 1); (self.search_ctrl if is_s else self.sort_ctrl).set_running_state(True)
        if not self.active_generator:
            tgt = int(self.entry_target.get() or "0") if is_s else 0
            algo = SEARCHING_ALGORITHMS[self.cur_search] if is_s else SORTING_ALGORITHMS[self.cur_sort]
            self.active_generator = algo.run(list(self.current_data), target=tgt)
        self._anim_loop()

    def action_pause(self) -> None:
        self.is_running, self.is_paused = False, True; self.stats.pause()
        self.sort_ctrl.set_running_state(False); self.search_ctrl.set_running_state(False)

    def action_step(self) -> None:
        if not self.active_generator:
            is_s = (self.tab_idx == 1); tgt = int(self.entry_target.get() or "0") if is_s else 0
            self.active_generator = (SEARCHING_ALGORITHMS[self.cur_search] if is_s else SORTING_ALGORITHMS[self.cur_sort]).run(list(self.current_data), target=tgt)
        self._advance()

    def _anim_loop(self) -> None:
        if self.is_running and self.active_generator:
            if self._advance():
                d = (self.search_ctrl if self.tab_idx == 1 else self.sort_ctrl).get_delay_ms()
                self.root.after(d, self._anim_loop)
            else:
                self.is_running = False; self.stats.stop()
                self.sort_ctrl.set_running_state(False); self.search_ctrl.set_running_state(False)
                play_sound("Glass"); self._update_xp_strip()

    def _advance(self) -> bool:
        try:
            step = next(self.active_generator)
            if step.comparing: self.stats.increment_comparisons(); play_sound("Tink")
            if step.swapping:  self.stats.increment_swaps(); play_sound("Pop")
            hud = self.search_hud if self.tab_idx == 1 else self.sort_hud
            if hud: hud.advance()
            try:
                nxt = next(self.active_generator); orig = self.active_generator
                def _chain(a, b): yield a; yield from b
                self.active_generator = _chain(nxt, orig); self._peek_step = nxt
            except StopIteration: self._peek_step = None
            algo_name = self.cur_search if self.tab_idx == 1 else self.cur_sort
            self.hint_engine.maybe_quiz(algo_name, step, self._peek_step)
            self._update_xp_strip(); self._update_ui(step); return True
        except StopIteration: return False

    def _update_xp_strip(self) -> None:
        if hasattr(self, "lbl_xp"): self.lbl_xp.configure(text=self.hint_engine.xp_label)

    def _update_ui(self, step: AlgorithmStep) -> None:
        is_s = (self.tab_idx == 1)
        cv = self.search_canvas if is_s else self.sort_canvas; ps = self.search_pseudo if is_s else self.sort_pseudo
        st = self.search_stats if is_s else self.sort_stats; ch = self.search_coach if is_s else self.sort_coach
        (cv.render_searching if is_s else cv.render_sorting)(step); ps.highlight_line(step.pseudo_line)
        ch.update_step(self.cur_search if is_s else self.cur_sort, step)
        st.update_metrics(self.stats.comparisons, self.stats.swaps, self.stats.formatted_time, step.status, step.variables)

    def show_benchmark(self) -> None:
        res = {n: sum(1 for s in a.run(list(self.original_data)) if s.comparing) for n, a in SORTING_ALGORITHMS.items()}
        win = tk.Toplevel(self.root); win.title("AlgoPlay — Benchmark"); win.geometry("540x300")
        cv = VisualizerCanvas(win, mode="bars", bg=theme_manager.get("bg_canvas"))
        cv.pack(fill="both", expand=True); cv.render_comparison_chart(res)

    def show_info(self) -> None:
        win = tk.Toplevel(self.root); win.title("AlgoPlay — Quick Guide"); win.geometry("500x280")
        c = theme_manager.colors; win.configure(bg=c["bg_card"], padx=16, pady=10)
        tk.Label(win, text="ℹ️  AlgoPlay Guide & Cheat Sheet", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["accent"]).pack(anchor="w", pady=(0, 6))
        for t in ["🔵 Blue: Unsorted  🟠 Comparing  🔴 Swapping  🟢 Sorted", "💡 Concept & Complexity: View core logic & Big-O before starting.",
                  "🤔 Why? — deep concept explanation per step.", "⚡ XP: predict next steps correctly (quiz every 8 steps).",
                  "Space/→: step  Enter: run  R: reset  S: shuffle  P: pause", "📖 Story Mode  🎮 Quiz  🏁 Race  📊 Benchmark"]:
            tk.Label(win, text=t, font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w", pady=2)
        FlatButton(win, text="Got it!", font=FONTS["body_bold"], bg=c["accent"], fg=c["accent_fg"], padx=12, pady=3, command=win.destroy).pack(side="bottom", pady=6)

    def toggle_theme(self) -> None:
        theme_manager.toggle_theme(); self.btn_theme.config(text=theme_manager.get_toggle_icon())

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors; self.root.configure(bg=c["bg_root"])
        for f in getattr(self, "_card_frames", []): f.configure(bg=c["bg_card"])
        for f in getattr(self, "_root_frames", []): f.configure(bg=c["bg_root"])
        for b in (self.btn_theme, self.btn_benchmark, self.btn_race, self.btn_quiz): b.configure(bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"])
        self.logo_algo.configure(bg=c["bg_card"], fg="#FFFFFF"); self.logo_play.configure(bg=c["bg_card"], fg=c["accent"]); self.tag_lbl.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.lbl_xp.configure(bg=c["bg_card"], fg=c["warning"]); self.lbl_keys.configure(bg=c["bg_card"], fg=c["fg_dim"])
        idx = self.tab_idx
        for i, b in enumerate((self.btn_tab_sort, self.btn_tab_search, self.btn_tab_story)):
            b.config(bg=c["accent"] if idx==i else c["btn_secondary_bg"], fg=c["accent_fg"] if idx==i else c["btn_secondary_fg"])
        for chips, cur in ((getattr(self, "sort_chips", {}), self.cur_sort), (getattr(self, "search_chips", {}), self.cur_search)):
            for n, btn in chips.items(): btn.config(bg=c["accent"] if n==cur else c["btn_secondary_bg"], fg=c["accent_fg"] if n==cur else c["btn_secondary_fg"])


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = AlgoPlayApp(tk_root)
    tk_root.update_idletasks(); app.action_reset()
    tk_root.protocol("WM_DELETE_WINDOW", lambda: (
        getattr(getattr(app, "story_tab", None), "game_state", None) and app.story_tab.game_state.save(),
        tk_root.destroy()))
    tk_root.mainloop()
